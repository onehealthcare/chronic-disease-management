class AccessDeniedError(Exception):
    def __init__(self, message="没有权限"):
        self.message = message
