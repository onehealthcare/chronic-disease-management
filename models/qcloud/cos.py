from models.init_db import qcloud_cos_doc_client, qcloud_cos_user_ident_client
from models.qcloud.const import QCloudCOSCategory
from models.qcloud.exceptions import NotSupportedCategoryError


def get_cos_temp_credential(category: int):
    client = {
        int(QCloudCOSCategory.USER_IDENT): qcloud_cos_doc_client,
        int(QCloudCOSCategory.USER_DOC): qcloud_cos_user_ident_client
    }.get(category)

    if not client:
        raise NotSupportedCategoryError()

    return client.get_temp_credential()
