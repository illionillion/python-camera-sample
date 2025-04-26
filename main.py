import cv2
import datetime
import time
from utils.overlay import draw_text_with_background
from utils.convert import convert_to_mp4
import threading

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
        draw_text_with_background(frame, f"REC:{elapsed_str}", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), (255, 255, 255), 0.6, 2)
        out.write(frame)  # 毎フレーム書き込む

    # フレームを表示
    cv2.imshow('RaspberryPi Camera', frame)

    key = cv2.waitKey(1) & 0xFF

    # 録画開始
    if key == ord('s') and not recording:
        dt = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        avi_filename = f"{dt}.avi"
        mp4_filename = f"{dt}.mp4"
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

        # 非同期で変換処理
        threading.Thread(
            target=convert_to_mp4,
            args=(avi_filename, mp4_filename),
            daemon=True
        ).start()

    # 終了
    elif key == ord('q'):
        print("👋 アプリを終了します")
        break

# 後片付け
cap.release()
if out:
    out.release()
cv2.destroyAllWindows()
