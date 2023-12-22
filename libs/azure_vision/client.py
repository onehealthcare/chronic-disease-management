import requests
from libs.azure_vision.dto import Result
from utils.logging import file_logger as _logger


logger = _logger('libs.azure_vision.client')


class AzureVisionClient:
    def __init__(self, key: str, endpoint: str):
        self.key = key
        self.endpoint = endpoint
        self.analyze_uri = "/computervision/imageanalysis:analyze"
        self.api_version = "2023-02-01-preview"

    def analyze_read_from_img_url(self, img_url: str) -> Result:
        """
        POST https://*.cognitiveservices.azure.com/computervision/imageanalysis:analyze?api-version=2023-02-01-preview&features=read&gender-neutral-caption=False HTTP/1.1
        Host: *.cognitiveservices.azure.com
        Content-Type: application/json
        Ocp-Apim-Subscription-Key: •••

        {
          "url": "string"
        }
        """
        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'HOST': self.endpoint,
            'Content-Type': 'application/json'
        }
        url = f"https://{self.endpoint}{self.analyze_uri}?api-version={self.api_version}&features=read"
        resp = requests.post(url, headers=headers, json={"url": img_url})
        if not resp.ok:
            logger.error(f"analyze_read_by_img_data, error, status_code:{resp.status_code} - resp:{resp.text} - img_url:{img_url}")
            resp.raise_for_status()

        return Result.parse_obj(resp.json())

    def analyze_read_by_img_data(self, img_data: bytes) -> Result:
        if not img_data:
            raise ValueError("img_data is empty")

        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'HOST': self.endpoint,
            'Content-Type': 'application/octet-stream'
        }
        url = f"https://{self.endpoint}{self.analyze_uri}?api-version={self.api_version}&features=read"
        resp = requests.post(url, headers=headers, data=img_data)

        if not resp.ok:
            logger.error(f"analyze_read_from_img_data, error, status_code:{resp.status_code} - resp:{resp.text}")
            resp.raise_for_status()

        return Result.parse_obj(resp.json())
