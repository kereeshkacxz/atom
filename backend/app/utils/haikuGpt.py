import httpx
import json
import asyncio
from app.config import getSettings
from fastapi import HTTPException

async def sendMessage(url, messages):
    """
    Отправляет сообщение через API.
    
    Args:
        url (str): URL API-endpoint.
        messages (list): Список сообщений в формате, ожидаемом API.
    
    Returns:
        dict: Ответ API.
    
    Raises:
        httpx.HTTPStatusError: Если ответ имеет статус ошибки.
        ValueError: Если ответ не может быть преобразован в JSON.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {getSettings().PROXY_API_KEY}",  # Убедитесь, что у вас есть ключ API
        "Anthropic-Version": "2023-06-01"  # Версия API
    }

    data = {
        "model": "claude-3-opus-20240229",  # Укажите модель
        "messages": messages,
        "max_tokens": 1024  # Укажите максимальное количество токенов
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()  # Проверка на статус ошибки
        except httpx.HTTPStatusError as e:
            # Обработка ошибки HTTP
            raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error occurred: {e.response.status_code} - {e.response.text}") from e
        except Exception as e:
            # Обработка других исключений
            raise HTTPException(status_code=500, detail=f"Error occurred: {e}") from e
    
    try:
        return response.json()  # Преобразование ответа в JSON
    except ValueError as e:
        raise HTTPException(status_code=500, detail="Error parsing response") from e

async def assayText(user_text: str, requirment_texts: list[str]):
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
            "role": "system",
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

    # Добавляем задержку в 5 секунд
    await asyncio.sleep(5)

    response = await sendMessage(url, messages)
    
    # Обработка ответа
    json_string = response['completion']  # Измените на правильный ключ для ответа
    data = json.loads(json_string)
    return data
