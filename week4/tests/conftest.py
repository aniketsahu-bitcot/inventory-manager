"""Pytest fixtures for Inventory Management.

Provides reusable fixtures for Product, FoodProduct, BookProduct,
ElectronicProduct, and Inventory instances for testing purposes.
"""

import pytest
from typing import Dict, Any
from datetime import date, timedelta
from week3.inventory_manager.core import Inventory
from week3.inventory_manager.models import (
    Product,
    ElectronicProduct,
    FoodProduct,
    BookProduct,
)

@pytest.fixture
def valid_product_data() -> Dict[str, Any]:
    """Fixture to create valid Product data."""
    return {
        "product_id": "P001",
        "product_name": "Laptop",
        "quantity": 10,
        "price": 999.99,
    }


@pytest.fixture
def edge_large_values_data() -> Dict[str, Any]:
    """Fixture to create Product data using large and unusual values."""
    return {
        "product_id": "X" * 50,
        "product_name": "High-End Workstation",
        "quantity": 1_000_000,
        "price": 123456.789,
    }


@pytest.fixture
def missing_name_data(valid_product_data: Dict[str, Any]) -> Dict[str, Any]:
    """Fixture to create product data missing product_name."""
    data = valid_product_data.copy()
    data.pop("product_name")
    return data

@pytest.fixture
def negative_quantity_data(valid_product_data: Dict[str, Any]) -> Dict[str, Any]:
    """Fixture to create product data with negative quantity."""
    data = valid_product_data.copy()
    data["quantity"] = -5
    return data


@pytest.fixture
def zero_price_data(valid_product_data: Dict[str, Any]) -> Dict[str, Any]:
    """Fixture to create product data with zero price."""
    data = valid_product_data.copy()
    data["price"] = 0
    return data


@pytest.fixture
def boundary_minimum_values_data(valid_product_data: Dict[str, Any]) -> Dict[str, Any]:
    """Fixture to create valid Product data at boundary conditions."""
    data = valid_product_data.copy()
    data["quantity"] = 0
    data["price"] = 0.01
    return data

@pytest.fixture
def product_laptop() -> Product:
    """Fixture to create a valid laptop product."""
    return Product(product_id="P001", product_name="Laptop", quantity=5, price=1000.0)


@pytest.fixture
def product_book() -> Product:
    """Fixture to create a valid book product."""
    return Product(product_id="P010", product_name="Generic Book", quantity=12, price=25.0)


@pytest.fixture
def product_food() -> Product:
    """Fixture to create a valid food product."""
    return Product(product_id="P011", product_name="Generic Food Item", quantity=30, price=5.0)


@pytest.fixture
def product_zero_qty() -> Product:
    """Fixture to create a product with zero quantity."""
    return Product(product_id="P020", product_name="Zero Qty Item", quantity=0, price=50.0)


@pytest.fixture
def product_large_qty() -> Product:
    """Fixture to create a product with a very large quantity."""
    return Product(product_id="P021", product_name="Bulk Item", quantity=10000, price=2.5)


@pytest.fixture
def product_min_price() -> Product:
    """Fixture to create a product with minimal positive price."""
    return Product(product_id="P030", product_name="Cheap Item", quantity=1, price=0.01)


@pytest.fixture
def product_single_qty() -> Product:
    """Fixture to create a product with quantity equal to one."""
    return Product(product_id="P031", product_name="Single Stock Item", quantity=1, price=100.0)


@pytest.fixture
def invalid_negative_price_data() -> dict:
    """Fixture to create product data with negative price."""
    return dict(product_id="P040", product_name="Invalid Negative Price", quantity=5, price=-10.0)


@pytest.fixture
def invalid_negative_qty_data() -> dict:
    """Fixture to create product data with negative quantity."""
    return dict(product_id="P041", product_name="Invalid Negative Qty", quantity=-5, price=100.0)



@pytest.fixture
def food_bread() -> FoodProduct:
    """Fixture to create a FoodProduct with a valid future expiry date."""
    return FoodProduct(product_id="F001", product_name="Bread", quantity=20, price=2.5,
                       expiry_date=date.today() + timedelta(days=7))


@pytest.fixture
def food_cheese() -> FoodProduct:
    """Fixture to create a FoodProduct with a valid future expiry date."""
    return FoodProduct(product_id="F002", product_name="Cheddar Cheese", quantity=5, price=4.0,
                       expiry_date=date.today() + timedelta(days=30))


@pytest.fixture
def food_expiry_today() -> FoodProduct:
    """Fixture to create a FoodProduct with expiry date today."""
    return FoodProduct(product_id="F010", product_name="Yogurt", quantity=3, price=1.5,
                       expiry_date=date.today())


@pytest.fixture
def food_large_quantity() -> FoodProduct:
    """Fixture to create a FoodProduct with a very high quantity."""
    return FoodProduct(product_id="F011", product_name="Bulk Rice", quantity=10000, price=1.0,
                       expiry_date=date.today() + timedelta(days=10))


@pytest.fixture
def food_zero_quantity() -> FoodProduct:
    """Fixture to create a FoodProduct with zero quantity."""
    return FoodProduct(product_id="F012", product_name="Zero Qty Nuts", quantity=0, price=3.0,
                       expiry_date=date.today() + timedelta(days=5))


@pytest.fixture
def food_min_price() -> FoodProduct:
    """Fixture to create a FoodProduct with minimal positive price."""
    return FoodProduct(product_id="F020", product_name="Budget Snack", quantity=1, price=0.01,
                       expiry_date=date.today() + timedelta(days=1))


