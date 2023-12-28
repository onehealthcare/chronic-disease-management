"""
Note: The openai-python library support for Azure OpenAI is in preview.
Note: This code sample requires OpenAI Python library version 0.28.1 or lower.
"""

import requests
from libs.openai.dto import Result


class OpenAIClient:
    def __init__(self, api_type: str, api_base: str, api_engine: str, api_version: str, api_key: str, timeout: int = 2):
        self.api_type = api_type
        self.api_base = api_base
        self.api_engine = api_engine
        self.api_version = api_version
        self.api_key = api_key
        self.timeout = timeout
        self.url = f"{self.api_base}openai/deployments/{self.api_engine}/chat/completions?api-version={self.api_version}"

    def chat(self, messages):
        """
        messages = [{
            "role": "system",
            "content": "Assistant is an AI chatbot that helps users turn a natural language list into JSON format. After users input a list they want in JSON format,   it will provide suggested list of attribute labels if the user has not provided any, then ask the user to confirm them before creating the list."
        }, {
            "role": "user", "content": '''
                格式化下面的消息，使用 json 返回，除了 json 信息外不需要其他的话：
                参数设置√\n· 胶片模拟: NC\n· 白平衡:R2 B-2\n· 色彩效果:强\n·\n动态范围:400%\n高光色调 :- 1\n· 阴影色调 :- 1\n· 锐度:+2\n测光模式:中央重点
                json 的格式为：
                {
                    "film_simulation": "value_placeholder",
                    "dynamic_range": "value_placeholder",
                    "grain_effect": "value_placeholder",
                    "color_chrome_effect": "value_placeholder",
                    "color_chrome_effect_blue": "value_placeholder",
                    "white_balance": "value_placeholder",
                    "highlight": "value_placeholder",
                    "shadow": "value_placeholder",
                    "color": "value_placeholder",
                    "sharpness": "value_placeholder",
                    "noise_reduction": "value_placeholder",
                    "clarity": "value_placeholder",
                    "iso": "value_placeholder",
                    "exposure_compensation": "value_placeholder"
                }
                如果没有对应的 value，请用 - 替代。\n那么 JSON 对象是:
            '''
        }]
      :param messages:
      :return:
      """
        headers = {
            'api-key': self.api_key,
            'Content-Type': 'application/json'
        }
        json_data = {
            'messages': messages,
            "max_tokens": 2048,
            "temperature": 0.2,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "top_p": 0.95,
            # "response_format": {"type": "json_object"}
        }
        resp = requests.post(self.url, headers=headers, json=json_data, timeout=self.timeout)
        if not resp.ok:
            # log
            resp.raise_for_status()

        return Result.parse_obj(resp.json())
