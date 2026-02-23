import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# print("APi Key:", os.getenv("GOOGLE_API_KEY"))


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, max_output_tokens=2048)

prompt = ChatPromptTemplate.from_template(
    "You are a helpful assistant. {input}"
)

chain = prompt | llm | StrOutputParser()

result = chain.invoke({"input": "What is FastAPI?"})

print(result)
