import pytest
from loguru import logger


# TEST SUCCESSFUL PAYMENT
def test_pay_order_success(client, auth_headers):
    logger.info("Testing successful payment")

    # First create order (authenticated)
    payload = {
        "product_id": 1,
        "quantity": 1
    }

    client.post(
        "/api/v1/cart/items",
        json=payload,
        headers=auth_headers
    )

    checkout = client.post(
        "/api/v1/orders/checkout",
        headers=auth_headers
    )

    order_id = checkout.json()["order_id"]

    # Pay for order (authenticated)
    response = client.post(
        f"/api/v1/payments/{order_id}",
        headers=auth_headers
    )

    logger.debug(f"Payment response: {response.json()}")

    assert response.status_code == 200
    data = response.json()

    assert "payment_id" in data
    assert data["order_id"] == order_id
    assert data["status"] == "success"

    logger.success("Payment success test passed")


# TEST DOUBLE PAYMENT BLOCKED
def test_double_payment_blocked(client, auth_headers):
    logger.info("Testing double payment prevention")

    payload = {
        "product_id": 1,
        "quantity": 1
    }

    client.post(
        "/api/v1/cart/items",
        json=payload,
        headers=auth_headers
    )

    checkout = client.post(
        "/api/v1/orders/checkout",
        headers=auth_headers
    )

    order_id = checkout.json()["order_id"]

    # First payment
    client.post(
        f"/api/v1/payments/{order_id}",
        headers=auth_headers
    )

    # Second payment attempt
    response = client.post(
        f"/api/v1/payments/{order_id}",
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Order already paid"

    logger.success("Double payment blocked test passed")


# TEST PAYMENT ORDER NOT FOUND
def test_payment_order_not_found(client, auth_headers):
    logger.info("Testing payment for invalid order")

    response = client.post(
        "/api/v1/payments/9999",
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"

    logger.success("Invalid order payment test passed")