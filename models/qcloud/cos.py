import uuid
from typing import Dict

from models.init_db import qcloud_cos_client


def get_cos_temp_credential() -> Dict[str, str]:
    data = qcloud_cos_client.get_temp_credential()

    return {
        'expired_time': str(data.get('expiredTime')),
        'start_time': str(data.get('startTime')),
        'token': data.get('credentials', {}).get('sessionToken'),
        'secret_id': data.get('credentials', {}).get('tmpSecretId'),
        'secret_key': data.get('credentials', {}).get('tmpSecretKey'),
        'filename_suffix': uuid.uuid1().hex
    }
