import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.routers.product_router import router as product_router
from app.database import get_db


app = FastAPI()
app.include_router(product_router, prefix="/api/v1")
BASE_URL = "/api/v1/products"

@pytest.fixture(autouse=True)
def override_db():
    app.dependency_overrides[get_db] = lambda: MagicMock()
    yield
    app.dependency_overrides = {}

# Override ALL role dependencies dynamically
@pytest.fixture(autouse=True)
def override_role_dependencies():
    for route in app.routes:
        if hasattr(route, "dependant"):
            for dep in route.dependant.dependencies:
                app.dependency_overrides[dep.call] = lambda: {
                    "user_id": 1,
                    "role": "admin"
                }
    yield
    app.dependency_overrides = {}
client = TestClient(app)

# Mock product helper
def mock_product_dict():
    return {
        "id": 1,
        "name": "Laptop",
        "price": 50000,
        "description": "Gaming laptop",
        "stock": 10,
        "seller_id": 1
    }

def mock_product_object():
    mock_obj = MagicMock()
    mock_obj.id = 1
    mock_obj.name = "Laptop"
    mock_obj.price = 50000
    mock_obj.description = "Gaming laptop"
    mock_obj.stock = 10
    mock_obj.seller_id = 1
    return mock_obj

# Tests
@patch("app.routers.product_router.ProductService")
def test_list_products(mock_service):
    mock_service.return_value.get_all_products.return_value = [
        mock_product_dict()
    ]
    response = client.get(f"{BASE_URL}/")
    assert response.status_code == 200


@patch("app.routers.product_router.ProductService")
def test_get_my_products(mock_service):
    mock_service.return_value.get_products_by_seller.return_value = [
        mock_product_dict()
    ]
    response = client.get(f"{BASE_URL}/my-products")
    assert response.status_code == 200


@patch("app.routers.product_router.ProductService")
def test_search_products(mock_service):
    mock_service.return_value.search_products.return_value = [
        mock_product_dict()
    ]
    response = client.get(f"{BASE_URL}/search/?keyword=laptop")
    assert response.status_code == 200


@patch("app.routers.product_router.ProductService")
def test_get_product_success(mock_service):
    mock_service.return_value.get_product_by_id.return_value = (
        mock_product_dict()
    )
    response = client.get(f"{BASE_URL}/1")
    assert response.status_code == 200


@patch("app.routers.product_router.ProductService")
def test_get_product_not_found(mock_service):
    mock_service.return_value.get_product_by_id.return_value = None
    response = client.get(f"{BASE_URL}/999")
    assert response.status_code == 404


@patch("app.routers.product_router.ProductService")
def test_add_product(mock_service):
    mock_service.return_value.create_product.return_value = (
        mock_product_object()
    )
    payload = {
        "name": "Laptop",
        "price": 50000,
        "description": "Gaming laptop",
        "stock": 10
    }
    response = client.post(f"{BASE_URL}/", json=payload)
    assert response.status_code == 201


@patch("app.routers.product_router.ProductService")
def test_update_product(mock_service):
    mock_service.return_value.update_product.return_value = (
        mock_product_dict()
    )
    payload = {
        "name": "Laptop",
        "price": 50000,
        "description": "Gaming laptop",
        "stock": 10
    }
    response = client.put(f"{BASE_URL}/1", json=payload)
    assert response.status_code == 200


@patch("app.routers.product_router.ProductService")
def test_delete_product(mock_service):
    mock_service.return_value.delete_product.return_value = None
    response = client.delete(f"{BASE_URL}/1")
    assert response.status_code == 204