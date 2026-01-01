"""
Unit tests for the Inventory class covering standard operations,
edge cases, error conditions, and boundary values using pytest fixtures.
"""

import pytest
from unittest.mock import mock_open
from unittest.mock import call
from pathlib import Path
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




def test_load_products_from_csv_populates_inventory(mocker) -> None:
    """Inventory should load valid rows from CSV using mocked builtins.open."""

    csv_data = (
        "product_id,product_name,quantity,price\n"
        "P001,Laptop,5,1000.0\n"
        "P002,Mouse,10,25.5\n"
    )

    mocker.patch.object(Path, "exists", return_value=True)

    m = mock_open(read_data=csv_data)

    mocker.patch("builtins.open", m)

    mocker.patch.object(Path, "open", m)

    mocker.patch.object(Path, "write_text", return_value=None)

    inventory = Inventory()

    inventory.load_products_from_csv(Path("fake.csv"))

    assert len(inventory.products) == 2

    p1 = inventory.products[0]
    assert p1.product_id == "P001"
    assert p1.product_name == "Laptop"
    assert int(p1.quantity) == 5
    assert float(p1.price) == 1000.0

    p2 = inventory.products[1]
    assert p2.product_id == "P002"
    assert p2.product_name == "Mouse"
    assert int(p2.quantity) == 10
    assert float(p2.price) == 25.5


def test_load_products_from_csv_handles_blank_lines(mocker) -> None:
    """Ensure blank lines in the CSV do not break processing and valid rows load."""

    csv_data = (
        "product_id,product_name,quantity,price\n"
        "\n"
        "P001,Laptop,5,1000.0\n"
        "\n"
        "P002,Mouse,10,25.5\n"
    )

    mocker.patch.object(Path, "exists", return_value=True)

    m = mock_open(read_data=csv_data)
    mocker.patch("builtins.open", m)
    mocker.patch.object(Path, "open", m)
    mocker.patch.object(Path, "write_text", return_value=None)

    inv = Inventory()
    inv.load_products_from_csv("fake.csv")

    assert len(inv.products) == 2

def test_load_products_from_csv_header_only_results_in_empty_inventory(mocker) -> None:
    """Verify that when only a header row exists, no products are added."""

    csv_data = "product_id,product_name,quantity,price\n"

    mocker.patch.object(Path, "exists", return_value=True)

    m = mock_open(read_data=csv_data)
    mocker.patch("builtins.open", m)
    mocker.patch.object(Path, "open", m)
    mocker.patch.object(Path, "write_text", return_value=None)

    inv = Inventory()
    inv.load_products_from_csv("fake.csv")

    assert len(inv.products) == 0

def test_load_products_from_csv_ignores_trailing_newlines(mocker) -> None:
    """Confirm extra trailing newline characters do not affect processing."""

    csv_data = (
        "product_id,product_name,quantity,price\n"
        "P001,Laptop,5,1000.0\n\n\n"
    )

    mocker.patch.object(Path, "exists", return_value=True)

    m = mock_open(read_data=csv_data)
    mocker.patch("builtins.open", m)
    mocker.patch.object(Path, "open", m)
    mocker.patch.object(Path, "write_text", return_value=None)

    inv = Inventory()
    inv.load_products_from_csv("fake.csv")

    assert len(inv.products) == 1

def test_load_products_from_csv_allows_zero_quantity(mocker) -> None:
    """Verify zero quantity is still treated as a valid product."""

    csv_data = (
        "product_id,product_name,quantity,price\n"
        "P001,Laptop,0,1000.0\n"
    )

    mocker.patch.object(Path, "exists", return_value=True)

    m = mock_open(read_data=csv_data)
    mocker.patch("builtins.open", m)
    mocker.patch.object(Path, "open", m)
    mocker.patch.object(Path, "write_text", return_value=None)

    inv = Inventory()
    inv.load_products_from_csv("fake.csv")

    assert len(inv.products) == 1
    assert int(inv.products[0].quantity) == 0

