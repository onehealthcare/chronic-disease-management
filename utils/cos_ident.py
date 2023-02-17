from config import QCLOUD_CDM_COS_URL_PATTERN


def get_url_by_ident(ident: str, width: int, height: int) -> str:
    if not ident:
        return ""
    return QCLOUD_CDM_COS_URL_PATTERN.format(ident).replace("#width#x#height#", f"{width}x{height}").format(width, height)
