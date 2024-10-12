from fastapi import FastAPI, HTTPException
from uvicorn import run
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

from model import RequestBody
from train import train_model as train_model_func  # Изменено имя для избежания конфликта

app = FastAPI()

# Загрузка модели и токенизатора
model_name = "model"  # Убедитесь, что это правильный путь к сохраненной модели

# Проверяем, существует ли модель
if not os.path.exists(model_name):
    print("Модель не найдена. Начинаем обучение...")
    # Запускаем обучение модели
    train_model_func('/data')  # Укажите путь к директории с вашими текстовыми файлами
    print("Обучение завершено.")

# Теперь загружаем модель и токенизатор
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

@app.post("/generate/")
def generate_text(request: RequestBody):
    inputs = tokenizer(request.prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=request.max_length)
    return {"generated_text": tokenizer.decode(outputs[0], skip_special_tokens=True)}

@app.post("/train/")
def train_model_endpoint():  # Изменено имя функции для избежания конфликта
    # Проверяем, существует ли директория с данными
    if not os.path.exists('/data'):
        raise HTTPException(status_code=404, detail="Data path not found")

    # Запускаем обучение модели
    train_model_func('/data')  # Вызов функции обучения

    # После обучения загружаем обновленную модель
    global tokenizer, model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    return {"message": "Model trained successfully"}

# Пример вызова функции
if __name__ == "__main__":
    run(
        "__main__:app",
        port=8000,
        reload=True,
        reload_dirs=["app", "tests"],
        log_level="debug",
        host='0.0.0.0',  # Изменено на '0.0.0.0' для доступа извне
    )
