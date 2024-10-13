import requests
import json
import re
import ast

from app.config import getSettings
from fastapi import HTTPException

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

async def textFormat(user_text: str, pattern_text: str, api_key: str | None):
    if api_key is None:
        api_key = getSettings().PROXY_API_KEY

    url = getSettings().URL

    messages = [
        {
            "role": "user",
            "content": """ 
                It is necessary to convert the text according to the template.
                Perhaps some fields are missing, bring the text to the template as best you can
                DO NOT INVENT TOO MUCH""",
        },
        {
            "role": "user",
            "content": f""" text:
                {user_text}
            """
        },
        {
            "role": "user",
            "content": f""" template:
                {pattern_text}
            """
        }
    ]

    response = await sendMessage(api_key, url, '', 0.1, messages)
    text = response['content'][0]['text']

    return text

async def assayText(user_text: str, requirment_texts: list[str], api_key: str | None):
    if api_key is None:
        api_key = getSettings().PROXY_API_KEY
    url = getSettings().URL

    instruction = """
                The data consists of two input artifacts: certification regulations and a development requirement.
                The regulations are described for each regulatory object, and the requirement for the system.
                It is necessary to check whether the requirements comply with the certification regulations.
                Output the result in JSON format.
                The result of the algorithm should be a comment on each processed development case. Comments can be of the following types (type 1/2/3):
                The system under development does not belong to the certified ones. No verification is required.
                The certified facilities are mentioned in the case, the regulations are followed. It is necessary to note the regulations that affect this development case.
                The case mentions certified objects that are subject to certification restrictions, but they are not described in the case. It is necessary to supplement the case with a description of the restrictions from the regulations.
                The case mentions certified facilities, the requirement for development contradicts (does not comply with) the certification regulations. Adjustments need to be made.
                The types can be found below.
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
    if not json_match.group(0):
        messages = [
            {
                "role": "user",
                "content": """Convert this message to a json of this type:
                    {
                        "result": "Do not match" or "Match",
                        "description": "Description",
                    }"""
            },
            {
                "role": "user",
                "content": f""" message:
                    {text}
                """
            }
            
        ]
        response = await sendMessage(api_key, url, '', 0.1, messages)
        text = response['content'][0]['text']
        json_match = re.search(r'\{.*?\}', text, re.DOTALL)
    try:
        json_string = json_match.group(0).replace('\n', '').replace('\\', '').replace('"', "'")
        data = ast.literal_eval(json_string)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"JSON decode error: {str(e)}. Response: {json_string}")
    return data
