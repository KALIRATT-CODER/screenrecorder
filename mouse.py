from pynput import mouse
import threading

class MouseTracker:
    def __init__(self):
        self.clicks = []
        self.lock = threading.Lock()
        self.listener = None

    def start(self):
        self.listener = mouse.Listener(on_click=self._on_click)
        self.listener.start()

    def _on_click(self, x, y, button, pressed):
        if pressed:
            with self.lock:
                self.clicks.append((int(x), int(y)))

    def get_and_clear_clicks(self):
        with self.lock:
            clicks = self.clicks.copy()
            self.clicks.clear()
        return clicks

    def stop(self):
        if self.listener:
            self.listener.stop()