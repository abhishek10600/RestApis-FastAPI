from pydantic import BaseModel
from typing import Optional


class TodoResponse(BaseModel):
    task: str