@pytest.fixture
def food_single_quantity() -> FoodProduct:
    """Fixture to create a FoodProduct with quantity equal to one."""
    return FoodProduct(product_id="F021", product_name="Single Apple", quantity=1, price=2.0,
                       expiry_date=date.today() + timedelta(days=3))


@pytest.fixture
def invalid_food_past_expiry_data() -> dict:
    """Fixture to create FoodProduct data with expiry date in the past."""
    return dict(product_id="F030", product_name="Expired Milk", quantity=2, price=1.0,
                expiry_date=date.today() - timedelta(days=1))


@pytest.fixture
def invalid_food_negative_price_data() -> dict:
    """Fixture to create FoodProduct data with negative price."""
    return dict(product_id="F031", product_name="Invalid Price Snack", quantity=3, price=-2.0,
                expiry_date=date.today() + timedelta(days=3))


@pytest.fixture
def invalid_food_negative_quantity_data() -> dict:
    """Fixture to create FoodProduct data with negative quantity."""
    return dict(product_id="F032", product_name="Invalid Qty Pasta", quantity=-5, price=3.5,
                expiry_date=date.today() + timedelta(days=4))



@pytest.fixture
def book_python() -> BookProduct:
    """Fixture to create a BookProduct representing a Python book."""
    return BookProduct(product_id="B001", product_name="Learning Python", quantity=8, price=40.0, author="Mark Lutz")


@pytest.fixture
def book_zero_qty() -> BookProduct:
    """Fixture to create a product with zero quantity."""
    return BookProduct(product_id="B010", product_name="Zero Qty Book", quantity=0, price=20.0, author="Unknown")


@pytest.fixture
def book_large_qty() -> BookProduct:
    """Fixture to create a product with a very large quantity."""
    return BookProduct(product_id="B011", product_name="Bulk Order Book", quantity=5000, price=12.0, author="Unknown")


@pytest.fixture
def book_min_price() -> BookProduct:
    """Fixture to create a product with minimal positive price."""
    return BookProduct(product_id="B020", product_name="Budget Book", quantity=1, price=0.01, author="Unknown")


@pytest.fixture
def book_single_qty() -> BookProduct:
    """Fixture to create a product with quantity equal to one."""
    return BookProduct(product_id="B021", product_name="Single Copy Book", quantity=1, price=10.0, author="Unknown")


@pytest.fixture
def invalid_book_negative_price_data() -> dict:
    """Fixture to create product data with negative price."""
    return dict(product_id="B030", product_name="Invalid Negative Price Book", quantity=3, price=-5.0)


@pytest.fixture
def invalid_book_negative_qty_data() -> dict:
    """Fixture to create product data with negative quantity."""
    return dict(product_id="B031", product_name="Invalid Negative Qty Book", quantity=-2, price=25.0)



@pytest.fixture
def electronic_tv() -> ElectronicProduct:
    """Fixture to create an ElectronicProduct representing a smart TV."""
    return ElectronicProduct(product_id="E001", product_name="Smart TV", quantity=3, price=1500.0, warranty_period=24)


@pytest.fixture
def electronic_product_with_one_month_warranty() -> ElectronicProduct:
    """Fixture to create an ElectronicProduct with the smallest reasonable warranty."""
    return ElectronicProduct(product_id="E_EDGE_01", product_name="USB Hub", quantity=5, price=25.0, warranty_period=1)


@pytest.fixture
def electronic_product_with_high_price_low_quantity() -> ElectronicProduct:
    """Fixture to create an ElectronicProduct with very high price and low quantity."""
    return ElectronicProduct(product_id="E_EDGE_02", product_name="Enterprise Server", quantity=1, price=250000.0,
                             warranty_period=36)


@pytest.fixture
def electronic_product_with_large_warranty() -> ElectronicProduct:
    """Fixture to create an ElectronicProduct with a large warranty period."""
    return ElectronicProduct(product_id="E003", product_name="Speaker", quantity=2, price=100.0, warranty_period=120)


@pytest.fixture
def invalid_electronic_zero_warranty_data() -> dict:
    """Fixture to create ElectronicProduct data with zero warranty."""
    return dict(product_id="E002", product_name="Camera", quantity=1, price=200.0, warranty_period=0)


@pytest.fixture
def invalid_electronic_negative_price_data() -> dict:
    """Fixture to create ElectronicProduct data with negative price."""
    return dict(product_id="E004", product_name="Phone", quantity=1, price=-500.0, warranty_period=12)


@pytest.fixture
def empty_inventory() -> Inventory:
    """Fixture for an empty Inventory instance."""
    return Inventory()

@pytest.fixture
def single_product_inventory(product_laptop: Product) -> Inventory:
    """Fixture for Inventory with a single product."""
    inventory = Inventory()
    inventory.add_product(product_laptop)
    return inventory

@pytest.fixture
def multiple_products_inventory(
    product_laptop: Product,
    product_book: Product,
    product_food: Product,
    electronic_tv: ElectronicProduct
) -> Inventory:
    """Fixture for Inventory with multiple diverse products."""
    inventory = Inventory()
    inventory.add_product(product_laptop)
    inventory.add_product(product_book)
    inventory.add_product(product_food)
    inventory.add_product(electronic_tv)
    return inventory

@pytest.fixture
def low_stock_inventory(product_zero_qty: Product, product_laptop: Product) -> Inventory:
    """Fixture with products that are low in stock."""
    inventory = Inventory()
    inventory.add_product(product_zero_qty)
    inventory.add_product(product_laptop)
    return inventory
