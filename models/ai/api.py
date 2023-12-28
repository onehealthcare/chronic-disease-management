import os

from libs.openai.dto import Result
from models.ai.exceptions import RequestException
from models.init_db import azure_open_ai, azure_vision
from requests import HTTPError


def is_image_file(file_path):
    # 通过文件扩展名来判断是否是图片文件
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    _, file_extension = os.path.splitext(file_path)

    return file_extension.lower() in image_extensions


def img_ocr(img_url_or_path: str) -> str:
    if not img_url_or_path:
        raise ValueError("img_url_or_path is empty")

    if not isinstance(img_url_or_path, str):
        raise ValueError("img_url_or_path is not str")

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


def img_data_ocr(img_data: bytes) -> str:
    if not img_data:
        raise ValueError("img_url_or_path is empty")

    if not isinstance(img_data, bytes):
        raise ValueError("img_data is not bytes")

    try:
        result = azure_vision.analyze_read_by_img_data(img_data=img_data)
    except HTTPError:
        raise RequestException()

    return result.readResult.content


def open_ai_fujix_json_util(message: str) -> str:
    messages = [{
        "role": "system",
        "content": "Assistant is an AI chatbot that helps users turn a natural language list into JSON format. After users input a list they want in JSON format,   it will provide suggested list of attribute labels if the user has not provided any, then ask the user to confirm them before creating the list."
    }, {
        "role": "user",
        "content": f''' 格式化下面的消息，使用 json 返回，返回的内容除了 json 信息外不需要其他的话：\n{message}\njson 的格式为：\n
            {{
                "film_simulation": "value_placeholder",
                "dynamic_range": "value_placeholder",
                "grain_effect": "value_placeholder",
                "color_chrome_effect": "value_placeholder",
                "color_chrome_effect_blue": "value_placeholder",
                "white_balance": "value_placeholder",
                "highlight": "value_placeholder",
                "shadow": "value_placeholder",
                "color": "value_placeholder",
                "sharpness": "value_placeholder",
                "noise_reduction": "value_placeholder",
                "clarity": "value_placeholder",
                "iso": "value_placeholder",
                "exposure_compensation": "value_placeholder"
            }}\n如果没有对应的 value，请用 - 替代。\n以下是格式化后的 json 对象：'''
    }]

    r: Result = azure_open_ai.chat(messages=messages)
    return r.choices[0].message.content
