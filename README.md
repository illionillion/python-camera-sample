# 🎥 Webcam Recorder with Motion Detection & Auto ffmpeg Conversion

Webカメラで動画を録画し、録画後に `ffmpeg` を使って自動で高互換な MP4 ファイルに変換してくれるツールです。  
OpenCV で録画・モーション検出を行い、`ffmpeg-python` により変換処理を行います。

## ✨ Features

- `[s]` キーで手動録画開始（`.avi` ファイルを作成）
- `[e]` キーで録画停止 → 自動的に `.mp4` に変換
- `[m]` キーでモーション検出モードのON/OFF切り替え
  - モーション検出ON時、動きを感知すると自動で録画開始・停止
- `[q]` キーで終了（録画中の場合は録画ファイルを削除して終了）
- 録画中は画面左上に `REC:00:00:00` のタイマーを表示
- 常に画面右上に現在時刻 `YYYY/MM/DD HH:MM:SS` を表示
- 録画ファイルは `YYYYMMDD_HHMMSS` 形式で保存

## 🧱 Requirements

- Python 3.8+
- Raspberry Pi または PC（macOS / Linux / Windows）
- ffmpeg がインストールされていること

## 📦 Install

```bash
git clone https://github.com/illionillion/python-camera-sample.git
cd python-camera-sample
python -m venv .venv
source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate
pip install -r requirements.txt
```

## ⚙️ Usage

```bash
python main.py
```

- 起動するとカメラが立ち上がり、画面に操作案内が表示されます。
- モーション検出モードにすると、動きを検出したときだけ自動で録画します。
