import numpy as np
import cvzone
from cvzone.HandTrackingModule import HandDetector
import cv2
#import mediapipe as mp
##pip3 install cvzone
##pip3 install numpy
##pip3 install opencv-python
##pip3 install pip3 install mediapipe-silicon

camera = cv2.VideoCapture(0)
detector= cvzone.HandTrackingModule.HandDetector(detectionCon=0.8,maxHands=1)
fpsReader = cvzone.FPS()

offset=20
imgSize=400

while camera.isOpened():

    success, img= camera.read()
    hands, img= detector.findHands(img)
    fps, img = fpsReader.update(img,pos=(50,80),color=(0,255,0),scale=5,thickness=5)
    whiteImage = np.zeros((imgSize, imgSize, 3), np.uint8)
    whiteImage[:] = (0, 0, 255)

    if hands:
        landmarksPoints= hands[0]
        x,y,w,h= hands[0]["bbox"]
        onlyHand= img[y-offset:y+h+offset,x-offset:x+w+offset]
        print(landmarksPoints)
        onlyHandShape= onlyHand.shape
        print(onlyHandShape)
        whiteImage[0:onlyHandShape[0],0:onlyHandShape[1]]=onlyHand

        #img=cv2.flip(img,1)
        cvzone.cornerRect(img, hands[0]["bbox"])
        cv2.imshow("OnlyHand",onlyHand)

    cv2.imshow("Hand_Alphabet_Translator",whiteImage)
    #cv2.imshow("Hand_Alphabet_Translator",img)

    if cv2.waitKey(25) != -1:
        break

camera.release()
cv2.destroyAllWindows()