def test_load_products_from_csv_rejects_zero_price(mocker) -> None:
    """Verify rows with zero price are treated as invalid and skipped."""

    csv_data = (
        "product_id,product_name,quantity,price\n"
        "P001,Laptop,5,0\n"
    )

    mocker.patch.object(Path, "exists", return_value=True)

    m = mock_open(read_data=csv_data)
    mocker.patch("builtins.open", m)
    mocker.patch.object(Path, "open", m)
    mocker.patch.object(Path, "write_text", return_value=None)

    inv = Inventory()
    inv.load_products_from_csv("fake.csv")

    assert len(inv.products) == 0

def test_load_products_from_csv_for_invalid_path_type(mocker) -> None:
    """If a non-path / non-string is passed, ValueError should be raised."""

    inv = Inventory()

    with pytest.raises(ValueError):
        inv.load_products_from_csv(12345)  

def test_load_products_from_csv_when_csv_cannot_be_read(mocker) -> None:
    """If the CSV exists but cannot be opened for reading, PermissionError should be raised."""

    mocker.patch.object(Path, "exists", return_value=True)

    m = mock_open()
    m.side_effect = PermissionError("blocked")
    mocker.patch("builtins.open", m)
    mocker.patch.object(Path, "open", m)

    mocker.patch.object(Path, "write_text", return_value=None)

    inv = Inventory()

    with pytest.raises(PermissionError):
        inv.load_products_from_csv("fake.csv")


def test_load_products_from_csv_file_not_found(mocker) -> None:
    """
    Ensure that attempting to load a CSV file that does not exist
    raises a PermissionError.
    """
    mocker.patch.object(Path, "exists", return_value=False)

    inv = Inventory()

    with pytest.raises(PermissionError):
        inv.load_products_from_csv("missing.csv")


def test_report_writes_only_low_stock_items(mocker) -> None:
    """Ensure only low stock products appear in the report."""
   
    inventory = Inventory()
    inventory.products = [
        Product(product_id="P1", product_name="Laptop", quantity=3, price=1000.0),
        Product(product_id="P2", product_name="Mouse", quantity=15, price=20.0),
    ]

    mock_file = mock_open()
    mocker.patch.object(Path, "open", mock_file)

    inventory.generate_low_stock_report(10, "dummy.txt")

    handle = mock_file()
    written_text = "".join(call.args[0] for call in handle.write.call_args_list)

    assert "Laptop - Quantity: 3" in written_text
    assert "Mouse - Quantity: 15" not in written_text

def test_report_handles_all_items_sufficient(mocker) -> None:
    """Verify the report states all products are sufficient when none qualify."""
   
    inventory = Inventory()
    inventory.products = [
        Product(product_id="P1", product_name="Phone", quantity=20, price=500.0),
    ]

    mock_file = mock_open()
    mocker.patch.object(Path, "open", mock_file)

    inventory.generate_low_stock_report(threshold=5, output_file="dummy.txt")

    handle = mock_file()
    handle.write.assert_has_calls(
        [
            call("Low Stock Report:\n\n"),
            call("All products have sufficient stock.\n"),
        ]
    )

def test_report_when_inventory_is_empty(mocker) -> None:
    """Verify the report handles an empty inventory gracefully."""
   
    inventory = Inventory()

    mock_file = mock_open()
    mocker.patch.object(Path, "open", mock_file)

    inventory.generate_low_stock_report(output_file="dummy.txt")

    handle = mock_file()
    handle.write.assert_has_calls(
        [
            call("Low Stock Report:\n\n"),
            call("All products have sufficient stock.\n"),
        ]
    )

def test_report_includes_items_equal_to_limit(mocker) -> None:
    """Confirm an item exactly at the threshold is not included."""
    
    inventory = Inventory()
    inventory.products = [
        Product(product_id="P1", product_name="Tablet", quantity=10, price=300.0),
    ]

    mock_file = mock_open()
    mocker.patch.object(Path, "open", mock_file)

    inventory.generate_low_stock_report(threshold=10, output_file="dummy.txt")

    handle = mock_file()
    handle.write.assert_has_calls(
        [
            call("Low Stock Report:\n\n"),
            call("All products have sufficient stock.\n"),
        ]
    )

