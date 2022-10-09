from typing import Tuple


class ApiError:
    invalid_api_sign: Tuple[int, str] = (403, "非法请求")
    access_denied: Tuple[int, str] = (403, "没有权限")
    login_needed: Tuple[int, str] = (1000, "需要登录")
    invalid_wxapp_code: Tuple[int, str] = (1001, "非法的小程序登录代码")
    admin_needed: Tuple[int, str] = (1002, "没有管理员权限")
    invalid_token: Tuple[int, str] = (1003, "token 无效")

    invalid_cursor: Tuple[int, str] = (2001, "无效的 cursor")
    invalid_sms_auth_code: Tuple[int, str] = (3001, "验证码无效")
