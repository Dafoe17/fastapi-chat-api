from sqlalchemy.orm import Session

from src.models import Chat


class ChatRepository:
    @staticmethod
    def get_chat(db: Session, id: int) -> Chat | None:
        return db.query(Chat).filter(Chat.id == id).first()

    @staticmethod
    def add_chat(db: Session, data) -> Chat:
        chat = Chat(**data.model_dump())
        db.add(chat)
        db.commit()
        db.refresh(chat)
        return chat

    @staticmethod
    def delete_chat(db: Session, chat: Chat) -> None:
        db.delete(chat)
        db.commit()
        return

    @staticmethod
    def rollback(db: Session) -> None:
        db.rollback()
        return None
