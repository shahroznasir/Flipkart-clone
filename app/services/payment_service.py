from app.core.logger import logger
from sqlalchemy.orm import Session
from app.entities.order_entity import OrderEntity
from app.entities.payment_entity import PaymentEntity

class PaymentService:
    def __init__(self, db: Session):
        self.db = db

    def pay(self, user_id: int, order_id: int):
        logger.info(
            "Payment initiated | user_id={} order_id={}",
            user_id,
            order_id
        )

        # Fetch order
        order = self.db.query(OrderEntity).filter_by(
            id=order_id,
            user_id=user_id
        ).first()

        if not order:
            logger.error(
                "Payment failed - order not found | user_id={} order_id={}",
                user_id,
                order_id
            )
            raise Exception("Order not found")

        logger.debug(
            "Order found | order_id={} status={} total={}",
            order.id,
            order.status,
            order.total
        )

        if order.status == "paid":
            logger.warning(
                "Payment attempt on already paid order | order_id={}",
                order.id
            )
            raise Exception("Order already paid")

        # Create payment record
        payment = PaymentEntity(
            order_id=order.id,
            amount=order.total,
            status="success"
        )

        # Update order status
        order.status = "paid"
        logger.debug(
            "Order status updated to paid | order_id={}",
            order.id
        )

        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)

        logger.success(
            "Payment completed successfully | payment_id={} order_id={} amount={}",
            payment.id,
            order.id,
            payment.amount
        )
        return payment