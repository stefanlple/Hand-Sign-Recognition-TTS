import numpy as np
import cvzone
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import cv2
import math
import random
import string
#import mediapipe as mp

#pip3 install cvzone==1.5.6  
#pip3 install numpy
#pip3 install opencv-python==4.5.4.60
#pip3 install/ pip3 install mediapipe-silicon==0.8.10.1
#pip3 install tensorflow-macos==2.9.1 #pip3 install tensorflow==2.9.1

camera = cv2.VideoCapture(0)
detector= cvzone.HandTrackingModule.HandDetector(detectionCon=0.8,maxHands=1)
classifier= Classifier("Model/keras_model.h5","AlphabetReferences/classes.txt")
fpsReader = cvzone.FPS()

offset=20
imgSize=800

classes= ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', "Space"]

message=""

while camera.isOpened():
    #print(randomString(10))
    success, img= camera.read()
    mainImg=img.copy()
    hands, img= detector.findHands(img)
    fps, img = fpsReader.update(img,pos=(50,80),color=(0,255,0),scale=5,thickness=5)
    whiteImage = np.zeros((imgSize, imgSize, 3), np.uint8)
    whiteImage[:] = (255,255,255)
    if hands:
        landmarksPoints= hands[0]
        x,y,width,height= hands[0]["bbox"]
        onlyHand= img[y-offset:y+height+offset,x-offset:x+width+offset]
        #print(landmarksPoints)
        #img=cv2.flip(img,1)
        #cvzone.cornerRect(img, hands[0]["bbox"])
        

        aspectRatio= height/width
        try:
            if aspectRatio>1:
                k=imgSize/height
                calculatedWidth=math.ceil(k*width)
                imgResize= cv2.resize(onlyHand,(calculatedWidth,imgSize))
                imageResized= imgResize.shape
                widthGap=math.ceil((imgSize-calculatedWidth)/2)
                whiteImage[:,widthGap:calculatedWidth+widthGap]=imgResize
                prediction, index= classifier.getPrediction(whiteImage)
            
            else:
                k=imgSize/width
                calculatedHeight=math.ceil(k*height)
                imgResize= cv2.resize(onlyHand,(imgSize,calculatedHeight))
                imageResized= imgResize.shape
                heightGap=math.ceil((imgSize-calculatedHeight)/2)
                whiteImage[heightGap:calculatedHeight+heightGap,:]=imgResize
                prediction, index= classifier.getPrediction(whiteImage)
        except:
            print("resize failed")
        #print(prediction,index)
        cv2.imshow("White",whiteImage)
        #cv2.imshow("OnlyHand",onlyHand)
        cv2.putText(mainImg, classes[index],(x+100,y-85), cv2.FONT_ITALIC, 3 , (255,0,0),5)
        cv2.rectangle(mainImg,(x-offset-50,y-offset-50),(x+offset+width+50,y+offset+height+50),(255,0,0),4)
    #cv2.imshow("White",whiteImage)
    cv2.putText(mainImg, message,(00,60), cv2.FONT_HERSHEY_SIMPLEX, 2 , (255,255,255),5)
    cv2.imshow("Webcam",mainImg)

    

    if cv2.waitKey(1) == ord("c"):
        print("close window")
        break
        
    if cv2.waitKey(25) == ord(" "):
        message+=str(classes[index])
    
    if cv2.waitKey(25) == 127: #delete key
        message=message[:-1]
    print(message)
camera.release()
cv2.destroyAllWindows()