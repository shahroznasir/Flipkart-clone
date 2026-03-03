from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class CartItemEntity(Base):
    __tablename__ = "cart_items"

    id = Column(
        Integer,
        primary_key=True
    )

    cart_id = Column(
        Integer,
        ForeignKey("carts.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )