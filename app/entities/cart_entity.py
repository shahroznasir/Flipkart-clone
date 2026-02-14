from sqlalchemy import Column, Integer, ForeignKey
from app.db import Base

class CartEntity(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
