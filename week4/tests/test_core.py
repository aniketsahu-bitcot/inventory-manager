"""
Unit tests for the Inventory class covering standard operations,
edge cases, error conditions, and boundary values using pytest fixtures.
"""

import pytest
from week3.inventory_manager.core import Inventory
from week3.inventory_manager.models import (
    Product,
    BookProduct,
    FoodProduct,
)



def test_inventory_creation_empty(empty_inventory: Inventory) -> None:
    """Test creating an empty Inventory instance."""
    
    inventory = empty_inventory
    
    assert isinstance(inventory, Inventory)
    assert len(inventory.products) == 0


def test_inventory_creation_single_product(single_product_inventory: Inventory) -> None:
    """Test Inventory creation with a single product."""
   
    inventory = single_product_inventory
    
    assert isinstance(inventory, Inventory)
    assert len(inventory.products) == 1
    assert isinstance(inventory.products[0], Product)

def test_inventory_creation_multiple_products(
    multiple_products_inventory: Inventory,
) -> None:
    """Test Inventory creation with multiple products using AAA pattern."""

    inventory = multiple_products_inventory

    products = inventory.products
    product_types = [isinstance(p, Product) for p in products]

    assert isinstance(inventory, Inventory)
    assert len(products) == 4
    assert all(product_types)



def test_inventory_creation_with_low_stock(low_stock_inventory: Inventory) -> None:
    """Test Inventory creation with products that include low stock items."""

    inventory = low_stock_inventory

    assert isinstance(inventory, Inventory)
    assert len(inventory.products) == 2
    low_stock_products = [p for p in inventory.products if p.quantity < 10]
    assert len(low_stock_products) == 2
    assert low_stock_products[0].quantity == 0


def test_add_product_standard(product_laptop: Product) -> None:
    """Add a single product to inventory."""

    inventory = Inventory()

    inventory.add_product(product_laptop)

    assert product_laptop in inventory.products
    assert len(inventory.products) == 1


def test_add_product_multiple_products(product_laptop: Product, product_book: BookProduct, food_bread: FoodProduct) -> None:
    """Add multiple products to inventory."""

    inventory = Inventory()

    inventory.add_product(product_laptop)
    inventory.add_product(product_book)
    inventory.add_product(food_bread)

    assert len(inventory.products) == 3
    assert product_laptop in inventory.products
    assert product_book in inventory.products
    assert food_bread in inventory.products


def test_add_product_duplicate_id_raises_error(product_laptop: Product) -> None:
    """Adding a product with duplicate ID raises ValueError."""

    inventory = Inventory()
    inventory.add_product(product_laptop)

    with pytest.raises(ValueError):
        inventory.add_product(product_laptop)


def test_add_product_zero_quantity(product_zero_qty: Product) -> None:
    """Add a product with zero quantity to inventory."""

    inventory = Inventory()

    inventory.add_product(product_zero_qty)

    assert product_zero_qty in inventory.products
    assert inventory.products[0].quantity == 0


def test_get_product_item_is_retrieved(
    single_product_inventory: Inventory,
    product_laptop: Product
) -> None:
    """Retrieving an existing product returns the correct object."""

    inventory = single_product_inventory
    product_id = product_laptop.product_id

    result = inventory.get_product(product_id)

    assert result is product_laptop


def test_get_product_unusual_id_still_matches(
    empty_inventory: Inventory
) -> None:
    """Unusual but matching product IDs are handled."""

    inventory = empty_inventory
    product = Product(product_id="XX--001!!", product_name="Odd Item", quantity=1, price=5.0)
    inventory.add_product(product)

    result = inventory.get_product("XX--001!!")

    assert result is product


def test_get_product_item_not_present_returns_none(
    empty_inventory: Inventory
) -> None:
    """Retrieving a product that does not exist returns None."""
   
    inventory = empty_inventory
    product_id = "NOT_PRESENT"

    result = inventory.get_product(product_id)

    assert result is None

def test_get_product_with_minimal_length_id(
    empty_inventory: Inventory
) -> None:
    """Retrieving using the shortest possible ID value."""
    
    inventory = empty_inventory
    product = Product(product_id="A", product_name="Tiny ID", quantity=2, price=10.0)
    inventory.add_product(product)

    result = inventory.get_product("A")

    assert result is product


def test_get_low_stock_returns_items_below_threshold(
    multiple_products_inventory: Inventory,
    product_laptop: Product,
    electronic_tv: Product,
) -> None:
    """Products with quantity below the default threshold should be returned."""

    inventory = multiple_products_inventory
    low_stock = list(inventory.get_low_stock())

    expected_ids = {product_laptop.product_id, electronic_tv.product_id}
    result_ids = {p.product_id for p in low_stock}

    assert result_ids == expected_ids


def test_get_low_stock_works_with_custom_threshold(
    multiple_products_inventory: Inventory,
    product_book: Product,
) -> None:
    """Scenario where a custom threshold is used to change which products qualify."""

    inventory = multiple_products_inventory
    threshold = 15

    low_stock = list(inventory.get_low_stock(threshold=threshold))

    
    result_ids = {p.product_id for p in low_stock}

    
    assert product_book.product_id in result_ids



def test_get_low_stock_when_inventory_is_empty(
    empty_inventory: Inventory,
) -> None:
    """Scenario where no products exist in inventory so nothing is returned."""
    
    inventory = empty_inventory

    result = list(inventory.get_low_stock())

    assert result == []

def test_get_low_stock_includes_products_with_zero_quantity(
    low_stock_inventory: Inventory,
    product_zero_qty: Product,
    product_laptop: Product,
) -> None:
    """Scenario where products with zero quantity are included when below the threshold."""

    inventory = low_stock_inventory
    low_stock = list(inventory.get_low_stock())

    expected_ids = {product_zero_qty.product_id, product_laptop.product_id}
    result_ids = {p.product_id for p in low_stock}

    assert result_ids == expected_ids


def test_get_inventory_value_multiple_items(
    multiple_products_inventory: Inventory,
) -> None:
    """Total inventory value should equal the sum of quantity * price."""
    
    inventory = multiple_products_inventory
    expected_total = sum(p.quantity * p.price for p in inventory.products)

    result = inventory.get_inventory_value()

    assert result == expected_total

def test_get_inventory_value_empty_inventory(
    empty_inventory: Inventory,
) -> None:
    """Scenario where the inventory is empty and total value should be zero."""
    
    inventory = empty_inventory

    result = inventory.get_inventory_value()

    assert result == 0

def test_get_inventory_value_with_high_quantity_item(
    product_large_qty: Product,
    empty_inventory: Inventory,
) -> None:
    """Scenario where an item has very high quantity and contributes most of the value."""

    inventory = empty_inventory
    inventory.add_product(product_large_qty)
    expected_total = product_large_qty.quantity * product_large_qty.price

    result = inventory.get_inventory_value()

    assert result == expected_total

def test_get_inventory_value_includes_zero_quantity_item(
    product_zero_qty: Product,
    product_laptop: Product,
    empty_inventory: Inventory,
) -> None:
    """Scenario where products with zero quantity still exist but add nothing to total value."""
 
    inventory = empty_inventory
    inventory.add_product(product_zero_qty)
    inventory.add_product(product_laptop)
    expected_total = product_laptop.quantity * product_laptop.price

    result = inventory.get_inventory_value()

    assert result == expected_total
