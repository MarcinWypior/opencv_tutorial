import cv2
import numpy as np

img = cv2.imread("assets/image.jpg", -1)

tag = img[70:170,90:190]
img[:100,:100] = tag


cv2.imshow('image', img)

cv2.waitKey(0)
cv2.destroyAllWindows()