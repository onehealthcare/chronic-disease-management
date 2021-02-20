from enum import IntEnum


class UserAuthProvider(IntEnum):
    WXAPP: int = 1
    WEIBO: int = 2
    GOOGLE: int = 3
    GITHUB: int = 4
