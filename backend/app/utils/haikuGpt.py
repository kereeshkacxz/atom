import requests
import json
import re
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
        "messages": messages,
    }
    
    headers = {
        "x-api-key": api_key
    }
    
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    
    return response.json()
async def assayText(user_text: str, requirment_texts: list[str]):
    api_key = getSettings().PROXY_API_KEY
    url = getSettings().URL

    instruction = """
                The data consists of two input artifacts: certification regulations and a development requirement.
                The regulations are described for each regulatory object, and the requirement for the system.
                It is necessary to check whether the requirements comply with the certification regulations.
                Output the result in JSON format.
                Response format:
                {
                    "result": "Do not match" or "Match",
                    "description": "Description",
                }
            """

    messages = [
        {
            "role": "user",
            "content": instruction
        },
        {
            "role": "user",
            "content": f""" development requirement:
                {user_text}
            """
        }
    ]

    for text in requirment_texts:
        messages.append(
            {
                "role": "user",
                "content": f""" certification regulation:
                    {text}
                """
            }
        )
    response = await sendMessage(api_key, url, '', 0.1, messages)
    text = response['content'][0]['text']

    # Использование регулярного выражения для извлечения JSON
    json_match = re.search(r'\{.*?\}', text, re.DOTALL)
    json_string = json_match.group(0).replace('\n', '').replace('\\', '')
    data = json.loads(json_string)
    return data