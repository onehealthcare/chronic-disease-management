class DocPackageNotFoundException(Exception):
    def __init__(self, message="不存在"):
        self.message = message
