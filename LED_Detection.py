import cv2
import time
import numpy as np

class LED_Detection:
    def __init__(self,interface_NR=0,showPreview=False):
        self.cap = cv2.VideoCapture(interface_NR)
        self.capture_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        print('capture width: ', self.capture_width)
        self.capture_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print('capture_height: ', self.capture_height)
        self.mask_of_rois = np.zeros((self.capture_height, self.capture_width, 3), dtype=np.uint8)

    def draw_rectangle(self,event, x, y, flags, param):
        global start_point, end_point, drawing

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            start_point = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                end_point = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            cv2.rectangle(self.mask_of_rois, start_point, (x, y), (255, 0, 0), 1)
            cv2.imshow("Rectangle Drawing", self.mask_of_rois)


def main():

    led_detection = LED_Detection()

    prev_time = 0
    while True:
        ret, frame = led_detection.cap.read()

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
        frame = cv2.bitwise_or(frame, led_detection.mask_of_rois)
        cv2.imshow('frame', frame)
        cv2.setMouseCallback("frame", led_detection.draw_rectangle)

        if cv2.waitKey(1) == ord('q'):
            break

    led_detection.cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
