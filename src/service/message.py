from fastapi import HTTPException

from src.core.logger import logger
from src.repo import ChatRepository, MessageRepository
from src.schemas import MessageCreate, MessageRead


class MessageService:
    @staticmethod
    def add_message(id: int, message: MessageCreate, db) -> MessageRead:
        logger.debug("Attempting to get chat by id: %s", id)
        chat = ChatRepository.get_chat(id=id, db=db)
        if not chat:
            logger.warning("Requested not existing chat")
            raise HTTPException(404, "Chat not found")

        try:
            logger.debug("Attempting to create message with data: %s", message.text)
            db_message = MessageRepository.add_message(chat_id=id, data=message, db=db)
            logger.info(
                "Message created successfully: %s - %s", db_message.id, db_message.text
            )
            logger.debug("Validating response model")
            response = MessageRead.model_validate(db_message)
            logger.info(
                "Returning MessageRead response for chat %s - %s (message_id = %s)",
                chat.id,
                chat.title,
                db_message.id,
            )
            return response
        except Exception as e:
            MessageRepository.rollback(db=db)
            logger.critical("Failed to create message: {%s}", str(e))
            raise HTTPException(500, f"Failed to create message: {str(e)}") from e
