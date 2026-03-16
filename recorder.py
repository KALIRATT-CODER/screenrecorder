import cv2
import numpy as np
import mss
import threading
import time

class ScreenRecorder:
    def __init__(self, fps=10):
        self.fps = fps
        self.running = False
        self.frames = []
        self.lock = threading.Lock()

    def start(self):
        self.running = True
        t = threading.Thread(target=self._record)
        t.daemon = True
        t.start()
        self.thread = t

    def _record(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            while self.running:
                img = np.array(sct.grab(monitor))
                frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                with self.lock:
                    self.frames.append(frame)
                time.sleep(1 / self.fps)

    def get_and_clear_frames(self):
        with self.lock:
            frames = self.frames.copy()
            self.frames.clear()
        return frames

    def stop(self):
        self.running = False
        self.thread.join()