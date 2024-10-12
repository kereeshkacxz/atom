import requests
import json
from app.config import getSettings

async def sendMessage(api_key, url, instruction, temperature, messages):
    """
    Отправляет сообщение через API.
    
    Args:
        api_key (str): API-ключ.
        url (str): URL API-endpoint.
        instruction (str): Инструкция для API.
        temperature (float): Температура для генерации ответа.
        messages (list): Список сообщений в формате, ожидаемом API.
    
    Returns:
        dict: Ответ API.
    """
    data = {
        "instruction": instruction,
        "temperature": temperature,
        "messages": messages
    }
    
    headers = {
        "x-api-key": api_key
    }
    
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    
    return response.json()

async def assayText(user_text: str, requirment_text: str):
    api_key = getSettings().API_KEY
    url = getSettings().URL

    instruction = """
                Я имею документацию и требования к ней, мне нужно проверить,
                соответсвует ли документация требованиям. Выведи результат в формате JSON.
                Формат ответа:
                {
                    "result": "Требования соответсвуют" или "Требования не соответсвуют",
                    "description": "Описание",
                }
            """

    messages = [
        {
            "role": "user",
            "content": instruction
        },
        {
            "role": "user",
            "content": f""" Документация:
                {user_text}
            """
        },
        {
            "role": "user",
            "content": f""" Требования:
                {requirment_text}
            """
        }
    ]

    response = await sendMessage(api_key, url, '', 0.1, messages)
    json_string = response['content'][0]['text'].replace('\n', '').replace('\\', '')
    data = json.loads(json_string)
    return data

