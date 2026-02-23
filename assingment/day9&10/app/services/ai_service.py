import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_embedding(self, context: str, question: str) -> str:
        prompt = f"""
You are a helpful assistant, Answer the question only using the provided context. If the answer is not in the context, say you don't know.
Context: {context}
Question: {question}
"""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content