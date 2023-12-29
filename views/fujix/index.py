from typing import Optional

import simplejson
from flask import g, request
from models.ai import img_data_ocr
from models.ai.api import open_ai_fujix_json_util
from models.ai.dto import FujixRecipe
from models.ai.exceptions import RequestException
from utils.logging import file_logger as _logger
from views.fujix import app
from views.middleware.auth import need_login
from views.render import ok
from werkzeug.datastructures import FileStorage


logger = _logger('views.fujix.index')


@app.route('/ocr/', methods=['POST'])
@need_login
def ocr():
    # return ok({'film_simulation': 'Nostalgic Neg.', 'dynamic_range': 'DR200', 'grain_effect': 'Strong Small', 'color_chrome_effect': 'Strong', 'color_chrome_effect_blue': 'Off', 'white_balance': 'Fluorescent 1, - 5 Red & 0 Blue', 'highlight': '+4', 'shadow': '+3', 'color': '-1', 'sharpness': '-2', 'noise_reduction': '-4', 'clarity': '-2', 'iso': 'up to ISO 6400', 'exposure_compensation': '0 to +2/3'})
    user_id: int = g.me.id
    data = request.form
    logger.info(f"ocr,request,{user_id}-{simplejson.dumps(data)}")
    fs: FileStorage = request.files['file']
    img_data = fs.read()
    try:
        message: str = img_data_ocr(img_data)
        if not message:
            return ok()
        data: Optional[FujixRecipe] = open_ai_fujix_json_util(message=message)
    except RequestException:
        return ok()
    except ValueError:
        return ok()

    if not data:
        return ok()

    return ok(data.dict())
