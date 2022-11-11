import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cv2


camera = cv2.VideoCapture(0)
detector= HandDetector(maxHands=1)

while True:
    success, img= camera.read()
    hands, img= detector.findHands(img)
    cv2.imshow("Hand_Alphabet_Translator",img)
    cv2.waitKey(1)
    cv2.destroyAllWindows()