from fastapi import APIRouter, Depends, Query, status

from src.api.dependencies import Session, get_db
from src.core.logger import logger
from src.schemas import ChatCreate, ChatRead, MessageCreate, MessageRead
from src.service import ChatService, MessageService

router = APIRouter(prefix="/chats", tags=["💬 Chats"])


@router.post("/", response_model=ChatRead, operation_id="add-chat")
def add_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    logger.info("Attempting to add new chat '%s'", chat.title)
    return ChatService.add_chat(chat=chat, db=db)


@router.post("/{id}/messages/", response_model=MessageRead, operation_id="add-message")
def add_message(id: int, message: MessageCreate, db: Session = Depends(get_db)):
    logger.info("Attempting to add new message '%s' in chat [%s]", message.text, id)
    return MessageService.add_message(id=id, message=message, db=db)


@router.get("/{id}", response_model=ChatRead, operation_id="get-chat-with-messages")
def get_chat(
    id: int, limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)
):
    logger.info("Attempting to get messages in chat [%s]", id)
    return ChatService.get_chat(id=id, limit=limit, db=db)


@router.delete(
    "/{id}", status_code=status.HTTP_204_NO_CONTENT, operation_id="delete-chat"
)
def delete_chat(id: int, db: Session = Depends(get_db)):
    logger.info("Attempting to delete chat [%s]", id)
    return ChatService.delete_chat(id=id, db=db)
