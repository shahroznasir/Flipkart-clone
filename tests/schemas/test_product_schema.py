import pytest
from pydantic import ValidationError
from app.schemas.product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)

# ProductCreate Tests
def test_product_create_valid():
    product = ProductCreate(
        name="iPhone 15",
        price=999.99,
        stock=10
    )

    assert product.name == "iPhone 15"
    assert product.price == 999.99
    assert product.stock == 10


def test_product_create_name_too_short():
    with pytest.raises(ValidationError):
        ProductCreate(
            name="ab",
            price=100,
            stock=5
        )


def test_product_create_price_zero():
    with pytest.raises(ValidationError):
        ProductCreate(
            name="Valid Product",
            price=0,
            stock=5
        )


def test_product_create_price_negative():
    with pytest.raises(ValidationError):
        ProductCreate(
            name="Valid Product",
            price=-10,
            stock=5
        )


def test_product_create_negative_stock():
    with pytest.raises(ValidationError):
        ProductCreate(
            name="Valid Product",
            price=100,
            stock=-1
        )

# ProductUpdate Tests
def test_product_update_partial_valid():
    update = ProductUpdate(price=150.5)

    assert update.price == 150.5
    assert update.name is None
    assert update.stock is None


def test_product_update_invalid_name():
    with pytest.raises(ValidationError):
        ProductUpdate(name="ab")


def test_product_update_invalid_price():
    with pytest.raises(ValidationError):
        ProductUpdate(price=0)


def test_product_update_invalid_stock():
    with pytest.raises(ValidationError):
        ProductUpdate(stock=-5)

# ProductResponse Tests
def test_product_response_valid():
    response = ProductResponse(
        id=1,
        seller_id=100,
        name="MacBook Pro",
        price=1999.99,
        stock=5
    )
    assert response.id == 1
    assert response.seller_id == 100
    assert response.name == "MacBook Pro"
    assert response.price == 1999.99
    assert response.stock == 5