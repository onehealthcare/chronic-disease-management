import base64
from typing import List, Tuple


def get_next_cursor(results: List, size: int) -> Tuple[List, str]:
    next_cursor: str = ''
    if len(results) > size:
        next_cursor = base64.b64encode(str(results[-1].id).encode('utf-8')).decode('utf-8')
        results = results[0: -1]

    return results, next_cursor
