import cv2
import time
import os
import numpy as np
from xml_read_write import read_coordinates_from_xml, write_coordinates_to_xml
import threading


class LED_Detection:
    def __init__(self, interface_NR=0, showPreview=False):
        self.cap = cv2.VideoCapture(interface_NR)
        self.capture_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        print('capture width: ', self.capture_width)
        self.capture_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print('capture_height: ', self.capture_height)
        self.mask_of_rois = np.zeros((self.capture_height, self.capture_width, 3), dtype=np.uint8)

        path_to_RAEngineering = r"C:\RAEngineering"
        path_to_xml_config = r"C:\RAEngineering\LED_detection_config.xml"
        if not os.path.exists(path_to_RAEngineering):
            os.makedirs(path_to_RAEngineering)
        if not os.path.isfile(path_to_xml_config):
            print("LED_detection_config.xml doesn't exist")
            self.list_of_rois = []
            write_coordinates_to_xml(self.list_of_rois)
        else:
            print("LED_detection_config.xml does exist")
            self.list_of_rois = read_coordinates_from_xml(path_to_xml_config)

            for roi in self.list_of_rois:
                cv2.rectangle(self.mask_of_rois, roi[0], roi[1], (255, 0, 0), 2)

        # private variables used for drawing areas to check
        self._start_point = None
        self._end_point = None
        self._drawing = None

    def start_capture(self):
        t2 = threading.Thread(target=self._run, args=())
        t2.start()

    def stop_capture(self):
        self.capture_run = False

    def _run(self):
        self.capture_run = True
        prev_time = 0
        while True:
            ret, frame = self.cap.read()
            current_time = time.time()
            fps = 1 / (current_time - prev_time)
            prev_time = current_time
            self.print_roi_colors(frame)
            cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
            frame = cv2.bitwise_or(frame, self.mask_of_rois)
            cv2.imshow('frame', frame)
            cv2.setMouseCallback("frame", self.draw_rectangle)

            # show windows with checked areas if list of areas is not empty
            if self.list_of_rois:
                cv2.imshow("Rectangle Drawing", self.mask_of_rois)
            # destroy window with checked areas if list of areas is empty
            if cv2.getWindowProperty("Rectangle Drawing", cv2.WND_PROP_VISIBLE) and not self.list_of_rois:
                cv2.destroyWindow("Rectangle Drawing")

            if cv2.waitKey(1) == ord('q'):
                break

            if not self.capture_run:
                break

            print(self.list_of_rois)

        self.cap.release()
        cv2.destroyAllWindows()

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
            _drawing = True
            self._start_point = (x, y)
            cv2.rectangle(self.mask_of_rois, self._start_point, (x, y), (255, 0, 0), 2)
        elif event == cv2.EVENT_MOUSEMOVE:
            if self._drawing:
                self._end_point = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            _drawing = False
            cv2.rectangle(self.mask_of_rois, self._start_point, (x, y), (255, 0, 0), 2)
            self.list_of_rois.append(rising_order_for_roi(self._start_point, (x, y)))
            cv2.imshow("Rectangle Drawing", self.mask_of_rois)
            write_coordinates_to_xml(self.list_of_rois)
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.list_of_rois = []
            self.mask_of_rois = np.zeros((self.capture_height, self.capture_width, 3), dtype=np.uint8)

    def print_roi_colors(self, frame):
        for roi in self.list_of_rois:
            create_pixel_matrix(frame, *roi[0], *roi[1])


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
    led_detection.start_capture()

    led_detection.stop_capture()


if __name__ == "__main__":
    main()
