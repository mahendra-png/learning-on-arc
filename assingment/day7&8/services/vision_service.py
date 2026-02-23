import os
import base64
from dotenv import load_dotenv
from google import genai 
from google.genai import types


load_dotenv()   

class VisionService:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    def analyze(self, image_data: bytes, prompt: str = "Describe this image"):
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents = [
                prompt,
                types.Part.from_bytes(
                    data=image_data,
                    mime_type="image/jpeg"
                )
            ]
        )   

        return response.text   
        