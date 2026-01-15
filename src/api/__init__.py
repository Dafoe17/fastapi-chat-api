from fastapi import APIRouter

from src.core.database import Base, engine

from .routers import router

main_router = APIRouter()

main_router.include_router(router)


@main_router.get("/", include_in_schema=False)
def root():
    return {
        "message": 'Тестовое задание для команды "hitalent": '
        "API для работы с чатами и сообщениями",
        "routes": {
            "GET /chats/{id}": "Get chat with messages",
            "POST /chats/": "Create chat",
            "POST /chats/{id}/messages/": "Send message",
            "DELETE /chats/{id}": "Delete chat",
        },
        "docs": "/docs",
    }


Base.metadata.create_all(bind=engine)
