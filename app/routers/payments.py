from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user

# ✅ Import ENTITIES (NOT models)
from app.entities.order_entity import OrderEntity
from app.entities.payment_entity import PaymentEntity
from app.entities.user_entity import UserEntity

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/{order_id}")
def pay_order(
    order_id: int,
    db: Session = Depends(get_db),
    user: UserEntity = Depends(get_current_user)
):
    # 1️⃣ Find order
    order = db.query(OrderEntity).filter(
        OrderEntity.id == order_id,
        OrderEntity.user_id == user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # 2️⃣ Prevent double payment
    if order.status == "paid":
        raise HTTPException(status_code=400, detail="Order already paid")

    # 3️⃣ Create payment (Mock payment logic)
    payment = PaymentEntity(
        order_id=order.id,
        amount=order.total,
        status="success"
    )

    db.add(payment)

    # 4️⃣ Update order status
    order.status = "paid"

    db.commit()
    db.refresh(payment)

    return {
        "payment_id": payment.id,
        "order_id": order.id,
        "amount": payment.amount,
        "status": payment.status
    }