import numpy as np
import cv2

camera = cv2.VideoCapture(0)

while True:
    cv2.imshow("Hand_Alphabet_Translator",camera)
    cv2.waitKey(0)
    cv2.destroyAllWindows()