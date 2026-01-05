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


