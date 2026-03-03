from sqlalchemy.orm import Session
from loguru import logger
from app.entities.cart_entity import CartEntity
from app.entities.cart_item_entity import CartItemEntity

class CartRepository:

    def __init__(self, db: Session):
        self.db = db

    # GET OR CREATE CART

    def get_or_create_cart(self, user_id: int) -> CartEntity:
        cart = self.db.query(CartEntity).filter_by(
            user_id=user_id
        ).first()
        if not cart:
            logger.info(f"Creating new cart user_id={user_id}")
            cart = CartEntity(
                user_id=user_id
            )
            self.db.add(cart)
            self.db.commit()
            self.db.refresh(cart)
        return cart

    # GET CART ITEMS

    def get_cart_items(self, cart_id: int):
        return self.db.query(CartItemEntity).filter_by(
            cart_id=cart_id
        ).all()

    # GET SINGLE ITEM

    def get_cart_item(self, cart_id: int, product_id: int):
        return self.db.query(CartItemEntity).filter_by(
            cart_id=cart_id,
            product_id=product_id
        ).first()

    # ADD ITEM

    def add_cart_item(self, cart_item: CartItemEntity):
        self.db.add(cart_item)
        self.db.commit()
        self.db.refresh(cart_item)
        logger.info(
            f"Cart item added id={cart_item.id}"
        )
        return cart_item

    # UPDATE ITEM

    def update_cart_item(self):
        self.db.commit()

    # DELETE ITEM

    def delete_cart_item(self, cart_item: CartItemEntity):
        self.db.delete(cart_item)
        self.db.commit()
        logger.info(
            f"Cart item deleted id={cart_item.id}"
        )

    # CLEAR CART

    def clear_cart(self, cart_id: int):
        self.db.query(CartItemEntity).filter_by(
            cart_id=cart_id
        ).delete()
        self.db.commit()
        logger.info(
            f"Cart cleared cart_id={cart_id}"
        )