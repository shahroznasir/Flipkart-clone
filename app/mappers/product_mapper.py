from loguru import logger
from app.schemas.product_schema import ProductCreate, ProductResponse
from app.entities.product_entity import ProductEntity


class ProductMapper:
    @staticmethod
    def to_entity(
        product_create: ProductCreate,
        seller_id: int
    ) -> ProductEntity:
        logger.debug(
            "Mapping ProductCreate schema to ProductEntity | name={} seller_id={}",
            product_create.name,
            seller_id
        )

        entity = ProductEntity(
            name=product_create.name,
            price=product_create.price,
            stock=product_create.stock,
            seller_id=seller_id
        )

        logger.info(
            "ProductEntity created successfully | name={} seller_id={}",
            entity.name,
            entity.seller_id
        )
        return entity


    @staticmethod
    def to_response(
        product: ProductEntity
    ) -> ProductResponse:
        logger.debug(
            "Mapping ProductEntity to ProductResponse | product_id={}",
            product.id
        )
        response = ProductResponse.model_validate(product)
        logger.info(
            "ProductResponse created successfully | product_id={}",
            response.id
        )
        return response