from typing import Tuple


class ApiError(object):
    invalid_wxapp_cod: Tuple[int, str] = (1001, "非法的小程序登录代码")
