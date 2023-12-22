from models.ai.exceptions import RequestException
from models.init_db import azure_vision
from requests import HTTPError


def img_ocr(img_url_or_path: str) -> str:
    if not img_url_or_path:
        raise ValueError("img_url_or_path is empty")

    try:
        if img_url_or_path.startswith('http'):
            result = azure_vision.analyze_read_from_img_url(img_url=img_url_or_path)
        else:
            with open(img_url_or_path, 'rb') as f:
                img_data = f.read()
            result = azure_vision.analyze_read_by_img_data(img_data=img_data)
    except HTTPError:
        raise RequestException()

    return result.readResult.content
