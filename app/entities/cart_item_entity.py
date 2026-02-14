from sqlalchemy import Column, Integer, ForeignKey
from app.db import Base

class CartItemEntity(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    qty = Column(Integer)
