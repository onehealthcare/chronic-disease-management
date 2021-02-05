class UserNotFoundException(Exception):
    """
    用户不存在
    """
    def __init__(self, message="用户不存在"):
        self.message = message
