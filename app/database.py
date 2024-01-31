from app.models import SessionLocal


def connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
