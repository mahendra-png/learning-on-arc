from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class NoteAnalysis(BaseModel):
    summary: str = Field(description="A brief summary of the note")
    sentiment: str = Field(description="The overall sentiment of the note, e.g., positive, negative, neutral")
    keywords: list[str] = Field(description="A list of important keywords extracted from the note")

parser = JsonOutputParser(pydantic_object=NoteAnalysis)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, max_output_tokens=2048)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant that analyzes notes. {format_instructions}"),
    ("human", "Please analyze the following note: {note}")
])

chain = prompt | llm | parser

note = "Today I learned about FastAPI. It's a modern web framework for building APIs with Python. I found it really easy to use and it has great performance. I'm excited to use it in my next project!"

result = chain.invoke({
    "note": note,
    "format_instructions": parser.get_format_instructions()
})

print(result)
