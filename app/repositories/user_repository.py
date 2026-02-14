from sqlalchemy.orm import Session
from app.entities.user_entity import UserEntity


class UserRepository:

    def find_by_email(self, db: Session, email: str):
        return db.query(UserEntity).filter(
            UserEntity.email == email
        ).first()

    def save(self, db: Session, user: UserEntity):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
