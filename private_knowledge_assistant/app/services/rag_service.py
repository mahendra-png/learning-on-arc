from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

class RAGServices:
    def __init__(self):
        self.client = genai.Client(
            api_key = os.getenv("GEMINI_API_KEY")
        )
        # self.model = genai.GenerativeModel("gemini-1.5-flash")
        
    def generte(self, context, question):
        prompt = f"""
        Answer only from the contaxt below,
        If answer not found, say 'not found in document.'
        Context : {context} 
        Question: {question}
        """
        response = self.client.models.generate_content(
            model = "models/gemini-2.5-flash",
            contents = prompt)
        return response.text
