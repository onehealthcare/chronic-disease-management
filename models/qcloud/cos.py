from models.init_db import qcloud_cos_client


def get_cos_temp_credential():
    return qcloud_cos_client.get_temp_credential()
