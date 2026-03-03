from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from loguru import logger
from app.schemas.product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)
from app.database import get_db
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService
from app.dependency import require_roles

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# Get All Products (Public)

@router.get(
    "/",
    response_model=List[ProductResponse]
)
def list_products(
    db: Session = Depends(get_db)
):
    logger.info("List all products API called")
    repo = ProductRepository(db)
    service = ProductService(repo)
    products = service.get_all_products()
    logger.info(f"{len(products)} products returned")
    return products

# Seller Dashboard

@router.get(
    "/my-products",
    response_model=List[ProductResponse]
)
def get_my_products(
    db: Session = Depends(get_db),
    user=Depends(require_roles(["admin", "seller"]))
):
    logger.info(
        f"My products API called user_id={user['user_id']}"
    )
    repo = ProductRepository(db)
    service = ProductService(repo)
    products = service.get_products_by_seller(
        user["user_id"]
    )
    logger.info(
        f"{len(products)} products returned for seller"
    )
    return products


# Search Products

@router.get(
    "/search/",
    response_model=List[ProductResponse]
)
def search_products(
    keyword: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):

    logger.info(
        f"Search products API called keyword={keyword}"
    )
    repo = ProductRepository(db)
    service = ProductService(repo)
    products = service.search_products(keyword)
    logger.info(
        f"{len(products)} products found"
    )

    return products

# Get Product by ID

@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    logger.info(
        f"Get product API called product_id={product_id}"
    )
    repo = ProductRepository(db)
    service = ProductService(repo)
    product = service.get_product_by_id(product_id)
    if not product:
        logger.error(
            f"Product not found product_id={product_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    logger.success(
        f"Product fetched successfully product_id={product_id}"
    )
    return product

# Create Product

@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def add_product(
    product_create: ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles(["admin", "seller"]))
):
    logger.info(
        f"Create product API called seller_id={user['user_id']}"
    )
    repo = ProductRepository(db)
    service = ProductService(repo)
    product = service.create_product(
        product_create,
        user["user_id"]
    )
    logger.success(
        f"Product created product_id={product.id}"
    )

    return product

# Update Product

@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_roles(["admin", "seller"]))
):
    logger.info(
        f"Update product API called product_id={product_id}"
    )
    repo = ProductRepository(db)
    service = ProductService(repo)
    product = service.update_product(
        product_id,
        product_update,
        user["user_id"],
        user["role"]
    )
    logger.success(
        f"Product updated product_id={product_id}"
    )

    return product

# Delete Product

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles(["admin", "seller"]))
):

    logger.info(
        f"Delete product API called product_id={product_id}"
    )
    repo = ProductRepository(db)
    service = ProductService(repo)
    service.delete_product(
        product_id,
        user["user_id"],
        user["role"]
    )

    logger.success(
        f"Product deleted product_id={product_id}"
    )
    return None