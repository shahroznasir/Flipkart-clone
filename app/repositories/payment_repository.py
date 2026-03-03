from sqlalchemy.orm import Session
from loguru import logger
from app.entities.payment_entity import PaymentEntity
from app.entities.order_entity import OrderEntity


class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    # CREATE PAYMENT

    def create_payment(self, payment: PaymentEntity):
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        logger.info(
            f"Payment created id={payment.id}"
        )
        return payment

    # GET PAYMENT BY ORDER

    def get_payment_by_order(self, order_id: int):
        return self.db.query(PaymentEntity).filter_by(
            order_id=order_id
        ).first()

    # UPDATE ORDER STATUS

    def update_order_status(self, order: OrderEntity):
        self.db.commit()
        logger.info(
            f"Order status updated order_id={order.id}"
        )