from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .message import MessageRead


class ChatBase(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
    )

    @field_validator("title")
    @classmethod
    def strip_title(cls, v: str) -> str:
        return v.strip()


class ChatRead(ChatBase):
    id: int
    messages: List[MessageRead] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatCreate(ChatBase):
    pass
