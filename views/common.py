from typing import Tuple


class ApiError(object):
    login_needed: Tuple[int, str] = (1000, "需要登录")
    invalid_wxapp_code: Tuple[int, str] = (1001, "非法的小程序登录代码")
