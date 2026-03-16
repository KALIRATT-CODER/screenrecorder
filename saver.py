import cv2
import os
import time
import threading
from datetime import datetime

class Saver:
    def __init__(self, screen_recorder, audio_recorder, mouse_tracker,
                 output_dir="recordings", interval=30, fps=5):
        self.screen = screen_recorder
        self.audio = audio_recorder
        self.mouse = mouse_tracker
        self.output_dir = output_dir
        self.interval = interval
        self.fps = fps
        self.running = False
        os.makedirs(output_dir, exist_ok=True)

    def start(self):
        self.running = True
        t = threading.Thread(target=self._loop)
        t.daemon = True
        t.start()
        self.thread = t

    def _loop(self):
        while self.running:
            time.sleep(self.interval)
            self._save_chunk()

    def _save_chunk(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        frames = self.screen.get_and_clear_frames()
        audio_frames = self.audio.get_and_clear_frames()
        clicks = self.mouse.get_and_clear_clicks()

        if frames:
            h, w, _ = frames[0].shape
            video_path = os.path.join(self.output_dir, f"{timestamp}_screen.avi")
            out = cv2.VideoWriter(video_path,
                                  cv2.VideoWriter_fourcc(*'XVID'),
                                  self.fps, (w, h))
            for frame in frames:
                for (x, y) in clicks:
                    cv2.circle(frame, (x, y), 15, (0, 0, 255), -1)
                out.write(frame)
            out.release()
            print(f"[+] Vidéo sauvegardée : {video_path}")

        if audio_frames:
            audio_path = os.path.join(self.output_dir, f"{timestamp}_audio.wav")
            self.audio.save(audio_path, audio_frames)
            print(f"[+] Audio sauvegardé : {audio_path}")

    def stop(self):
        self.running = False
        self._save_chunk()