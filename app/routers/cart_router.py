from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loguru import logger
from app.dependency import get_db
from app.dependency import require_roles
from app.services.cart_service import CartService
from app.schemas.cart_schema import CartItemCreate

router = APIRouter(prefix="/cart", tags=["Cart"])

# VIEW CART
@router.get("/")
def view_cart(
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles(["user"]))
):
    user_id = user["user_id"]
    logger.info(f"View cart user_id={user_id}")
    service = CartService(db)
    cart = service.get_or_create_cart(user_id)
    items = service.get_cart_items(cart.id)
    return {
        "cart_id": cart.id,
        "items": items
    }

# ADD ITEM
@router.post("/items", status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles(["user"]))
):
    user_id = user["user_id"]
    logger.info(
        f"Add to cart user_id={user_id} product_id={item.product_id}"
    )
    service = CartService(db)
    try:
        cart_item = service.add_item(
            user_id=user_id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        return {
            "message": "Item added to cart",
            "cart_item_id": cart_item.id
        }
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

# UPDATE ITEM
@router.put("/items/{item_id}")
def update_cart_item(
    item_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles(["user"]))
):
    user_id = user["user_id"]
    logger.info(
        f"Update cart item user_id={user_id} item_id={item_id}"
    )
    service = CartService(db)
    try:
        service.update_item(
            user_id=user_id,
            item_id=item_id,
            quantity=quantity
        )
        return {
            "message": "Cart updated"
        }

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

# REMOVE ITEM
@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles(["user"]))
):
    user_id = user["user_id"]
    logger.info(
        f"Remove cart item user_id={user_id} item_id={item_id}"
    )
    service = CartService(db)
    try:
        service.remove_item(
            user_id=user_id,
            item_id=item_id
        )

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )