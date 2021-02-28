from flask import Blueprint, request
from libs.qcloud import QCloudCOSGetCredentialError
from models.qcloud import NotSupportedCategoryError, get_cos_temp_credential
from views.render import error, ok


app = Blueprint('auth', __name__, url_prefix="/auth")


@app.route('/cos_temp_credential/', methods=['POST'])
def cos_temp_credential():
    data = request.get_json()
    if not data:
        return error('请输入 category')

    _category: str = data.get('category', '')

    if not _category:
        return error('请输入 category')

    try:
        category: int = int(_category)
    except (ValueError, TypeError):
        return error('category 类型错误')

    try:
        result = get_cos_temp_credential(category)
    except (QCloudCOSGetCredentialError, NotSupportedCategoryError) as e:
        return error(str(e.message))

    return ok(result)
