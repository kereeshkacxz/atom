from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
import os

def train_model(data_path):
    # Загрузка данных
    dataset = load_dataset('text', data_files=os.path.join(data_path, '*.txt'))

    # Инициализация модели и токенизатора
    model_name = "meta-llama/Llama-3.2-11B-Vision-Instruct" 
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Подготовка данных для обучения
    def tokenize_function(examples):
        return tokenizer(examples['text'], truncation=True, padding='max_length', max_length=512)

    tokenized_dataset = dataset.map(tokenize_function, batched=True)

    # Удаляем ненужные колонки
    tokenized_dataset = tokenized_dataset.remove_columns(["text"])
    tokenized_dataset.set_format("torch")

    # Настройка параметров обучения
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=4,
        save_steps=10_000,
        save_total_limit=2,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset['train'],  # Используем обучающую часть датасета
    )

    trainer.train()
    model.save_pretrained('./model')  # Сохранение обученной модели
    tokenizer.save_pretrained('./model')

# Пример вызова функции
if __name__ == "__main__":
    train_model('/data')  # Укажите путь к директории с вашими текстовыми файлами
