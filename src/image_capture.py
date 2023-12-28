from multiprocessing import Process, Event
from data_models import CaptureSignalPayload

import cv2

import constants


class ImageCaptureProcess(Process):
    def __init__(self, device, capture_signal, quit_event):
        super().__init__()
        self.device = device
        self.capture_signal = capture_signal
        self.quit_event = quit_event
        self.cap = None

    def run(self):
        self.cap = cv2.VideoCapture()

        while not self.quit_event.is_set():
            ret, frame = self.cap.read()
            payload = self.capture_signal.payload

            if payload.is_capture:
                payload.frame = preprocess_frame(frame)
                store_data(payload)
                payload.is_capture = False

        self.quit()

    def quit(self):
        if self.cap:
            self.cap.release()
        self.cap = None
        self.quit_event.set()


def preprocess_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(
        frame, (constants.IMAGE_HEIGHT, constants.IMAGE_WIDTH))
    return frame


def store_data(payload: CaptureSignalPayload):
    pass
