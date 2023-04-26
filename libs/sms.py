from typing import List

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20210111 import models, sms_client


class QCloudSMSReqError(Exception):
    def __init__(self, message="发送短信失败"):
        self.message = message


class SMSClient:
    def __init__(
        self, secret_id: str,
        secret_key: str,
        sdk_app_id: str,  # 腾讯云短信控制台建的 app
        sign_name: str,  # 后台已经审核过的签名
        template_id: str  # 模板 ID
    ):
        cred = credential.Credential(secret_id, secret_key)
        self.client = sms_client.SmsClient(cred, "ap-beijing")
        self.sdk_app_id = sdk_app_id
        self.sign_name = sign_name
        self.template_id = template_id

    def send_sms(self, phone_numbers: List[str], template_param_set: List[str]) -> models.SendSmsResponse:
        """

        :param phone_numbers:
        :param template_param_set:
        :return:
            {
              "SendStatusSet": [
                {
                  "SerialNo": "3369:152750356316825026452808044",
                  "PhoneNumber": "+8618601980445",
                  "Fee": 1,
                  "SessionContext": "",
                  "Code": "Ok",
                  "Message": "send success",
                  "IsoCode": "CN"
                }
              ],
              "RequestId": "6ca538cf-11f0-49c2-833e-93598d3aeb07"
            }
        """
        req = models.SendSmsRequest()

        # 基本类型的设置:
        # SDK采用的是指针风格指定参数，即使对于基本类型你也需要用指针来对参数赋值。
        # SDK提供对基本类型的指针引用封装函数
        # 帮助链接：
        # 短信控制台: https://console.cloud.tencent.com/smsv2
        # 腾讯云短信小助手: https://cloud.tencent.com/document/product/382/3773#.E6.8A.80.E6.9C.AF.E4.BA.A4.E6.B5.81

        # 短信应用ID: 短信SdkAppId在 [短信控制台] 添加应用后生成的实际SdkAppId，示例如1400006666
        # 应用 ID 可前往 [短信控制台](https://console.cloud.tencent.com/smsv2/app-manage) 查看
        req.SmsSdkAppId = self.sdk_app_id
        # 短信签名内容: 使用 UTF-8 编码，必须填写已审核通过的签名
        # 签名信息可前往 [国内短信](https://console.cloud.tencent.com/smsv2/csms-sign)
        # 或 [国际/港澳台短信](https://console.cloud.tencent.com/smsv2/isms-sign) 的签名管理查看
        req.SignName = self.sign_name
        # 模板 ID: 必须填写已审核通过的模板 ID
        # 模板 ID 可前往 [国内短信](https://console.cloud.tencent.com/smsv2/csms-template)
        # 或 [国际/港澳台短信](https://console.cloud.tencent.com/smsv2/isms-template) 的正文模板管理查看
        req.TemplateId = self.template_id
        # 模板参数: 模板参数的个数需要与 TemplateId 对应模板的变量个数保持一致，，若无模板参数，则设置为空
        req.TemplateParamSet = template_param_set
        # 下发手机号码，采用 E.164 标准，+[国家或地区码][手机号]
        # 示例如：+8613711112222， 其中前面有一个+号 ，86为国家码，13711112222为手机号，最多不要超过200个手机号
        req.PhoneNumberSet = phone_numbers
        # 用户的 session 内容（无需要可忽略）: 可以携带用户侧 ID 等上下文信息，server 会原样返回
        req.SessionContext = ""
        # 短信码号扩展号（无需要可忽略）: 默认未开通，如需开通请联系 [腾讯云短信小助手]
        req.ExtendCode = ""
        # 国际/港澳台短信 senderid（无需要可忽略）: 国内短信填空，默认未开通，如需开通请联系 [腾讯云短信小助手]
        req.SenderId = ""

        try:
            resp: models.SendSmsResponse = self.client.SendSms(req)
            return resp
        except TencentCloudSDKException as e:
            raise QCloudSMSReqError(e.get_message())
