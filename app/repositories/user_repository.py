from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.entities.user_entity import UserEntity


class UserRepository:

    def __init__(self, db: Session):

        self.db = db


    # ========================
    # FIND USER BY EMAIL
    # ========================

    def find_by_email(self, email: str) -> UserEntity | None:

        return (

            self.db
            .query(UserEntity)
            .filter(UserEntity.email == email)
            .first()

        )


    # ========================
    # CREATE USER
    # ========================

    def create(self, user_data: dict) -> UserEntity:

        try:

            user = UserEntity(**user_data)

            self.db.add(user)

            self.db.commit()

            self.db.refresh(user)

            return user


        except SQLAlchemyError as e:

            self.db.rollback()

            raise e


    # ========================
    # FIND USER BY ID
    # ========================

    def find_by_id(self, user_id: int) -> UserEntity | None:

        return (

            self.db
            .query(UserEntity)
            .filter(UserEntity.id == user_id)
            .first()

        )


    # ========================
    # GET ALL USERS
    # ========================

    def get_all(self) -> list[UserEntity]:

        return self.db.query(UserEntity).all()


    # ========================
    # DELETE USER
    # ========================

    def delete(self, user_id: int) -> bool:

        try:

            user = self.find_by_id(user_id)

            if not user:

                return False


            self.db.delete(user)

            self.db.commit()

            return True


        except SQLAlchemyError:

            self.db.rollback()

            raise