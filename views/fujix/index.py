import simplejson
from flask import g, request
from models.ai import img_data_ocr
from utils.logging import file_logger as _logger
from views.fujix import app
from views.middleware.auth import need_login
from views.render import ok
from werkzeug.datastructures import FileStorage


logger = _logger('views.fujix.index')


@app.route('/ocr/', methods=['POST'])
@need_login
def ocr():
    user_id: int = g.me.id
    data = request.form
    logger.info(f"ocr,request,{user_id}-{simplejson.dumps(data)}")
    fs: FileStorage = request.files['file']
    img_data = fs.read()
    content: str = img_data_ocr(img_data)

    return ok({"content": content})
