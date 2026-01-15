import time

from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from src.core.database import Session, Session_local  # noqa: F401

MAX_RETRIES = 5
RETRY_DELAY = 2


def get_db():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            db = Session_local()
            db.execute(text("SELECT 1"))
            break  # подключение успешно
        except OperationalError:
            if attempt == MAX_RETRIES:
                raise
            print(
                f"DB not ready, retrying in {RETRY_DELAY}s... ({attempt}/{MAX_RETRIES})"
            )
            time.sleep(RETRY_DELAY)
    try:
        yield db
    finally:
        db.close()
