from typing import Tuple

from models.init_db import wxapp_sms_login_client
from models.redis.api import send_code_freq_limit
from tencentcloud.sms.v20210111.models import SendSmsResponse, SendStatus


def send_wxapp_login_sms(
    country_code: str, phone_number: str, code: str, expires_mins: int = 5
) -> Tuple[bool, str]:
    """
    send_wxapp_login_sms("86", "18601980445", "233445", "2")
    :param country_code: 国家码，不带+号
    :param phone_number:
    :param code: 验证码
    :param expires_mins: expires_mins 分钟后有效
    :return:
    """
    ret = False
    msg = "获取回执失败"
    cnt: int = send_code_freq_limit(phone_number)  # 次数
    if cnt:
        return ret, f"频率过快，请 {cnt} 分钟后重试"

    full_phone_number: str = f"+{country_code}{phone_number}"
    resp: SendSmsResponse = wxapp_sms_login_client.send_sms([full_phone_number], [code, str(expires_mins)])
    send_status: SendStatus
    for send_status in resp.SendStatusSet:
        if send_status.PhoneNumber == full_phone_number:
            if send_status.Code == "Ok":
                ret = True
                msg = ""
            else:
                msg = send_status.Message

    return ret, msg
