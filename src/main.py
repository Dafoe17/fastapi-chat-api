import uvicorn
from fastapi import FastAPI

from src.api import main_router

app = FastAPI(
    title="Chat API",
    description='Тестовое задание для команды "hitalent": '
    "API для работы с чатами и сообщениями",
    version="1.0.0",
)

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug"
    )
