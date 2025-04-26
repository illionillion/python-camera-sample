import cv2
import datetime
import time
import os
from utils.overlay import draw_text_with_background
from utils.recorder import Recorder

cap = cv2.VideoCapture(0)

# 解像度とFPS取得
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# FPS取得
fps = cap.get(cv2.CAP_PROP_FPS)

# コーデック
codec = cv2.VideoWriter_fourcc(*"XVID")

recorder = None
active_recorders = []
start_time = 0
avi_filename = ""
mp4_filename = ""

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 操作案内表示
    draw_text_with_background(frame, "[s]:Start REC", (5, 415), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), (255, 255, 255), 0.6, 2)
    draw_text_with_background(frame, "[e]:End REC",   (5, 445), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), (255, 255, 255), 0.6, 2)

    # 変換中インスタンスの削除（終了したものをクリーンアップ）
    active_recorders = [r for r in active_recorders if r.converting or r.recording]

    if any(r.converting for r in active_recorders):
        draw_text_with_background(frame, "Converting... Please wait", (5, 475), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), (255, 255, 255), 0.6, 2)
    else:
        draw_text_with_background(frame, "[q]:Quit", (5, 475), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), (255, 255, 255), 0.6, 2)

    # 録画中表示
    if recorder and recorder.recording:
        elapsed_time = time.time() - start_time
        elapsed_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        draw_text_with_background(frame, f"REC:{elapsed_str}", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), (255, 255, 255), 0.6, 2)
        recorder.write(frame)

    # フレームを表示
    cv2.imshow('RaspberryPi Camera', frame)
    key = cv2.waitKey(1) & 0xFF

    # 録画開始
    if key == ord('s') and (recorder is None or not recorder.recording):
        dt = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        avi_filename = f"{dt}.avi"
        mp4_filename = f"{dt}.mp4"
        recorder = Recorder(avi_filename, codec, fps, (width, height))
        recorder.start()
        active_recorders.append(recorder)
        start_time = time.time()
        print("📹 録画を開始しました")

    # 録画終了
    elif key == ord('e') and recorder and recorder.recording:
        recorder.stop()
        print("🛑 録画を終了しました")
        recorder.start_conversion(mp4_filename)

    # 終了（変換中があると終了不可。録画中ならavi削除）
    elif key == ord('q'):
        if any(r.converting for r in active_recorders):
            print("⚠️ 変換中のため終了できません。少々お待ちください。")
        else:
            if recorder and recorder.recording:
                recorder.stop()
                if os.path.exists(avi_filename):
                    os.remove(avi_filename)
                    print(f"🧹 録画途中のファイル {avi_filename} を削除しました")
            print("👋 アプリを終了します")
            break

# 後片付け
cap.release()
cv2.destroyAllWindows()
