import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

class BlogPost(BaseModel):
    title: str = Field(description="The title of the blog post")
    content: str = Field(description="The content of the blog post")
    tags: list[str] = Field(description="A list of tags related to the blog post")

parser = JsonOutputParser(pydantic_object=BlogPost)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, max_output_tokens=2048)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Generate a blog structure. {format_instructions}"),
    ("human", "Topic: {topic}")
])

chain = prompt | llm | parser

result = chain.invoke({
    "topic": "The benefits of using FastAPI for web development",
    "format_instructions": parser.get_format_instructions()
})

print(result)
