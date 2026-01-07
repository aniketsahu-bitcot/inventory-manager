"""
Integration tests for the inventory API routes.

These tests verify that the FastAPI inventory endpoints return the correct responses and behavior.
It integrates the existing `inventory_manager` package which handles all inventory operations.
"""

from typing import Any
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from week3.inventory_manager.models import Product


def test_list_products(client: TestClient, mock_inventory: Any) -> None:
    """
    GET /products returns all products correctly.
    """
    response = client.get("/api/products")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    ids = [p["product_id"] for p in data]

    for expected_id in ["101", "104", "105", "106", "108", "109"]:
        assert expected_id in ids

def test_list_products_empty_inventory(client: TestClient, mock_inventory: Any) -> None:
    """
    GET /products returns empty list when inventory is empty.
    """
    mock_inventory.products.clear()
    mock_inventory._product_map.clear()

    response = client.get("/api/products")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == []


def test_list_products_special_characters_in_name(client: TestClient, mock_inventory: Any) -> None:
    """
    Products with special characters in name are returned correctly.
    """
    response = client.get("/api/products")
    data = response.json()
    names = [p["product_name"] for p in data]
    assert any("Laptop - Pro/Max" in name for name in names)


def test_list_products_zero_quantity(client: TestClient, mock_inventory: Any) -> None:
    """
    Products with quantity=0 are returned correctly.
    """
    response = client.get("/api/products")
    data = response.json()
    zero_qty = [p for p in data if p["quantity"] == 0]
    assert len(zero_qty) >= 1


def test_list_products_large_price_and_quantity(client: TestClient, mock_inventory: Any) -> None:
    """
    Products with very large quantity and price are returned correctly.
    """
    response = client.get("/api/products")
    data = response.json()
    large_product = [p for p in data if p["product_id"] == "106"]
    assert large_product[0]["price"] == 999999.99
    assert large_product[0]["quantity"] == 1000000


def test_list_products_duplicate_product_id(mock_inventory: Any) -> None:
    """
    Adding duplicate product ID raises ValueError.
    """
    product = Product(product_id="101", product_name="Mouse", quantity=5, price=499.0)
    with pytest.raises(ValueError):
        mock_inventory.add_product(product)


def test_get_product(client: TestClient, mock_inventory: Any) -> None:
    """
    GET /products/{product_id} returns correct product.
    """
    response = client.get("/api/products/101")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["product_id"] == "101"
    assert data["product_name"] == "Mouse"


def test_get_product_min_quantity(client: TestClient, mock_inventory: Any) -> None:
    """
    GET /products/{product_id} with quantity=0.
    """
    response = client.get("/api/products/104")
    data = response.json()
    assert data["quantity"] == 0


def test_get_product_special_characters_in_name(client: TestClient, mock_inventory: Any) -> None:
    """
    GET /products/{product_id} with special characters in name.
    """
    response = client.get("/api/products/108")
    data = response.json()
    assert data["product_name"] == "Camera+Lens Kit"


def test_get_product_high_quantity(client: TestClient, mock_inventory: Any) -> None:
    """
    GET /products/{product_id} with high quantity.
    """
    response = client.get("/api/products/105")
    data = response.json()
    assert data["quantity"] == 100000


def test_get_product_large_price(client: TestClient, mock_inventory: Any) -> None:
    """
    GET /products/{product_id} with very large price.
    """
    response = client.get("/api/products/109")
    data = response.json()
    assert data["price"] == 1000000.0


def test_get_product_not_found(client: TestClient, mock_inventory: Any) -> None:
    """
    GET /products/{product_id} with non-existent product ID returns 404.
    """
    response = client.get("/api/products/999") 
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "Product not found"