def test_report_with_item_quantity_zero(mocker) -> None:
    """Ensure products with quantity zero are included if threshold > 0."""
    
    inventory = Inventory()
    inventory.products = [
        Product(product_id="P1", product_name="ItemZero", quantity=0, price=10.0),
    ]

    mock_file = mock_open()
    mocker.patch.object(Path, "open", mock_file)

    inventory.generate_low_stock_report(threshold=1, output_file="dummy.txt")
    
    handle = mock_file()
    handle.write.assert_has_calls([
        call("Low Stock Report:\n\n"),
        call("ItemZero - Quantity: 0\n"),
    ])

def test_report_permission_denied(mocker) -> None:
    """Raise error if the file cannot be written due to permission issues."""
    
    inventory = Inventory()
    inventory.products = [
        Product(product_id="P1", product_name="Item", quantity=2, price=10.0),
    ]

    def raise_permission(*args, **kwargs):
        raise PermissionError("Permission denied")

    mocker.patch("pathlib.Path.open", side_effect=raise_permission)

    with pytest.raises(PermissionError):
        inventory.generate_low_stock_report(output_file="dummy.txt")

def test_report_missing_product_name(mocker) -> None:
    """Raise an error if a product in inventory has missing product_name."""
    
    inventory = Inventory()
    
    class IncompleteProduct:
        product_id = "P1"
        quantity = 5
        price = 10.0
    
    inventory.products = [IncompleteProduct()]

    mock_file = mock_open()
    mocker.patch.object(Path, "open", mock_file)

    with pytest.raises(AttributeError):
        inventory.generate_low_stock_report(output_file="dummy.txt")

def test_report_invalid_quantity_type(mocker) -> None:
    """Raise TypeError if a product's quantity is not an integer."""
    
    inventory = Inventory()
 
    class InvalidQuantityProduct:
        product_id = "P1"
        product_name = "Item"
        quantity = "ten"
        price = 10.0
    
    inventory.products = [InvalidQuantityProduct()]

    mock_file = mock_open()
    mocker.patch.object(Path, "open", mock_file)

    with pytest.raises(TypeError):
        inventory.generate_low_stock_report(output_file="dummy.txt")


def test_errors_log_write_fails(mocker) -> None:
    """
    Verify that a PermissionError is raised when the inventory attempts
    to write to errors.log but the write operation fails.
    """
    mocker.patch.object(Path, "exists", return_value=True)

    mocker.patch.object(Path, "open", mock_open(read_data="product_id,product_name,quantity,price\n"))

    mocker.patch.object(Path, "write_text", side_effect=PermissionError("Denied"))

    inv = Inventory()

    with pytest.raises(PermissionError):
        inv.load_products_from_csv("fake.csv")


def test_error_log_write_failure_is_ignored(mocker) -> None:
    """
    Ensure that when writing to errors.log fails during row-level logging,
    the exception is suppressed and normal CSV processing continues.
    """
    csv_data = (
        "product_id,product_name,quantity,price\n"
        "P1,Laptop,5,0\n"
    )

    mocker.patch.object(Path, "exists", return_value=True)

    csv_mock = mock_open(read_data=csv_data)

    def error_log_mock(*args, **kwargs):
        raise PermissionError("no write")

    def fake_open(self, mode="r", *args, **kwargs):
        if str(self).endswith("fake.csv") and "r" in mode:
            return csv_mock()
        if str(self).endswith("errors.log") and "a" in mode:
            return error_log_mock()
        return mock_open()()

    mocker.patch.object(Path, "open", fake_open)

    inv = Inventory()
    inv.load_products_from_csv("fake.csv")

    assert len(inv.products) == 0


