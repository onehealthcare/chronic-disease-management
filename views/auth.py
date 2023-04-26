from broker.sms import send_wxapp_login_sms
from flask import Blueprint, request
from libs.qcloud import QCloudCOSGetCredentialError
from libs.sms import QCloudSMSReqError
from models.qcloud import get_cos_temp_credential
from models.sms_sys import generate_and_send_auth_code
from views.render import error, ok


app = Blueprint('auth', __name__, url_prefix="/auth")


@app.route('/cos_temp_credential/', methods=['POST'])
def cos_temp_credential():
    try:
        result = get_cos_temp_credential()
    except QCloudCOSGetCredentialError as e:
        return error(str(e.message))

    return ok({'credential': result})


@app.route('/sms_auth_code/', methods=['POST'])
def sys_auth_code():
    data = request.get_json() or {}
    phone: str = data.get('phone', '')

    if not phone:
        return error('请输入手机号')

    code: str = generate_and_send_auth_code(phone=phone)
    try:
        ret, msg = send_wxapp_login_sms(country_code="86", phone_number=phone, code=code, expires_mins=5)
        if not ret:
            return error(f"短信发送失败：{msg}")
    except QCloudSMSReqError as e:
        return error(f"短信发送失败: {e.message}")

    return ok()
