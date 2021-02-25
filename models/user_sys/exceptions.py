class UserNotFoundException(Exception):
    """
    用户不存在
    """
    def __init__(self, message="用户不存在"):
        self.message = message


class UserAuthNotFoundException(Exception):
    """
    用户 Auth 不存在
    """
    def __init__(self, message="用户 Auth 不存在"):
        self.message = message


class DuplicatedUserNameError(Exception):
    def __init__(self, message="存在同名用户"):
        self.message = message
