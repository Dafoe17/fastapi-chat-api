from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker  # noqa: F401

from .config import settings

engine = create_engine(settings.DATABASE_URL)

Session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)


class Base(DeclarativeBase):
    pass


from src.models import Chat, Message  # noqa: E402,F401
