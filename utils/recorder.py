import cv2
import threading
import queue
import ffmpeg
import imageio_ffmpeg
import os
class Recorder:
    def __init__(self, filename: str, codec, fps: float, size: tuple[int, int]):
        self.filename = filename
        self.queue = queue.Queue()
        self.writer = cv2.VideoWriter(filename, codec, fps, size)
        self.recording = False
        self.converting = False
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
    
    def start_conversion(self, mp4_filename: str):
        """変換処理を非同期で開始"""
        def _convert():
            self.converting = True
            self._convert_to_mp4(self.filename, mp4_filename)
            self.converting = False

        threading.Thread(target=_convert, daemon=True).start()

    def _convert_to_mp4(self, avi_filename: str, mp4_filename: str):
        """内部用: ffmpegでmp4変換"""
        print("🔄 mp4 に変換中...")
        try:
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            ffmpeg.input(avi_filename).output(
                mp4_filename,
                vcodec="libx264",
                crf=23,
                preset="veryfast"
            ).run(cmd=ffmpeg_exe)
            print(f"✅ 変換完了: {mp4_filename}")
            os.remove(avi_filename)
            print(f"🗑 元のファイル削除: {avi_filename}")
        except Exception as e:
            print("❌ 変換中にエラー:", e)
