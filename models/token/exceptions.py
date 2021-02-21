class InvalidTokenError(Exception):
    def __init__(self, message="非法 token"):
        self.message = message
