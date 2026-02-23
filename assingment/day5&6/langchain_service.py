import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class LangChainService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, max_output_tokens=2048)

    def generate_response(self, prompt:str) -> str:
        response = self.llm.invoke(prompt)
        return response