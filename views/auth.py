from flask import Blueprint
from libs.qcloud import QCloudCOSGetCredentialError
from models.qcloud import get_cos_temp_credential
from views.render import error, ok


app = Blueprint('auth', __name__, url_prefix="/auth")


@app.route('/cos_temp_credential/', methods=['POST'])
def cos_temp_credential():
    try:
        result = get_cos_temp_credential()
    except QCloudCOSGetCredentialError as e:
        return error(str(e))

    return ok(result)
