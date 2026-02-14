from app.db import SessionLocal
from app.models import UserEntity


def save_user(entity: UserEntity) -> UserEntity:
    db = SessionLocal()

    db.add(entity)
    db.commit()
    db.refresh(entity)

    return entity
