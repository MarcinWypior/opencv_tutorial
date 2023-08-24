import cv2

img = cv2.imread("assets/image.jpg",-1)
#img = cv2.resize(img,(200,100))
img = cv2.resize(img,(0,0),fx=2,fy=2) # proportional saling
img= cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)

#cv2.imwrite("assets/newimage.jpg",img) zapisywanie obrazów

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()