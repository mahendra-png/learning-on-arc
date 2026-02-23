from langchain_service import LangChainService

service = LangChainService()
response = service.generate_response("What is FastAPI?")
print(response)
