from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loguru import logger
from app.database import get_db
from app.dependency import get_current_user
from app.entities.order_entity import OrderEntity
from app.entities.payment_entity import PaymentEntity

router = APIRouter(prefix="/payments", tags=["Payments"])

# PAY FOR ORDER

@router.post("/{order_id}")
def pay_order(
    order_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):

    user_id = user["user_id"]
    logger.info(f"Payment initiated: user_id={user_id}, order_id={order_id}")

    # Find order
    order = db.query(OrderEntity).filter(

        OrderEntity.id == order_id,
        OrderEntity.user_id == user_id
    ).first()

    if not order:
        logger.warning(
            f"Payment failed: Order not found order_id={order_id}, user_id={user_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    # Prevent double payment
    if order.status == "paid":
        logger.warning(
            f"Payment blocked: Order already paid order_id={order_id}"
        )
        raise HTTPException(
            status_code=400,
            detail="Order already paid"
        )
    logger.info(
        f"Processing payment: order_id={order.id}, amount={order.total}"
    )

    # Create payment
    payment = PaymentEntity(
        order_id=order.id,
        amount=order.total,
        status="success"
    )
    db.add(payment)

    # Update order status
    order.status = "paid"
    db.commit()
    db.refresh(payment)
    logger.success(
        f"Payment successful: payment_id={payment.id}, order_id={order.id}"
    )
    return {
        "payment_id": payment.id,
        "order_id": order.id,
        "amount": payment.amount,
        "status": payment.status
    }