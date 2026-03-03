import pytest
from pydantic import ValidationError
from app.schemas.cart_schema import (
    CartItemCreate,
    CartItemUpdate,
    CartItemResponse,
    CartResponse,
)

# CartItemCreate Tests
def test_cart_item_create_valid():
    item = CartItemCreate(product_id=1, quantity=2)
    assert item.product_id == 1
    assert item.quantity == 2


def test_cart_item_create_invalid_quantity_zero():
    with pytest.raises(ValidationError):
        CartItemCreate(product_id=1, quantity=0)


def test_cart_item_create_invalid_quantity_negative():
    with pytest.raises(ValidationError):
        CartItemCreate(product_id=1, quantity=-5)

# CartItemUpdate Tests
def test_cart_item_update_valid():
    update = CartItemUpdate(quantity=3)
    assert update.quantity == 3


def test_cart_item_update_zero_allowed():
    update = CartItemUpdate(quantity=0)
    assert update.quantity == 0


def test_cart_item_update_negative_not_allowed():
    with pytest.raises(ValidationError):
        CartItemUpdate(quantity=-1)

# CartItemResponse Tests
def test_cart_item_response_valid():
    response = CartItemResponse(
        id=1,
        product_id=10,
        quantity=5
    )
    assert response.id == 1
    assert response.product_id == 10
    assert response.quantity == 5

# CartResponse Tests
def test_cart_response_with_items():
    item1 = CartItemResponse(id=1, product_id=1, quantity=2)
    item2 = CartItemResponse(id=2, product_id=2, quantity=3)

    cart = CartResponse(
        cart_id=100,
        items=[item1, item2]
    )
    assert cart.cart_id == 100
    assert len(cart.items) == 2
    assert cart.items[0].product_id == 1
    assert cart.items[1].quantity == 3


def test_cart_response_empty_items():
    cart = CartResponse(cart_id=1, items=[])
    assert cart.cart_id == 1
    assert cart.items == []