import os
import re
from typing import Optional

import simplejson
from libs.openai.dto import Result
from models.ai.dto import FujixRecipe
from models.ai.exceptions import RequestException
from models.init_db import azure_open_ai, azure_vision
from requests import HTTPError, ReadTimeout
from utils.logging import file_logger


logger = file_logger('models.ai')


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

    logger.info(f"img_ocr,request,img_url_or_path:{img_url_or_path}")
    try:
        if img_url_or_path.startswith('http'):
            result = azure_vision.analyze_read_from_img_url(img_url=img_url_or_path)
        else:
            if not os.path.exists(img_url_or_path):
                raise FileNotFoundError()

            with open(img_url_or_path, 'rb') as f:
                img_data = f.read()
            result = azure_vision.analyze_read_by_img_data(img_data=img_data)
    except HTTPError as e:
        logger.error(f"img_ocr,http_error,img_url_or_path:{img_url_or_path}-error:{e}")
        raise RequestException()

    content: str = result.readResult.content
    logger.info(f"img_ocr,ok,img_url_or_path:{img_url_or_path}-content:{content}")
    return content


def img_data_ocr(img_data: bytes) -> str:
    if not img_data:
        raise ValueError("img_url_or_path is empty")

    if not isinstance(img_data, bytes):
        raise ValueError("img_data is not bytes")

    logger.info(f"img_ocr,request,img_length:{len(img_data)}")
    try:
        result = azure_vision.analyze_read_by_img_data(img_data=img_data)
    except (HTTPError, ReadTimeout) as e:
        logger.error(f"img_ocr,http_error,img_length:{len(img_data)}-error:{e}")
        raise RequestException()

    content: str = result.readResult.content
    logger.info(f"img_ocr,request,img_length:{len(img_data)}-content:{content}")
    return content


def open_ai_fujix_json_util(message: str) -> Optional[FujixRecipe]:
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

    logger.info(f"open_ai_fujix_json_util,request,messages:{messages}")
    try:
        r: Result = azure_open_ai.chat(messages=messages)
    except (HTTPError, ReadTimeout) as e:
        logger.error(f"open_ai_fujix_json_util,http_error,messages:{messages}-error:{e}")
        raise RequestException

    if not r.choices:
        logger.error(f"open_ai_fujix_json_util,empty_choices,messages:{messages}")
        return None

    content: str = r.choices[0].message.content
    if not content:
        logger.error(f"open_ai_fujix_json_util,empty_content,messages:{messages}")
        return None

    group = re.findall("{.+}", content, re.S)
    if not group:
        logger.error(f"open_ai_fujix_json_util,invalid_content,messages:{messages}")
        return None

    try:
        data = simplejson.loads(group[0])
    except ValueError:
        logger.error(f"open_ai_fujix_json_util,invalid_json,messages:{messages}")
        return None

    logger.info(f"open_ai_fujix_json_util,ok,messages:{messages}-data:{data}")
    return FujixRecipe.parse_obj(data)
