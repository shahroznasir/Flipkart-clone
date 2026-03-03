from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from app.entities.product_entity import ProductEntity


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db


    # Create Product
    def create_product(
        self,
        product: ProductEntity
    ) -> ProductEntity:

        try:
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)

            return product
        except SQLAlchemyError as e:

            self.db.rollback()
            raise e


    # Get Product by ID
    def get_product_by_id(
        self,
        product_id: int
    ) -> Optional[ProductEntity]:

        return (
            self.db.query(ProductEntity)
            .filter(ProductEntity.id == product_id)
            .first()
        )


    # Get All Products
    def get_all_products(
        self
    ) -> List[ProductEntity]:

        return (
            self.db.query(ProductEntity)
            .order_by(ProductEntity.id.desc())
            .all()
        )


    # Get Products by Seller (VERY IMPORTANT)
    def get_products_by_seller(
        self,
        seller_id: int
    ) -> List[ProductEntity]:

        return (
            self.db.query(ProductEntity)
            .filter(ProductEntity.seller_id == seller_id)
            .all()
        )


    # Update Product
    def update_product(
        self,
        product: ProductEntity
    ) -> ProductEntity:

        try:
            self.db.commit()
            self.db.refresh(product)

            return product

        except SQLAlchemyError as e:

            self.db.rollback()
            raise e


    # Delete Product
    def delete_product(
        self,
        product: ProductEntity
    ) -> bool:

        try:
            self.db.delete(product)
            self.db.commit()

            return True

        except SQLAlchemyError as e:

            self.db.rollback()
            raise e


    # Search Product
    def search_products_by_name(
        self,
        keyword: str
    ) -> List[ProductEntity]:

        return (
            self.db.query(ProductEntity)
            .filter(ProductEntity.name.ilike(f"%{keyword}%"))
            .order_by(ProductEntity.id.desc())
            .all()
        )


    # Check Exists
    def product_exists(
        self,
        product_id: int
    ) -> bool:

        return self.db.query(
            self.db.query(ProductEntity)
            .filter(ProductEntity.id == product_id)
            .exists()
        ).scalar()