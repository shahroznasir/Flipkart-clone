from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db, require_roles

from app.entities.cart_entity import CartEntity
from app.entities.cart_item_entity import CartItemEntity
from app.entities.product_entity import ProductEntity
from app.entities.user_entity import UserEntity

from app.schemas.cart_schema import CartItemCreate

router = APIRouter(prefix="/cart", tags=["Cart"])


# ==========================
# GET OR CREATE CART
# ==========================
def get_or_create_cart(user: UserEntity, db: Session):
    cart = db.query(CartEntity).filter_by(user_id=user.id).first()

    if not cart:
        cart = CartEntity(user_id=user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    return cart


# ==========================
# VIEW CART
# ==========================
@router.get("/")
def view_cart(
    db: Session = Depends(get_db),
    user: UserEntity = Depends(require_roles(["user"]))
):
    cart = get_or_create_cart(user, db)

    items = db.query(CartItemEntity).filter(
        CartItemEntity.cart_id == cart.id
    ).all()

    return {
        "cart_id": cart.id,
        "items": items
    }


# ==========================
# ADD ITEM TO CART
# ==========================
@router.post("/items", status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    user: UserEntity = Depends(require_roles(["user"]))
):
    cart = get_or_create_cart(user, db)

    product = db.query(ProductEntity).filter(
        ProductEntity.id == item.product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    cart_item = db.query(CartItemEntity).filter_by(
        cart_id=cart.id,
        product_id=product.id
    ).first()

    if cart_item:
        cart_item.qty += item.quantity   # ✅ IMPORTANT
    else:
        cart_item = CartItemEntity(
            cart_id=cart.id,
            product_id=product.id,
            qty=item.quantity             # ✅ MUST BE qty
        )
        db.add(cart_item)

    db.commit()

    return {"message": "Item added to cart"}


# ==========================
# UPDATE CART ITEM
# ==========================
@router.put("/items/{item_id}")
def update_cart_item(
    item_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    user: UserEntity = Depends(require_roles(["user"]))
):
    cart = get_or_create_cart(user, db)

    item = db.query(CartItemEntity).filter_by(
        id=item_id,
        cart_id=cart.id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if quantity <= 0:
        db.delete(item)
    else:
        item.qty = quantity   # ✅ MUST BE qty

    db.commit()

    return {"message": "Cart updated"}


# ==========================
# REMOVE CART ITEM
# ==========================
@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    user: UserEntity = Depends(require_roles(["user"]))
):
    cart = get_or_create_cart(user, db)

    item = db.query(CartItemEntity).filter_by(
        id=item_id,
        cart_id=cart.id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
