from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.db import Base


class ProductEntity(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

    seller_id = Column(Integer, ForeignKey("users.id"))
