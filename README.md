# 🎥 Webcam Recorder with Auto ffmpeg Conversion

Webカメラで動画を録画し、録画後に `ffmpeg` を使って自動で高互換な MP4 ファイルに変換してくれるツールです。  
OpenCV で録画し、`ffmpeg-python` により変換処理を行います。

## ✨ Features

- `[s]` で録画開始（`.avi` ファイルを作成）
- `[e]` で録画停止 → 自動的に `.mp4` に変換
- `[q]` で終了
- 録画中は `REC:00:00:00` のようにタイマー表示
- 録画ファイルは `YYYYMMDD_HHMMSS` 形式で保存

## 🧱 Requirements

- Python 3.8+
- ラズパイ or PC（macOS / Linux / Windows）

## 📦 Install

```bash
git clone https://github.com/illionillion/python-camera-sample.git
cd python-camera-sample
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```