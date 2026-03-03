from sqlalchemy.orm import Session
from loguru import logger
from app.entities.order_entity import OrderEntity
from app.entities.order_item_entity import OrderItemEntity


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    # CREATE ORDER

    def create_order(self, order: OrderEntity):
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        logger.info(
            f"Order created id={order.id}"
        )
        return order

    # ADD ORDER ITEM

    def add_order_item(self, order_item: OrderItemEntity):
        self.db.add(order_item)
        self.db.commit()
        self.db.refresh(order_item)
        logger.info(
            f"Order item added id={order_item.id}"
        )
        return order_item

    # UPDATE ORDER

    def update_order(self):
        self.db.commit()

    # GET USER ORDERS

    def get_user_orders(self, user_id: int):
        return self.db.query(OrderEntity).filter_by(
            user_id=user_id
        ).all()

    # GET ORDER BY ID

    def get_order_by_id(self, order_id: int):
        return self.db.query(OrderEntity).filter_by(
            id=order_id
        ).first()


    # GET ORDER ITEMS

    def get_order_items(self, order_id: int):
        return self.db.query(OrderItemEntity).filter_by(
            order_id=order_id
        ).all()