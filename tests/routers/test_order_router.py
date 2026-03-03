import pytest
from loguru import logger


# TEST CHECKOUT
def test_checkout(client, auth_headers):
    logger.info("Testing checkout")

    payload = {
        "product_id": 1,
        "quantity": 2
    }

    # Add item to cart (authenticated)
    client.post(
        "/api/v1/cart/items",
        json=payload,
        headers=auth_headers
    )

    # Checkout (authenticated)
    response = client.post(
        "/api/v1/orders/checkout",
        headers=auth_headers
    )

    logger.debug(f"Checkout response: {response.json()}")

    assert response.status_code == 201
    data = response.json()

    assert "order_id" in data
    assert isinstance(data["order_id"], int)

    assert "total" in data
    assert isinstance(data["total"], (int, float))

    assert "status" in data

    logger.success("Checkout test passed")


# TEST MY ORDERS
def test_my_orders(client, auth_headers):
    logger.info("Testing my orders")

    response = client.get(
        "/api/v1/orders/me",
        headers=auth_headers
    )

    logger.debug(f"My orders response: {response.json()}")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)

    logger.success("My orders test passed")


# TEST ORDER DETAIL
def test_order_detail(client, auth_headers):
    logger.info("Testing order detail")

    payload = {
        "product_id": 1,
        "quantity": 1
    }

    # Add item to cart
    client.post(
        "/api/v1/cart/items",
        json=payload,
        headers=auth_headers
    )

    # Checkout
    checkout = client.post(
        "/api/v1/orders/checkout",
        headers=auth_headers
    )

    order_id = checkout.json()["order_id"]

    # Get order detail
    response = client.get(
        f"/api/v1/orders/{order_id}",
        headers=auth_headers
    )

    logger.debug(f"Order detail response: {response.json()}")

    assert response.status_code == 200
    data = response.json()

    assert "order_id" in data
    assert data["order_id"] == order_id

    assert "total" in data
    assert "status" in data

    logger.success("Order detail test passed")


# TEST INVALID ORDER DETAIL
def test_invalid_order_detail(client, auth_headers):
    logger.info("Testing invalid order detail")

    response = client.get(
        "/api/v1/orders/9999",
        headers=auth_headers
    )

    logger.debug(f"Invalid order response: {response.text}")

    assert response.status_code == 400

    logger.success("Invalid order detail test passed")