import cv2
import datetime
import time
import os
import ffmpeg
import imageio_ffmpeg
from utils.overlay import draw_text_with_background

cap = cv2.VideoCapture(0)

# 解像度取得
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# FPSを取得
fps = cap.get(cv2.CAP_PROP_FPS)

# ファイル名
dt = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
avi_filename = f"{dt}.avi"
mp4_filename = f"{dt}.mp4"
codec = cv2.VideoWriter_fourcc(*"XVID")

out = None
start_time = 0
recording = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 操作案内表示
    draw_text_with_background(frame, "[s]:Start REC", (5, 415), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), (255, 255, 255), 0.6, 2)
    draw_text_with_background(frame, "[e]:End REC",   (5, 445), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), (255, 255, 255), 0.6, 2)
    draw_text_with_background(frame, "[q]:Quit",      (5, 475), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), (255, 255, 255), 0.6, 2)

    if recording:
        elapsed_time = time.time() - start_time
        elapsed_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        draw_text_with_background(frame, f"REC:{elapsed_str}", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), (255, 255, 255), 0.6, 2)
        out.write(frame)  # 毎フレーム書き込む

    # フレームを表示
    cv2.imshow('Frame', frame)

    key = cv2.waitKey(1) & 0xFF

    # 録画開始
    if key == ord('s') and not recording:
        out = cv2.VideoWriter(avi_filename, codec, fps, (width, height))  # FPSを設定
        if not out.isOpened():
            print("❌ VideoWriter の初期化に失敗しました")
            break
        recording = True
        start_time = time.time()
        print("📹 録画を開始しました")

    # 録画終了
    elif key == ord('e') and recording:
        recording = False
        out.release()
        print("🛑 録画を終了しました")

        # ffmpeg-python で mp4 に変換
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
            print("❌ 変換中にエラーが発生:", e)

    # 終了
    elif key == ord('q'):
        print("👋 アプリを終了します")
        break

# 後片付け
cap.release()
if out:
    out.release()
cv2.destroyAllWindows()
