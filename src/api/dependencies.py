from src.core.database import Session, Session_local


def get_db():
    db: Session = Session_local()
    try:
        yield db
    finally:
        db.close()
