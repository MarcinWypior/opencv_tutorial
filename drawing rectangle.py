import cv2
import numpy as np

def draw_rectangle(event, x, y, flags, param):
    global start_point, end_point, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            end_point = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(image, start_point, (x, y), (255, 0, 0), 2)
        cv2.imshow("Rectangle Drawing", image)

image = np.zeros((512, 512, 3), dtype=np.uint8)
drawing = False
start_point = None
end_point = None

cv2.namedWindow("Rectangle Drawing")
cv2.setMouseCallback("Rectangle Drawing", draw_rectangle)

while True:
    cv2.imshow("Rectangle Drawing", image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()