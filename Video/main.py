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
fpsReader = cvzone.FPS()
classifier= Classifier("Model/keras_model.h5","AlphabetReferences/classes.txt")

offset=20
imgSize=800

classes= ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', "Space"]

while camera.isOpened():
    #print(randomString(10))
    success, img= camera.read()
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

        if aspectRatio>1:
            k=imgSize/height
            calculatedWidth=math.ceil(k*width)
            imgResize= cv2.resize(onlyHand,(calculatedWidth,imgSize))
            imageResized= imgResize.shape
            widthGap=math.ceil((imgSize-calculatedWidth)/2)
            whiteImage[:,widthGap:calculatedWidth+widthGap]=imgResize
            prediction, index= classifier.getPrediction(whiteImage)
            print(prediction,index)
        
        else:
            k=imgSize/width
            calculatedHeight=math.ceil(k*height)
            imgResize= cv2.resize(onlyHand,(imgSize,calculatedHeight))
            imageResized= imgResize.shape
            heightGap=math.ceil((imgSize-calculatedHeight)/2)
            whiteImage[heightGap:calculatedHeight+heightGap,:]=imgResize
            prediction, index= classifier.getPrediction(whiteImage)
            print(prediction,index)
        cv2.imshow("White",whiteImage)
        #cv2.imshow("OnlyHand",onlyHand)
    #cv2.imshow("White",whiteImage)
    cv2.imshow("Webcam",img)

    

    if cv2.waitKey(1) == ord("c"):
        print("close window")
        break
    

camera.release()
cv2.destroyAllWindows()