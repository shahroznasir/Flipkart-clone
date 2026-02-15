from sqlalchemy.orm import Session
from app.models.user import User
from app.


class UserRepository:

    def find_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
