import cv2
import numpy as np

img = cv2.imread("assets/soccer_practice.jpg")
template = cv2.imread("assets/shoe_2.PNG",0)
template = cv2.resize(template,(0,0),fx=0.8,fy=0.8)
#shoe = cv2.imread("assets/shoe.PNG")

h,w =template.shape

methods = [cv2.TM_CCOEFF,cv2.TM_CCOEFF_NORMED,cv2.TM_CCORR,
           cv2.TM_CCORR_NORMED,cv2.TM_SQDIFF,cv2.TM_SQDIFF_NORMED]

img2 = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
img2 = cv2.resize(img2,(0,0),fy=0.6,fx=0.6)

for i ,method in enumerate(methods):

    result = cv2.matchTemplate(img2,template,method)
    min_val , max_val, min_loc, max_loc =cv2.minMaxLoc(result)
    if method in [cv2.TM_SQDIFF,cv2.TM_SQDIFF_NORMED]:
        location = min_loc
    else:
        location = max_loc

    bottom_right = (location[0]+w+i*3,location[1]+h+i*3)
    cv2.rectangle(img,location,bottom_right,(255,0,0))
    cv2.imshow("Found",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #print(min_loc,max_loc)

