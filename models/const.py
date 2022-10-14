from enum import IntEnum


class CommonStatus(IntEnum):
    NORMAL: int = 0
    INIT: int = 1
    DELETED: int = 2


class Role:
    BITS_ROLE_ADMIN = 0b1
    BITS_ROLE_EDITOR = 0b10
    BITS_ROLE_VIDEO_PROVIDER = 0b100


class ColorEnum:
    NORMAL = "#91CB74"
    WARN = "#EE6666"
