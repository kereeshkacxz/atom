import httpx
import json
import asyncio  # Импортируем asyncio для использования sleep
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
    """
    data = {
        "messages":  messages
    }
    
    headers = {
        "Content-Type": "application/json",
    }
    
    async with httpx.AsyncClient() as client:

        try:
            response = await client.post(url, headers=headers, json=data, timeout=40)
            response.raise_for_status()
        except httpx.ReadTimeout:
            raise HTTPException(status_code=504, detail="Request timed out")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))


    
    try:
        return response.json() 
    except ValueError as e:
        raise HTTPException(status_code=500, detail=e)

async def assayText(user_text: str, requirment_texts: list[str]):
    url = getSettings().URL

    instruction = """
                The data consists of: Requirements and documents.
                You need to match the document to the requirements and understand whether it meets or not
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
            "content": f""" Document:
                {user_text}
            """
        }
    ]

    for text in requirment_texts:
        messages.append(
            {
                "role": "user",
                "content": f""" Requirement:
                    {text}
                """
            }
        )

    # Добавляем задержку в 5 секунд
    await asyncio.sleep(5)

    response = await sendMessage(url, messages)
    
    # # Обработка ответа
    # json_string = response['generated_text']['content'].replace('\n', '').replace('\\', '')
    # data = json.loads(json_string)
    return response
