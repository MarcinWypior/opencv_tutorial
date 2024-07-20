import cv2
import time
import numpy as np


class LED_Detection:
    def __init__(self, interface_NR=0, showPreview=False):
        self.cap = cv2.VideoCapture(interface_NR)
        self.capture_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        print('capture width: ', self.capture_width)
        self.capture_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print('capture_height: ', self.capture_height)
        self.mask_of_rois = np.zeros((self.capture_height, self.capture_width, 3), dtype=np.uint8)
        self.list_of_rois = []
        self._start_point = None
        self._end_point = None
        self._drawing = None

    def draw_rectangle(self, event, x, y, flags, param):
        def rising_order_for_roi(start, stop):
            start_x, start_y = start
            stop_x, stop_y = stop

            if start_x > stop_x:
                start_x, stop_x = stop_x, start_x
            if start_y > stop_y:
                start_y, stop_y = stop_y, start_y

            return (start_x, start_y), (stop_x, stop_y)

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            self._start_point = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE:
            if self._drawing:
                self._end_point = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            cv2.rectangle(self.mask_of_rois, self._start_point, (x, y), (255, 0, 0), 2)
            self.list_of_rois.append(rising_order_for_roi(self._start_point, (x, y)))
            cv2.imshow("Rectangle Drawing", self.mask_of_rois)
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.list_of_rois = []
            self.mask_of_rois = np.zeros((self.capture_height, self.capture_width, 3), dtype=np.uint8)
            if self.list_of_rois:
                cv2.imshow("Rectangle Drawing", self.mask_of_rois)

    def print_roi_colors(self, frame):
        for roi in self.list_of_rois:
            create_pixel_matrix(frame, *roi[0], *roi[1])

    def stop_capture(self):
        self.cap.release()
        cv2.destroyAllWindows()


def print_pixels_in_area(frame, x1, y1, x2, y2):
    for y in range(y1, y2):
        for x in range(x1, x2):
            # Get the BGR values of each pixel
            b, g, r = frame[y, x]
            print(f'Pixel at ({x}, {y}) - B: {b}, G: {g}, R: {r}')


def create_pixel_matrix(frame, x1, y1, x2, y2):
    # Define the dimensions of the matrix
    height = y2 - y1
    width = x2 - x1

    # Create an empty matrix to store pixel colors
    pixel_matrix = np.zeros((height, width, 3), dtype=np.uint8)

    # Iterate over the area defined by coordinates (x1, y1) and (x2, y2)
    for y in range(y1, y2):
        for x in range(x1, x2):
            # Get the BGR values of each pixel and store them in the matrix
            pixel_matrix[y - y1, x - x1] = frame[y, x]
    return pixel_matrix


def main():
    led_detection = LED_Detection()

    prev_time = 0
    while True:
        ret, frame = led_detection.cap.read()
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        # print(led_detection.list_of_rois)
        led_detection.print_roi_colors(frame)
        cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
        frame = cv2.bitwise_or(frame, led_detection.mask_of_rois)
        cv2.imshow('frame', frame)
        cv2.setMouseCallback("frame", led_detection.draw_rectangle)

        if cv2.waitKey(1) == ord('q'):
            break

    led_detection.stop_capture()


if __name__ == "__main__":
    main()
