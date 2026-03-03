import pytest
from loguru import logger


# TEST VIEW CART
def test_view_cart(client, auth_headers):
    logger.info("Testing view cart")
    response = client.get("/api/v1/cart/", headers=auth_headers)
    logger.debug(f"Response status: {response.status_code}")
    logger.debug(f"Response body: {response.json()}")

    assert response.status_code == 200
    data = response.json()

    assert "cart_id" in data
    assert isinstance(data["cart_id"], int)

    assert "items" in data
    assert isinstance(data["items"], list)

    logger.success("View cart test passed")


# TEST ADD ITEM TO CART
def test_add_to_cart(client, auth_headers):
    payload = {
        "product_id": 1,
        "quantity": 2
    }

    logger.info(f"Testing add to cart payload={payload}")

    response = client.post(
        "/api/v1/cart/items",
        json=payload,
        headers=auth_headers
    )

    logger.debug(f"Response status: {response.status_code}")
    logger.debug(f"Response body: {response.json()}")

    assert response.status_code == 201
    data = response.json()

    assert data["message"] == "Item added to cart"
    assert "cart_item_id" in data
    assert isinstance(data["cart_item_id"], int)

    logger.success("Add to cart test passed")


# TEST UPDATE CART ITEM
def test_update_cart_item(client, auth_headers):
    logger.info("Testing update cart item")

    response = client.put(
        "/api/v1/cart/items/1",
        params={"quantity": 5},
        headers=auth_headers
    )

    logger.debug(f"Response status: {response.status_code}")
    logger.debug(f"Response body: {response.json()}")

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Cart updated"

    logger.success("Update cart test passed")


# TEST REMOVE CART ITEM
def test_remove_cart_item(client, auth_headers):
    logger.info("Testing remove cart item")

    response = client.delete(
        "/api/v1/cart/items/1",
        headers=auth_headers
    )

    logger.debug(f"Response status: {response.status_code}")

    assert response.status_code == 204

    logger.success("Remove cart test passed")


# TEST REMOVE NON EXISTING ITEM
def test_remove_invalid_item(client, auth_headers):
    logger.info("Testing remove invalid cart item")

    response = client.delete(
        "/api/v1/cart/items/9999",
        headers=auth_headers
    )

    logger.debug(f"Response status: {response.status_code}")
    logger.debug(f"Response body: {response.text}")

    assert response.status_code in (400, 404)

    logger.success("Remove invalid item test passed")


# TEST ADD INVALID PRODUCT
def test_add_invalid_product(client, auth_headers):
    payload = {
        "product_id": 9999,
        "quantity": 1
    }

    logger.info(f"Testing add invalid product payload={payload}")

    response = client.post(
        "/api/v1/cart/items",
        json=payload,
        headers=auth_headers
    )

    logger.debug(f"Response status: {response.status_code}")
    logger.debug(f"Response body: {response.text}")

    assert response.status_code == 400

    logger.success("Add invalid product test passed")