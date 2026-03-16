import pyaudio
import wave
import threading

class AudioRecorder:
    def __init__(self, rate=44100, chunk=1024, channels=1):
        self.rate = rate
        self.chunk = chunk
        self.channels = channels
        self.running = False
        self.frames = []
        self.lock = threading.Lock()

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def _record(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        frames_per_buffer=self.chunk)
        while self.running:
            data = stream.read(self.chunk, exception_on_overflow=False)
            with self.lock:
                self.frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()

    def get_and_clear_frames(self):
        with self.lock:
            frames = self.frames.copy()
            self.frames.clear()
        return frames

    def stop(self):
        self.running = False
        self.thread.join()

    def save(self, filename, frames):
        p = pyaudio.PyAudio()
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))
        p.terminate()