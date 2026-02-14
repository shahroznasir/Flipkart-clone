from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class StoreEntity(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"))

    seller = relationship("UserEntity")
