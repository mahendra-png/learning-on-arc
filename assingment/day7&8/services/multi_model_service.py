import os 
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

class MultiModelService:
    def __init__(self):
        self.models = {
            "gemini": ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, max_output_tokens=2048),
            "gpt-4": ChatOpenAI(model="gpt-4"),
            "gpt-3.5": ChatOpenAI(model="gpt-3.5-turbo")
        }
    
    def generate_response(self,prompt: str,  model_name: str = "gemini"):
        llm = self.models.get(model_name)

        if not llm:
            raise ValueError(f"Model '{model_name}' not found. Available models: {list(self.models.keys())}")
        
        chain = (
            ChatPromptTemplate.from_template("{p}")
            | llm
            | StrOutputParser()
        )
        return chain.invoke({"p": prompt})


