
from io import BytesIO
import logging
import os
import random
from PIL import Image, ImageDraw, ImageFont
from plugins.gocqOnQQ.entities.components import Image as QQImage


def add_text_to_image(base64_image: bytes, text_list: list):
    """将文本添加到图片上"""
    def _len(string: str):
        """获取字符串s的长度"""
        res = 0
        for ch in string:
            if 0 <= ord(ch) < 128:
                res += 1
            else:
                res += 2
        return res

    # 将 base64 图片解码为图像对象
    image = Image.open(BytesIO(base64_image))
    width, height = image.size

    # 创建一个可以在图片上绘制的对象
    draw = ImageDraw.Draw(image)

    # 设置字体和字号
    len_max_text_list = _len(max(text_list, key=_len))//2
    font_size = min(width // 12, height // 6)
    if font_size <= 10:
        font_size = 10
    x, y = width-20-len_max_text_list * \
        font_size, height-20-len(text_list)*font_size
    logging.debug(
        f'插件[PictureForAddWatermark] 图片预览参数: {width=} {height=} {x=} {y=} {len_max_text_list=} {font_size=} {text_list=}')
    font = ImageFont.truetype("simkai.ttf", font_size)

    # 根据背景颜色来确定文字颜色
    num_samples = 10
    sample_points = [
        (random.randint(0, width - 1), random.randint(0, height - 1))
        for _ in range(num_samples)
    ]
    background_colors = [image.getpixel(point) for point in sample_points]
    for i in range(len(background_colors)):
        if isinstance(background_colors[i], int):
            background_colors[i] = \
                (background_colors[i],
                 background_colors[i], background_colors[i])

    avg_background_color = \
        tuple(map(lambda x: sum(x) // num_samples, zip(*background_colors)))

    text_color = (0, 0, 0) if \
        sum(avg_background_color) / 3 > 128 else (255, 255, 255)

    logging.debug(
        f'插件[PictureForAddWatermark] 图片预览参数: {sample_points=} {background_colors=} {avg_background_color=} {text_color=}')

    for text in text_list:
        draw.text((x, y), text, fill=text_color, font=font, align="left")
        y += font_size + 5

    image_data = BytesIO()
    image = image.convert("RGB")
    image.save(image_data, format='PNG')
    image_data.seek(0)

    file_path = os.path.join(os.path.dirname(__file__), 'temp.jpg')
    image = Image.open(BytesIO(image_data.getvalue()))
    image.save(file_path)
    return QQImage.fromFileSystem(file_path)
