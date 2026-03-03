from typing import List
from fastapi import HTTPException, status
from app.core.logger import logger
from app.repositories.product_repository import ProductRepository

from app.schemas.product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)

from app.mappers.product_mapper import ProductMapper


class ProductService:

    def __init__(self, repo: ProductRepository):
        self.repo = repo


    # Create Product
    def create_product(
        self,
        product_create: ProductCreate,
        seller_id: int
    ) -> ProductResponse:

        logger.info(
            "Product creation started | seller_id={} name={} price={}",
            seller_id,
            product_create.name,
            product_create.price
        )

        product_entity = ProductMapper.to_entity(
            product_create,
            seller_id
        )

        saved_product = self.repo.create_product(
            product_entity
        )

        logger.success(
            "Product created successfully | product_id={} seller_id={}",
            saved_product.id,
            seller_id
        )

        return ProductMapper.to_response(
            saved_product
        )


    # Get All Products
    def get_all_products(self) -> List[ProductResponse]:

        logger.info("Fetching all products")

        products = self.repo.get_all_products()

        logger.debug(
            "Products fetched | count={}",
            len(products)
        )

        return [
            ProductMapper.to_response(product)
            for product in products
        ]


    # Get Seller Products
    def get_products_by_seller(
        self,
        seller_id: int
    ) -> List[ProductResponse]:

        logger.info(
            "Fetching seller products | seller_id={}",
            seller_id
        )

        products = self.repo.get_products_by_seller(
            seller_id
        )

        logger.debug(
            "Seller products fetched | seller_id={} count={}",
            seller_id,
            len(products)
        )

        return [
            ProductMapper.to_response(product)
            for product in products
        ]


    # Get Product by ID
    def get_product_by_id(
        self,
        product_id: int
    ) -> ProductResponse:

        logger.info(
            "Fetching product | product_id={}",
            product_id
        )

        product = self.repo.get_product_by_id(
            product_id
        )

        if not product:

            logger.warning(
                "Product not found | product_id={}",
                product_id
            )

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        logger.debug(
            "Product fetched successfully | product_id={} seller_id={}",
            product.id,
            product.seller_id
        )

        return ProductMapper.to_response(product)


    # Update Product
    def update_product(
        self,
        product_id: int,
        product_update: ProductUpdate,
        user_id: int,
        role: str
    ) -> ProductResponse:

        logger.info(
            "Product update attempt | product_id={} user_id={} role={}",
            product_id,
            user_id,
            role
        )

        product = self.repo.get_product_by_id(
            product_id
        )

        if not product:

            logger.warning(
                "Update failed - product not found | product_id={}",
                product_id
            )

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )


        if role != "admin" and product.seller_id != user_id:

            logger.warning(
                "Unauthorized product update attempt | product_id={} user_id={}",
                product_id,
                user_id
            )

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can update only your own products"
            )


        if product_update.name is not None:
            product.name = product_update.name

        if product_update.price is not None:
            product.price = product_update.price

        if product_update.stock is not None:
            product.stock = product_update.stock


        updated_product = self.repo.update_product(product)

        logger.success(
            "Product updated successfully | product_id={}",
            updated_product.id
        )

        return ProductMapper.to_response(updated_product)


    # Delete Product
    def delete_product(
        self,
        product_id: int,
        user_id: int,
        role: str
    ) -> bool:

        logger.info(
            "Product delete attempt | product_id={} user_id={} role={}",
            product_id,
            user_id,
            role
        )

        product = self.repo.get_product_by_id(product_id)

        if not product:

            logger.warning(
                "Delete failed - product not found | product_id={}",
                product_id
            )

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )


        if role != "admin" and product.seller_id != user_id:

            logger.warning(
                "Unauthorized delete attempt | product_id={} user_id={}",
                product_id,
                user_id
            )

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can delete only your own products"
            )


        result = self.repo.delete_product(product)

        logger.success(
            "Product deleted successfully | product_id={}",
            product_id
        )

        return result


    # Search Product
    def search_products(
        self,
        keyword: str
    ) -> List[ProductResponse]:

        logger.info(
            "Product search | keyword={}",
            keyword
        )

        products = self.repo.search_products_by_name(keyword)

        logger.debug(
            "Search completed | keyword={} results={}",
            keyword,
            len(products)
        )

        return [
            ProductMapper.to_response(product)
            for product in products
        ]