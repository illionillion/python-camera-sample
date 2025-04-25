import cv2

def draw_text_with_background(
    img,
    text,
    position,
    font,
    font_scale,
    text_color,
    bg_color,
    alpha,
    thickness=1,
    padding=5
):
    """背景付きでテキストを描画する"""
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
    x, y = position

    # 背景用の矩形の座標
    rect_x1, rect_y1 = x - padding, y - text_height - padding
    rect_x2, rect_y2 = x + text_width + padding, y + padding

    overlay = img.copy()
    cv2.rectangle(overlay, (rect_x1, rect_y1), (rect_x2, rect_y2), bg_color, -1)

    # 透過合成
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    # テキスト描画
    cv2.putText(img, text, (x, y), font, font_scale, text_color, thickness)
