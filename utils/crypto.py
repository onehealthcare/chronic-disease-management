import hashlib
import hmac
from typing import Dict, List

from config import API_SECRET


def _dict_to_str(data: Dict):
    keys: List[str] = list(data.keys())
    params: List[str] = []

    for key in sorted(keys):
        if key == 'sign':
            continue

        value = data[key]
        params.append(f"{key}={value}")

    return '&'.join(params)


def hmac_sha1_encode(data: Dict):
    msg: str = _dict_to_str(data)
    return hmac.new(API_SECRET.encode('utf-8'), msg.encode('utf-8'), hashlib.sha1).hexdigest()
