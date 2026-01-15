from fastapi import HTTPException

from src.core.logger import logger
from src.repo import ChatRepository, MessageRepository
from src.schemas import ChatCreate, ChatRead, MessageRead


class ChatService:
    @staticmethod
    def add_chat(chat: ChatCreate, db) -> ChatRead:
        if len(chat.title.strip()) == 0:
            logger.warning("Attempted to create chat with empty title")
            raise ValueError("Title cannot be empty")

        try:
            logger.debug("Attempting to create chat with data: %s", chat.title)
            db_chat = ChatRepository.add_chat(db=db, data=chat)
            logger.info("Chat created successfully: %s - %s", db_chat.id, db_chat.title)
            logger.debug("Validating response model")
            response = ChatRead.model_validate(db_chat)
            logger.info(
                "New chat created: ChatRead(id=%s, title=%s)", db_chat.id, db_chat.title
            )
            return response
        except Exception as e:
            ChatRepository.rollback(db=db)
            logger.critical("Failed to create chat: {%s}", str(e))
            raise HTTPException(500, f"Failed to create chat: {str(e)}") from e

    @staticmethod
    def get_chat(id: int, limit: int, db) -> ChatRead:
        logger.debug("Attempting to get chat by id: %s", id)
        chat = ChatRepository.get_chat(id=id, db=db)
        if not chat:
            logger.warning("Requested not existing chat")
            raise HTTPException(404, "Chat not found")

        logger.debug("Attempting to get messages from chat %s", chat.title)
        messages = MessageRepository.get_messages_from_chat(
            db=db, chat_id=id, limit=limit
        )
        logger.debug("Validating messages model")
        messages = [MessageRead.model_validate(m) for m in messages]
        logger.debug("Validating response model")
        response = ChatRead(**chat.__dict__, messages=messages)
        logger.info(
            "Returning ChatRead response for chat %s - %s with %d messages (limit=%d)",
            chat.id,
            chat.title,
            len(messages),
            limit,
        )
        return response

    @staticmethod
    def delete_chat(id: int, db) -> None:
        logger.debug("Attempting to get chat by id: %s", id)
        chat = ChatRepository.get_chat(id=id, db=db)
        if not chat:
            logger.warning("Requested not existing chat")
            raise HTTPException(404, "Chat not found")

        try:
            logger.debug("Attempting to delete chat %s", chat.title)
            ChatRepository.delete_chat(chat=chat, db=db)
            logger.info("Chat deleted: id=%s, title=%s", chat.id, chat.title)
            return
        except Exception as e:
            ChatRepository.rollback(db=db)
            logger.critical("Failed to delete chat: {%s}", str(e))
            raise HTTPException(500, f"Failed to delete chat: {str(e)}") from e
