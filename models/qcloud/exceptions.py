class NotSupportedCategoryError(Exception):
    def __init__(self, message="不支持的类型"):
        self.message = message
