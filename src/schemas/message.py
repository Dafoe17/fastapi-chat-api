from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MessageBase(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=5000,
    )


class MessageRead(MessageBase):
    id: int
    chat_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageCreate(MessageBase):
    pass
