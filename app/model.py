from pydantic import BaseModel

class RequestBody(BaseModel):
    prompt: str
    max_length: int = 50