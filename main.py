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

motion_detected = False
motion_detection_enabled = False
last_motion_time = time.time()

# モーション検出の待機時間
COOL_DOWN_TIME = 5  # 秒

# 前フレームとの差分を取るための初期化
previous_frame = None

# テキスト行の高さ
line_height = 30

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # モーション検出処理
    if motion_detection_enabled:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if previous_frame is None:
            previous_frame = gray
            continue

        frame_diff = cv2.absdiff(previous_frame, gray)
        threshold = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]

        # モーションが検出された場合
        if cv2.countNonZero(threshold) > 500:
            motion_detected = True
            last_motion_time = time.time()  # 最後の動きがあった時間を更新

            # 録画開始
            if recorder is None or not recorder.recording:
                dt = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                avi_filename = f"{dt}.avi"
                mp4_filename = f"{dt}.mp4"
                recorder = Recorder(avi_filename, codec, fps, (width, height))
                recorder.start()
                active_recorders.append(recorder)
                start_time = time.time()
                print("📹 Motion detected: Recording started")
        else:
            # COOL_DOWN_TIME秒以上動きがない場合に録画停止
            if time.time() - last_motion_time > COOL_DOWN_TIME and recorder and recorder.recording:
                recorder.stop()
                print("🛑 Recording stopped")
                recorder.start_conversion(mp4_filename)
                motion_detected = False

        # フレーム差分の処理を続ける
        previous_frame = gray

    # 操作案内表示
    draw_text_with_background(frame, "[s]:Start REC", (5, height - 5 * line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), (255, 255, 255), 0.6, 2)
    draw_text_with_background(frame, "[e]:End REC", (5, height - 4 * line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), (255, 255, 255), 0.6, 2)

    # モード表示
    if motion_detection_enabled:
        draw_text_with_background(frame, "[m]:Motion Detection Mode: ON", (5, height - 3 * line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), (255, 255, 255), 0.6, 2)
    else:
        draw_text_with_background(frame, "[m]:Motion Detection Mode: OFF", (5, height - 3 * line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), (255, 255, 255), 0.6, 2)

    # 変換中表示 or Quit
    if any(r.converting for r in active_recorders):
        draw_text_with_background(frame, "Converting... Please wait", (5, height - 2 * line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), (255, 255, 255), 0.6, 2)
    else:
        draw_text_with_background(frame, "[q]:Quit", (5, height - 2 * line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), (255, 255, 255), 0.6, 2)
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
        print("📹 Recording started")

    # 録画終了
    elif key == ord('e') and recorder and recorder.recording:
        recorder.stop()
        print("🛑 Recording stopped")
        recorder.start_conversion(mp4_filename)

    # モーション検出のオン/オフを切り替え
    elif key == ord('m'):
        motion_detection_enabled = not motion_detection_enabled
        if motion_detection_enabled:
            previous_frame = None
            print("🚶‍♂️ Motion Detection Mode: ON")
        else:
            print("🚶‍♂️ Motion Detection Mode: OFF")

    # 終了（変換中があると終了不可。録画中ならavi削除）
    elif key == ord('q'):
        if any(r.converting for r in active_recorders):
            print("⚠️ Cannot quit, conversion in progress. Please wait.")
        else:
            if recorder and recorder.recording:
                recorder.stop()
                if os.path.exists(avi_filename):
                    os.remove(avi_filename)
                    print(f"🧹 Deleted partial recording file {avi_filename}")
            print("👋 Exiting the application")
            break

    # 使い終わった recorder をクリーンアップ
    active_recorders = [r for r in active_recorders if r.recording or r.converting]


# 後片付け
cap.release()
cv2.destroyAllWindows()
