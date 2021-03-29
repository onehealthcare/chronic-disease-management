from flask import Blueprint, request
from libs.qcloud import QCloudCOSGetCredentialError
from models.qcloud import get_cos_temp_credential
from models.sms_sys import generate_auth_code
from views.render import error, ok


app = Blueprint('auth', __name__, url_prefix="/auth")


@app.route('/cos_temp_credential/', methods=['POST'])
def cos_temp_credential():
    try:
        result = get_cos_temp_credential()
    except (QCloudCOSGetCredentialError) as e:
        return error(str(e.message))

    return ok(result)


@app.route('/sms_auth_code/', methods=['POST'])
def sys_auth_code():
    data = request.get_json() or {}
    phone: str = data.get('phone', '')

    if not phone:
        return error('请输入手机号')

    generate_auth_code(phone=phone)

    return ok()
