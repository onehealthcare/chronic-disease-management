class InvalidAuthCodeError(Exception):
    def __init__(self, message="无效的 auth code"):
        self.message = message
