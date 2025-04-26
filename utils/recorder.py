import cv2
import threading
import queue

class Recorder:
    def __init__(self, filename: str, codec, fps: float, size: tuple[int, int]):
        self.filename = filename
        self.queue = queue.Queue()
        self.writer = cv2.VideoWriter(filename, codec, fps, size)
        self.recording = False
        self.thread = threading.Thread(target=self._write_frames, daemon=True)

    def start(self):
        self.recording = True
        self.thread.start()

    def write(self, frame):
        if self.recording:
            self.queue.put(frame)

    def stop(self):
        self.recording = False
        self.queue.put(None)  # 終了シグナル
        self.thread.join()
        self.writer.release()

    def _write_frames(self):
        while True:
            frame = self.queue.get()
            if frame is None:
                break
            self.writer.write(frame)
