from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, max_output_tokens=2048)

prompt = ChatPromptTemplate.from_template(
    """
        Write a detailed technical article.

        Topic: {topic}
        Audience: {audience}
        Tone: {tone}
    """
)

chain = prompt | llm | StrOutputParser()

result = chain.invoke({
    "topic": "The benefits of using FastAPI for web development",
    "audience": "Python developers looking to build APIs",
    "tone": "Informative and engaging"
})

print(result)

