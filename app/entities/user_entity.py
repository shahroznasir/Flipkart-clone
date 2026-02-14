from sqlalchemy import Column, Integer, String
from app.db import Base


class UserEntity(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)

    # Only two roles allowed: "admin" or "user"
    role = Column(String, nullable=False, default="user")
