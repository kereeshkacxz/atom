import os
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling

# Установка переменной окружения для управления памятью
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# Инициализация FastAPI
app = FastAPI()

# Загрузка модели
model_id = "meta-llama/Llama-3.2-3B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.float16,  # Используйте float16 для уменьшения использования памяти
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

    # Очистка кэша CUDA
    torch.cuda.empty_cache()

    try:
        with torch.no_grad():  # Отключение отслеживания градиентов
            outputs = pipe(
                message_list,
                max_new_tokens=256,
            )
        generated_text = outputs[0]["generated_text"][-1]
        return {"generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def load_dataset(file_paths):
    # Загрузка текстовых файлов в один датасет
    return TextDataset(
        tokenizer=pipe.tokenizer,
        file_path=file_paths,
        block_size=128,  # Размер блока для обучения
    )

def train_model(dataset):
    training_args = TrainingArguments(
        output_dir="./results",
        overwrite_output_dir=True,
        num_train_epochs=1,
        per_device_train_batch_size=2,
        save_steps=10_000,
        save_total_limit=2,
    )

    data_collator = DataCollatorForLanguageModeling(tokenizer=pipe.tokenizer, mlm=False)

    trainer = Trainer(
        model=pipe.model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
    )

    trainer.train()

if __name__ == "__main__": 
    directory = './data'

    file_paths = []

    for filename in os.listdir(directory):
        full_path = os.path.join(directory, filename)
        
        if os.path.isfile(full_path):
            file_paths.append(full_path)
    dataset = load_dataset(file_paths)

    # Обучение модели
    train_model(dataset)

    # Запуск FastAPI
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
