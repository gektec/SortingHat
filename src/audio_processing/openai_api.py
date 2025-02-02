import openai
from openai import OpenAI
import json
from pydantic import BaseModel

# Might not supported by DeepSeek


class SortingResult(BaseModel):
    hat_response: str
    gryffindor: int
    hufflepuff: int
    ravenclaw: int
    slytherin: int

class OpenAIAPI:
    def __init__(self):
        with open('config/config.json') as f:
            self.config = json.load(f)
        
        self.client = OpenAI(
            api_key=self.config["openai_api_key"],
            base_url=self.config["openai_base_url"]
        )
        self.history = [{
            "role": "system",
            "content": "You are the Hogwarts Sorting Hat. Analyze student's traits and assign house affinity scores (1-10). Provide poetic reasoning in British English."
        }]

    def process_text(self, text: str) -> SortingResult:
        self.history.append({"role": "user", "content": text})
        
        
        completion = self.client.beta.chat.completions.parse(
            model=self.config["model"],
            messages=self.history,
            response_format=SortingResult,
        )
        
        print(completion)
        
        result = completion.choices[0].message.parsed
        
        print(result)
        
        self.history.append({
            "role": "assistant", 
            "content": result.model_dump_json()
        })
        
        return result
