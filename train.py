import numpy as np
import cv2

img = np.zeros(shape=(240,360,3), dtype=np.uint8)

camera = cv2.VideoCapture(0)

cv2.imshow("hello world",camera)
cv2.waitKey(0)
cv2.destroyAllWindows()