import simplejson
from sts.sts import Sts
from utils.logging import logger as _logger


logger = _logger('labs.qcloud')


class QCloudCOSGetCredentialError(Exception):
    def __init__(self, message="获取临时密钥失败"):
        self.message = message


class QCloudCOSClient(object):
    def __init__(self,
                 secret_id, secret_key,
                 bucket, region, allow_prefix,
                 allow_actions=[
                     'name/cos:PutObject',
                     # 简单上传
                     'name/cos:PostObject',
                     # 分片上传
                     'name/cos:InitiateMultipartUpload',
                     'name/cos:ListMultipartUploads',
                     'name/cos:ListParts',
                     'name/cos:UploadPart',
                     'name/cos:CompleteMultipartUpload'
                 ]):
        """
            说明
            'url': 'https://sts.tencentcloudapi.com/',
            'domain': 'sts.tencentcloudapi.com',
            # 临时密钥有效时长，单位是秒
            'duration_seconds': 1800,
            'secret_id': os.environ['COS_SECRET_ID'],
            # 固定密钥
            'secret_key': os.environ['COS_SECRET_KEY'],
            # 设置网络代理
            # 'proxy': {
            #     'http': 'xx',
            #     'https': 'xx'
            # },
            # 换成你的 bucket
            'bucket': 'example-1253653367',
            # 换成 bucket 所在地区
            'region': 'ap-guangzhou',
            # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径

            # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
            'allow_prefix': 'exampleobject',
            # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
            'allow_actions': [
                # 简单上传
                'name/cos:PutObject',
                'name/cos:PostObject',
                # 分片上传
                'name/cos:InitiateMultipartUpload',
                'name/cos:ListMultipartUploads',
                'name/cos:ListParts',
                'name/cos:UploadPart',
                'name/cos:CompleteMultipartUpload'
            ],
        """
        self.url = 'https://sts.tencentcloudapi.com/'
        self.domain = 'sts.tencentcloudapi.com'
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.bucket = bucket
        self.region = region
        self.allow_prefix = allow_prefix
        self.allow_actions = allow_actions

    def get_temp_credential(self, duration_seconds=1800):
        config = {
            'url': self.url,
            'domain': self.domain,
            # 临时密钥有效时长，单位是秒
            'duration_seconds': duration_seconds,
            'secret_id': self.secret_id,
            'secret_key': self.secret_key,
            'bucket': self.bucket,
            'region': self.region,
            'allow_prefix': self.allow_prefix,
            'allow_actions': self.allow_actions,
        }
        logger.info(f'get_credential,request,{simplejson.dumps(config)}')
        try:
            sts = Sts(config)
            res = sts.get_credential()
        except Exception as e:
            logger.error(f'get_credential,error,{str(e)}')
            raise QCloudCOSGetCredentialError()

        return res
