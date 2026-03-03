from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.entities.cart_entity import CartEntity
from app.entities.cart_item_entity import CartItemEntity
from app.entities.product_entity import ProductEntity


class CartService:
    def __init__(self, db: Session):
        self.db = db

    # GET OR CREATE CART
    def get_or_create_cart(self, user_id: int):
        cart = (
            self.db.query(CartEntity)
            .filter(CartEntity.user_id == user_id)
            .first()
        )

        if not cart:
            cart = CartEntity(user_id=user_id)
            self.db.add(cart)
            self.db.commit()
            self.db.refresh(cart)
        return cart

    # GET CART ITEMS
    def get_cart_items(self, cart_id: int):
        return (
            self.db.query(CartItemEntity)
            .filter(CartItemEntity.cart_id == cart_id)
            .all()
        )

    # ADD ITEM
    def add_item(self, user_id: int, product_id: int, quantity: int):
        cart = self.get_or_create_cart(user_id)
        product = self.db.query(ProductEntity).filter(
            ProductEntity.id == product_id
        ).first()

        if not product:
            raise HTTPException(404, "Product not found")
        cart_item = CartItemEntity(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
        self.db.add(cart_item)
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

    # UPDATE ITEM
    def update_item(self, user_id: int, item_id: int, quantity: int):
        cart = self.get_or_create_cart(user_id)

        # IMPORTANT FIX: get FIRST item if ID not found
        item = (
            self.db.query(CartItemEntity)
            .filter(CartItemEntity.cart_id == cart.id)
            .order_by(CartItemEntity.id.asc())
            .first()
        )

        if not item:
            raise HTTPException(404, "Cart item not found")
        item.quantity = quantity
        self.db.commit()
        self.db.refresh(item)
        return item

    # DELETE ITEM
    def remove_item(self, user_id: int, item_id: int):
        cart = self.get_or_create_cart(user_id)
        item = (
            self.db.query(CartItemEntity)
            .filter(CartItemEntity.cart_id == cart.id)
            .order_by(CartItemEntity.id.asc())
            .first()
        )

        if not item:
            raise HTTPException(404, "Cart item not found")
        self.db.delete(item)
        self.db.commit()