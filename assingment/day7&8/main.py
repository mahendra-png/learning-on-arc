from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from services.vision_service import VisionService
from services.multi_model_service import MultiModelService
from enum import Enum

app = FastAPI()

# valid_models = ["gemini", "openai"]

class ModelType(str, Enum):
    gemini = "gemini"
    openai = "openai"



MultimodalService = MultiModelService()
VisionService = VisionService()

@app.get("/generate")
def generate(prompt:str, model: ModelType = ModelType.gemini):
    result = MultimodalService.generate_response(prompt, model)
    return {"response": result}

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...), prompt: str = Form("Describe this image")):
    image_data = await file.read()
    result = VisionService.analyze(image_data, prompt)
    return {"response": result}