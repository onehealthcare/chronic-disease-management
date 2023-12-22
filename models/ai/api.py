import os

from models.ai.exceptions import RequestException
from models.init_db import azure_vision
from requests import HTTPError


def is_image_file(file_path):
    # 通过文件扩展名来判断是否是图片文件
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    _, file_extension = os.path.splitext(file_path)

    return file_extension.lower() in image_extensions


def img_ocr(img_url_or_path: str) -> str:
    if not img_url_or_path:
        raise ValueError("img_url_or_path is empty")

    if not is_image_file(img_url_or_path):
        raise ValueError("img_url_or_path is not an image file")

    try:
        if img_url_or_path.startswith('http'):
            result = azure_vision.analyze_read_from_img_url(img_url=img_url_or_path)
        else:
            if not os.path.exists(img_url_or_path):
                raise FileNotFoundError()

            with open(img_url_or_path, 'rb') as f:
                img_data = f.read()
            result = azure_vision.analyze_read_by_img_data(img_data=img_data)
    except HTTPError:
        raise RequestException()

    return result.readResult.content
