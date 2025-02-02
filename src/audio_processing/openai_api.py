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
            model=config["model"],
            messages=[
                {
                    "role": "system",
                    "content": "You are the Hogwarts Sorting Hat. Analyze student's traits and assign house affinity scores (1-10) for Gryffindor, Hufflepuff, Ravenclaw and Slytherin. Provide poetic reasoning in British English."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "submit_sorting_results",
                        "description": "Finalize house sorting with affinity scores and poetic explanation",
                        "strict": True,
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "hat_response": {
                                    "type": "string",
                                    "description": "The Sorting Hat's poetic assessment in British English (3-5 sentences)"
                                },
                                "gryffindor": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 10,
                                    "description": "Courage, bravery and chivalry score"
                                },
                                "hufflepuff": {
                                    "type": "integer", 
                                    "minimum": 1,
                                    "maximum": 10,
                                    "description": "Loyalty, patience and hard work score"
                                },
                                "ravenclaw": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 10,
                                    "description": "Intelligence, creativity and wisdom score"
                                },
                                "slytherin": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 10,
                                    "description": "Ambition, cunning and resourcefulness score"
                                }
                            },
                            "required": [
                                "hat_response",
                                "gryffindor",
                                "hufflepuff", 
                                "ravenclaw",
                                "slytherin"
                            ],
                            "additionalProperties": False
                        }
                    }
                }
            ],
            stream=False,
            tool_choice="required"
        )
        
        print(response)
        
        # Extract tool call arguments
        tool_call = response.choices[0].message.tool_calls[0]
        result = json.loads(tool_call.function.arguments)
        return result
