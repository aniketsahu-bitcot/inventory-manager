"""
Pytest configuration for test fixtures.

This module provides shared pytest fixtures for running integration tests.
It integrates the existing `inventory_manager` package which handles all inventory operations.
"""
import pytest
from fastapi.testclient import TestClient
from week6.app import app
from week3.inventory_manager.models import Product
from week6.api.routes import inventory as api_inventory
from week3.inventory_manager.core import Inventory

@pytest.fixture(scope="module")
def client() -> TestClient:
    """
    Provides a FastAPI TestClient for testing endpoints.
    """
    return TestClient(app)

@pytest.fixture
def mock_inventory() -> Inventory:
    """
    Provides a clean Inventory instance for testing.
    """
    api_inventory.products.clear()
    return api_inventory

@pytest.fixture(autouse=True)
def populate_inventory(mock_inventory) -> None:
    """Populate the inventory with sample products for testing."""

    mock_inventory.products.clear()
    mock_inventory._product_map.clear()   

    products = [
        Product(product_id="101", product_name="Mouse", quantity=10, price=499.0),
        Product(product_id="104", product_name="Keyboard", quantity=0, price=999.0),
        Product(product_id="106", product_name="Laptop - Pro/Max", quantity=1000000, price=999999.99),
        Product(product_id="105", product_name="Monitor", quantity=100000, price=15000.0),
        Product(product_id="108", product_name="Camera+Lens Kit", quantity=5, price=1200.0),
        Product(product_id="109", product_name="Server", quantity=10, price=1000000.0),
    ]

    for p in products:
        mock_inventory.add_product(p)
