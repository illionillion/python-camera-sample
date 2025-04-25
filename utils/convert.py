import ffmpeg
import os
import imageio_ffmpeg

def convert_to_mp4(avi_filename: str, mp4_filename: str):
    """ffmpeg-python で mp4 に変換"""

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
