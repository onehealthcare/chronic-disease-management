class DocPackageNotFoundException(Exception):
    def __init__(self, message="Doc Package 不存在"):
        self.message = message


class DocPackageIdentNotFoundException(Exception):
    def __init__(self, message="Doc Package Ident 不存在"):
        self.message = message


class MetricNotFoundException(Exception):
    def __init__(self, message="Metric 不存在"):
        self.message = message


class DuplicatedMetricException(Exception):
    def __init__(self, message="Metric 已存在"):
        self.message = message


class MetricLabelNotFoundException(Exception):
    def __init__(self, message="Metric Label 不存在"):
        self.message = message
