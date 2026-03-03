from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.entities.cart_entity import CartEntity
from app.entities.cart_item_entity import CartItemEntity
from app.entities.order_entity import OrderEntity
from app.entities.order_item_entity import OrderItemEntity
from app.entities.product_entity import ProductEntity

from app.core.logger import logger


class OrderService:

    def __init__(self, db: Session):
        self.db = db


    # ✅ CHECKOUT
    def checkout(self, user_id: int):

        logger.info("Checkout process started | user_id={}", user_id)

        cart = (
            self.db.query(CartEntity)
            .filter(CartEntity.user_id == user_id)
            .first()
        )

        if not cart:
            raise HTTPException(400, "Cart is empty")

        items = (
            self.db.query(CartItemEntity)
            .filter(CartItemEntity.cart_id == cart.id)
            .all()
        )

        if not items:
            raise HTTPException(400, "Cart is empty")


        total = 0

        order = OrderEntity(
            user_id=user_id,
            total=0,
            status="PLACED"
        )

        self.db.add(order)
        self.db.flush()


        for item in items:

            product = (
                self.db.query(ProductEntity)
                .filter(ProductEntity.id == item.product_id)
                .first()
            )

            if not product:
                raise HTTPException(404, "Product not found")

            price = product.price

            total += price * item.quantity

            order_item = OrderItemEntity(

                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=price

            )

            self.db.add(order_item)


        order.total = total


        # clear cart
        (
            self.db.query(CartItemEntity)
            .filter(CartItemEntity.cart_id == cart.id)
            .delete()
        )

        self.db.commit()

        logger.success("Order created | order_id={}", order.id)

        return order


    # ✅ GET USER ORDERS
    def get_user_orders(self, user_id: int):

        orders = (
            self.db.query(OrderEntity)
            .filter(OrderEntity.user_id == user_id)
            .all()
        )

        return orders


    # ✅ ORDER DETAIL
    def get_order_detail(self, user: dict, order_id: int):

        order = (
            self.db.query(OrderEntity)
            .filter(OrderEntity.id == order_id)
            .first()
        )

        if not order:
            raise HTTPException(404, "Order not found")


        # user can only view own order
        if user["role"] != "admin" and order.user_id != user["user_id"]:

            raise HTTPException(403, "Not allowed")


        items = (
            self.db.query(OrderItemEntity)
            .filter(OrderItemEntity.order_id == order_id)
            .all()
        )


        return {

            "order_id": order.id,

            "total": order.total,

            "status": order.status,

            "items": items

        }