from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db, require_roles

# ✅ IMPORT ENTITIES (NOT models)
from app.entities.user_entity import UserEntity
from app.entities.cart_entity import CartEntity
from app.entities.cart_item_entity import CartItemEntity
from app.entities.product_entity import ProductEntity
from app.entities.order_entity import OrderEntity
from app.entities.order_item_entity import OrderItemEntity

router = APIRouter(prefix="/orders", tags=["Orders"])


# ==========================
# CHECKOUT CART → ORDER
# ==========================
@router.post("/checkout", status_code=status.HTTP_201_CREATED)
def checkout(
    db: Session = Depends(get_db),
    user: UserEntity = Depends(require_roles(["user"]))
):
    cart = db.query(CartEntity).filter_by(user_id=user.id).first()

    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    cart_items = db.query(CartItemEntity).filter_by(cart_id=cart.id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0

    order = OrderEntity(
        user_id=user.id,
        total=0,
        status="pending"
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart_items:
        product = db.query(ProductEntity).filter(
            ProductEntity.id == item.product_id
        ).first()

        if not product or product.stock < item.qty:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product {item.product_id}"
            )

        product.stock -= item.qty
        item_total = product.price * item.qty
        total += item_total

        order_item = OrderItemEntity(
            order_id=order.id,
            product_id=product.id,
            quantity=item.qty,
            price=product.price
        )
        db.add(order_item)

    order.total = total

    # clear cart
    db.query(CartItemEntity).filter_by(cart_id=cart.id).delete()

    db.commit()

    return {
        "order_id": order.id,
        "total": order.total,
        "status": order.status
    }


# ==========================
# USER ORDER HISTORY
# ==========================
@router.get("/me")
def my_orders(
    db: Session = Depends(get_db),
    user: UserEntity = Depends(require_roles(["user"]))
):
    return db.query(OrderEntity).filter(
        OrderEntity.user_id == user.id
    ).all()


# ==========================
# SINGLE ORDER (OWNER ONLY)
# ==========================
@router.get("/{order_id}")
def order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    user: UserEntity = Depends(require_roles(["user", "admin"]))
):
    order = db.query(OrderEntity).filter_by(id=order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if user.role != "admin" and order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    items = db.query(OrderItemEntity).filter_by(order_id=order.id).all()

    return {
        "order": order,
        "items": items
    }
