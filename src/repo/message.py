from typing import List

from sqlalchemy.orm import Session

from src.models import Message


class MessageRepository:
    @staticmethod
    def get_messages_from_chat(db: Session, chat_id: int, limit: int) -> List[Message]:
        messages = (
            db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
            .all()
        )

        messages.reverse()
        return messages

    @staticmethod
    def add_message(db: Session, chat_id: int, data) -> Message:
        message = Message(**data.model_dump(), chat_id=chat_id)
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    @staticmethod
    def rollback(db: Session) -> None:
        db.rollback()
        return None
