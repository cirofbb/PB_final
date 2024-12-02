from pydantic import BaseModel
from typing import List, Dict, Union

class Message(BaseModel):
    role: str
    content: str

class ChatModel(BaseModel):
    messages: List[Message]

class ChatResponseModel(BaseModel):
    response: str