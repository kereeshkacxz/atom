import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

# Инициализация FastAPI
app = FastAPI()

# Загрузка модели
model_id = "meta-llama/Llama-3.2-3B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

class Message(BaseModel):
    role: str
    content: str

class RequestData(BaseModel):
    messages: list[Message]


@app.post("/generate/")
async def generate_text(request_data: RequestData):
    if not request_data.messages:
        raise HTTPException(status_code=400, detail="Messages list cannot be empty.")
    
    message_list = [{"role": message.role, "content": message.content} for message in request_data.messages]

    try:
        outputs = pipe(
            message_list,
            max_new_tokens=256,
        )
        generated_text = outputs[0]["generated_text"][-1]
        return {"generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
