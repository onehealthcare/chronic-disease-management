class RequestException(Exception):
    def __init__(self, message="服务请求失败"):
        self.message = message
