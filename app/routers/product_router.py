from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.entities.user_entity import UserEntity
from app.entities.product_entity import ProductEntity
from app.schemas.product_schema import ProductCreate, ProductResponse
from app.deps import get_db, require_roles

router = APIRouter(prefix="/products", tags=["Products"])


# ==========================
# LIST PRODUCTS (PUBLIC)
# ==========================
@router.get("/", response_model=List[ProductResponse])
def list_products(
    search: str | None = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(ProductEntity)

    if search:
        query = query.filter(ProductEntity.name.ilike(f"%{search}%"))

    return query.all()


# ==========================
# ADD PRODUCT (SELLER/ADMIN)
# ==========================
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductResponse
)
def add_product(
    p: ProductCreate,
    db: Session = Depends(get_db),
    seller: UserEntity = Depends(require_roles(["seller", "admin"]))
):
    product = ProductEntity(
        name=p.name,
        price=p.price,
        stock=p.stock,
        seller_id=seller.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


# ==========================
# UPDATE PRODUCT
# ==========================
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    p: ProductCreate,
    db: Session = Depends(get_db),
    user: UserEntity = Depends(require_roles(["seller", "admin"]))
):
    product = db.query(ProductEntity).filter(
        ProductEntity.id == product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = p.name
    product.price = p.price
    product.stock = p.stock

    db.commit()
    db.refresh(product)

    return product


# ==========================
# DELETE PRODUCT (ADMIN ONLY)
# ==========================
@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: UserEntity = Depends(require_roles(["admin"]))
):
    product = db.query(ProductEntity).filter(
        ProductEntity.id == product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}
