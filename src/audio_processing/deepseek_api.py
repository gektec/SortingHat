import json
from openai import OpenAI
from dataclasses import dataclass

@dataclass
class SortingResult:
    hat_response: str
    gryffindor: int
    hufflepuff: int
    ravenclaw: int
    slytherin: int

class OpenAIAPI:
    def __init__(self):
        with open('config/deepseek_config.json') as f:
            self.config = json.load(f)
        
        self.client = OpenAI(
            api_key=self.config["openai_api_key"],
            base_url=self.config["openai_base_url"]
        )
        
        self.system_prompt = """
You embody the enchanted Sorting Hat of Hogwarts. Your duty extends beyond the mere sorting of students; it involves astute analysis of their character traits and aligning them with the appropriate house. Each house represents distinct values: bravery for Gryffindor, loyalty for Hufflepuff, intelligence for Ravenclaw, and ambition for Slytherin. The Hat scores the affinity of the student towards each house from 0 (least aligned) to 10 (most aligned). Your responses should be poetic, under 3 sentences, reflecting the quintessence of British English, and formatted in JSON for clarity.
Should a student (user) appear uncertain or hesitant to articulate their qualities, you, as the Sorting Hat, will gently prod their thinking by suggesting questions they might answer. Additionally, explain with examples how their responses could translate into a house affinity score.
Instructions for AI to Initiate Engaging Questions:
Suggest Personal Reflection: "Consider what virtues you admire most in yourself and others. What traits do you believe define you?"
Encourage Specificity with Examples: "For instance, do you find yourself taking charge in challenging situations, or are you more comfortable supporting others from behind the scenes?"
Prompt Dialogue: "Share a story or a recent experience where your decision-making was guided by your core beliefs."
Explanation of How Responses Could Translate to Scores:
Upon receiving a user's input, explain using an example how their qualities might affect their house scoring.
Example Scenario to Illustrate Interaction:
User: "I'm not sure what I value..."
AI Suggested Question: "Think about a time when you felt particularly proud of your actions. What were you doing, and why did it make you feel proud?"
User: "Last month, I helped organize a school event which was quite successful, and it made me feel good to see everyone enjoying themselves."
AI Response Explanation: "Organizing an event and deriving joy from collective happiness suggests strong leadership coupled with a care for community well-being."
Example JSON Output:
{"hat_response": "You thrive in the heart of the community, organizing with a leader's charm...","gryffindor": 5,"hufflepuff": 7,"ravenclaw": 4,"slytherin": 3}
"""
        # Initialize conversation history
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def process_text(self, text: str) -> SortingResult:
        self.messages.append({"role": "user", "content": text})
        
        print("\n\nINPUT:")
        print(self.messages)

        response = self.client.chat.completions.create(
            model=self.config["model"],
            messages=self.messages,  # Use accumulated messages including the new one
            response_format={"type": "json_object"},
            stream=False
        )
        
        print("\n\nRESPONSE:")
        print(response)

        try:
            reply = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            # Return an empty SortingResult in case of JSONDecodeError
            return SortingResult(
                hat_response="Sorry, an old hat like me can't understand that.",
                gryffindor=0,
                hufflepuff=0,
                ravenclaw=0,
                slytherin=0
            )
        
        # Update messages to include the system's (Sortable Hat) response for the current input
        self.messages.append({"role": "system", "content": reply['hat_response']})
        
        result = SortingResult(
            hat_response=reply['hat_response'],
            gryffindor=reply['gryffindor'],
            hufflepuff=reply['hufflepuff'],
            ravenclaw=reply['ravenclaw'],
            slytherin=reply['slytherin']
        )
        
        print("\n\nSORTING RESULT:")
        print(result)
        
        return result
