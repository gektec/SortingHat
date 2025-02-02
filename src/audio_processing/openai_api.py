import openai
from openai import OpenAI
import json

class OpenAIAPI:
    def __init__(self):
        with open('config/config.json') as f:
            config = json.load(f)
        self.openai = OpenAI(api_key=config["openai_api_key"], base_url=config["openai_base_url"])

    def process_text(self, text):
        with open('config/config.json') as f:
            config = json.load(f)
        response = self.openai.chat.completions.create(
            model=config["model"],  # 选择合适的模型
            messages=[
                {"role": "user", "content": f"This is a test：\n{text}"},
            ],
            stream=False
        )
        return response.choices[0].message.content.strip()