def test_create_product(client: TestClient) -> None:
    """
    Ensure a valid product is created successfully and returns 201 + product body.
    """
  
    payload = {
        "product_id": "200",
        "product_name": "USB Cable",
        "quantity": 10,
        "price": 99.99,
    }

    response = client.post("/api/products", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data == payload

def test_create_many_products(client: TestClient) -> None:
    """Test creating 50 products in bulk via the POST /api/products endpoint."""

    for i in range(1,51):
        payload = {
            "product_id": f"bulk_{i}",
            "product_name": f"Product {i}",
            "quantity": i,
            "price": float(i),
        }
        response = client.post("/api/products", json=payload)
        assert response.status_code == 201

def test_create_product_min_quantity(client: TestClient) -> None:
    """
    quantity = 0 should still be valid.
    """

    payload = {
        "product_id": "201",
        "product_name": "Empty Box",
        "quantity": 0,
        "price": 10.0,
    }

    response = client.post("/api/products", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["quantity"] == 0

def test_create_product_extremely_large_quantity(client: TestClient) -> None:
    """
    Test creating a product with an extremely large quantity.
    """
    payload = {
        "product_id": "BIG999",
        "product_name": "Huge Quantity",
        "quantity": 10_000_000_000,
        "price": 99.99,
    }

    response = client.post("/api/products", json=payload)

    assert response.status_code in (200, 201, 400, 422)

def test_create_product_with_whitespace_product_id(client) -> None:
    """
    Ensure that creating a product with leading/trailing whitespace
    in product_id succeeds because API does not trim or reject whitespace.
    """

    payload = {
        "product_id": "  P111  ",
        "product_name": "Whitespaced ID Product",
        "quantity": 5,
        "price": 25.50,
    }

    response = client.post("/api/products", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == "  P111  "



def test_create_product_large_value_price(client: TestClient) -> None:
    """
    Test a very large price — should still be handled.
    """

    payload = {
        "product_id": "202",
        "product_name": "Golden Keyboard",
        "quantity": 2,
        "price": 9999999.99,
    }

    response = client.post("/api/products", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["price"] == 9999999.99

def test_create_product_duplicate_id(client: TestClient) -> None:
    """
    Creating a product with an existing ID should return 409 Conflict.
    """
    
    payload = {
        "product_id": "101",
        "product_name": "Duplicate Test",
        "quantity": 1,
        "price": 10.0,
    }

    response = client.post("/api/products", json=payload)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "already exists" in response.json()["detail"]

def test_create_product_invalid_quantity_type(client: TestClient) -> None:
    """
    Non-integer quantity should trigger validation error (422)."""
    payload = {
        "product_id": "T100",
        "product_name": "Invalid Quantity",
        "quantity": "abc",  
        "price": 10.5,
    }

    response = client.post("/api/products", json=payload)
    assert response.status_code == 422

def test_create_product_negative_quantity(client: TestClient) -> None:
    """
    Negative quantity should trigger validation error (400 or 422).
    """
    payload = {
        "product_id": "N100",
        "product_name": "Negative Quantity",
        "quantity": -5,
        "price": 10.0,
    }

    response = client.post("/api/products", json=payload)

    assert response.status_code in (400, 422)

def test_create_product_float_quantity(client: TestClient) -> None:
    """
    Float quantity should trigger validation error (422).
    """
    payload = {
        "product_id": "1001",
        "product_name": "Float Quantity",
        "quantity": 10.5,
        "price": 20,
    }

    response = client.post("/api/products", json=payload)
    assert response.status_code == 422


def test_create_product_negative_price(client: TestClient) -> None:
    """
    Negative price should trigger validation error (400 or 422)."""
    payload = {
        "product_id": "N101",
        "product_name": "Negative Price",
        "quantity": 5,
        "price": -10.0,
    }

    response = client.post("/api/products", json=payload)

    assert response.status_code in (400, 422)

def test_create_product_invalid_price_type(client: TestClient) -> None:
    """
    Non-float price should trigger validation error (422)."""
    payload = {
        "product_id": "1000",
        "product_name": "Invalid Price",
        "quantity": 5,
        "price": "abc",
    }

    response = client.post("/api/products", json=payload)
    assert response.status_code == 422

def test_create_product_very_long_name(client: TestClient) -> None:
    """
    Very long product_name should be accepted."""
    long_name = "A" * 500

    payload = {
        "product_id": "1002",
        "product_name": long_name,
        "quantity": 2,
        "price": 50,
    }

    response = client.post("/api/products", json=payload)
    assert response.status_code == 201


def test_create_product_no_body(client: TestClient) -> None:
    """
    Missing request body should trigger validation error (422)."""
    response = client.post("/api/products")

    assert response.status_code == 422


def test_create_product_invalid_body(client: TestClient) -> None:
    """
    Missing required fields should trigger validation error (422).
    """
    payload = {
        "product_id": "203"
    }

    response = client.post("/api/products", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_create_product_invalid_value(monkeypatch, client: TestClient) -> None:
    """Test create_product route triggers HTTP 400 via simulated ValueError."""
    
    def fake_add_product(product) -> None:
        """Simulate a ValueError in Inventory.add_product."""
        raise ValueError("Some custom error")

    monkeypatch.setattr("week5.api.routes.inventory.add_product", fake_add_product)

    payload = {
        "product_id": "999",
        "product_name": "Test Product",
        "quantity": 5,
        "price": 50.0,
    }

    response = client.post("/api/products", json=payload)

    assert response.status_code == 400
    assert "Some custom error" in response.json()["detail"]

def test_product_id_case_sensitivity(client: TestClient) -> None:
    """
    Ensure product_id is case-sensitive.
    """
    payload = {
        "product_id": "ABC",
        "product_name": "Case Test",
        "quantity": 3,
        "price": 30,
    }

    client.post("/api/products", json=payload)

    response = client.get("/api/products/abc")
    assert response.status_code == 404



def test_update_product(client: TestClient) -> None:
    """
    Update an existing product successfully.
    """
    payload = {
        "product_id": "101",
        "product_name": "Updated Laptop",
        "quantity": 20,
        "price": 3000.0,
    }

    response = client.put("/api/products/101", json=payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["product_name"] == "Updated Laptop"

def test_update_product_zero_quantity(client) -> None:
    """
    Updating a product that does not exist should return 404.
    """

    payload = {
        "product_id": "102",
        "product_name": "Out of Stock Mouse",
        "quantity": 0,
        "price": 500.0,
    }

    response = client.put("/api/products/102", json=payload)

    assert response.status_code == 404

def test_update_product_negative_price(client: TestClient) -> None:
    """
    Updating a product with negative price should fail validation."""
    create_payload = {
        "product_id": "1004",
        "product_name": "To Update",
        "quantity": 2,
        "price": 10,
    }

    client.post("/api/products", json=create_payload)

    update_payload = {
        "product_id": "1004",
        "product_name": "To Update",
        "quantity": 2,
        "price": -5,
    }

    response = client.put("/api/products/1004", json=update_payload)
    assert response.status_code == 422



def test_update_product_empty_name(client, mock_inventory) -> None:
    """
    API currently allows an empty product_name, so update should succeed.
    """

    payload = {
        "product_id": "101",
        "product_name": "",
        "quantity": 10,
        "price": 99.99,
    }

    response = client.put("/api/products/101", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["product_name"] == ""

def test_update_product_high_quantity(client) -> None:
    """
    Updating a non-existing product should return 404,
    even if the quantity is extremely large.
    """

    payload = {
        "product_id": "103",
        "product_name": "Mega Supply Pen Pack",
        "quantity": 1_000_000,
        "price": 2.5,
    }

    response = client.put("/api/products/103", json=payload)

    assert response.status_code == 404


def test_update_product_not_found(client: TestClient) -> None:
    """
    Updating a non-existent product should return 404.
    """

    payload = {
        "product_id": "999",
        "product_name": "Ghost Item",
        "quantity": 1,
        "price": 10.0,
    }

    response = client.put("/api/products/999", json=payload)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Product not found"

def test_update_product_partial_body(client: TestClient) -> None:
    """
    Partial update payload should fail validation."""
    
    create_payload = {
        "product_id": "P200",
        "product_name": "Original",
        "quantity": 5,
        "price": 10.0,
    }
    client.post("/api/products", json=create_payload)

    
    update_payload = {
        "product_name": "Only Name Sent"
    }

    response = client.put("/api/products/P200", json=update_payload)

    assert response.status_code == 422


def test_update_product_invalid_body(client: TestClient) -> None:
    """
    Invalid payload should fail validation.
    """

    payload: dict[str, Any] = {}

    response = client.put("/api/products/101", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_update_product_attempt_change_id(client: TestClient) -> None:
    """
    Attempting to change product_id in update should return 400."""

    create_payload = {
        "product_id": "U300",
        "product_name": "Original",
        "quantity": 3,
        "price": 50.0,
    }
    client.post("/api/products", json=create_payload)

    update_payload = {
        "product_id": "DIFFERENT_ID",
        "product_name": "Updated",
        "quantity": 3,
        "price": 50.0,
    }

    response = client.put("/api/products/U300", json=update_payload)

    assert response.status_code == 400


def test_update_product_path_body_id_mismatch(client: TestClient) -> None:
    """
    Updating a product where the product_id in the path and body differ
    should return 400.
    """
    payload = {
        "product_id": "102",    
        "product_name": "Wrong Match",
        "quantity": 5,
        "price": 50.0,
    }

    response = client.put("/api/products/101", json=payload) 

    assert response.status_code == 400
    assert response.json()["detail"] == "Product ID in path and body must match"


