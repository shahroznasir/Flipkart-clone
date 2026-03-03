from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loguru import logger
from app.dependency import get_db, require_roles
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])

# CHECKOUT

@router.post("/checkout", status_code=status.HTTP_201_CREATED)
def checkout(
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles(["user"]))
):

    user_id = user["user_id"]
    logger.info(f"Checkout API called user_id={user_id}")
    service = OrderService(db)
    try:
        order = service.checkout(user_id)
        logger.success(
            f"Checkout successful order_id={order.id}"
        )
        return {
            "order_id": order.id,
            "total": order.total,
            "status": order.status
        }

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

# MY ORDERS

@router.get("/me")
def my_orders(
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles(["user"]))
):

    user_id = user["user_id"]
    logger.info(f"My orders API called user_id={user_id}")
    service = OrderService(db)
    orders = service.get_user_orders(user_id)
    logger.info(f"{len(orders)} orders returned")
    return orders

# ORDER DETAIL

@router.get("/{order_id}")
def order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles(["user", "admin"]))
):

    logger.info(
        f"Order detail API called order_id={order_id}"
    )
    service = OrderService(db)
    try:
        order_data = service.get_order_detail(
            user=user,
            order_id=order_id
        )

        logger.success(
            f"Order detail fetched order_id={order_id}"
        )
        return order_data

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )