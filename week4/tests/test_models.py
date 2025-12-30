"""
This module contains unit tests for the Product model. It verifies correct
initialization, total value calculation, and validation behavior for invalid
inputs. All tests use the Product class from the inventory_manager package.
"""

import pytest
from pydantic import ValidationError
from week3.inventory_manager.models import Product


def test_create_product_initialization() -> None:
    """Test that a Product initializes with the expected attribute values.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        AssertionError: If any attribute does not match the expected value.
    """
    product = Product(product_id="P1", product_name="Laptop", quantity=5, price=1000.0)

    assert product.product_id == "P1"
    assert product.product_name == "Laptop"
    assert product.quantity == 5
    assert product.price == 1000.0


def test_create_product_with_long_name() -> None:
    """Verify that a Product accepts a long product_name value.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        AssertionError: If the stored product_name does not match the expected value.
    """
    long_name = "A" * 255
    product = Product(product_id="P4", product_name=long_name, quantity=10, price=99.99)

    assert product.product_name == long_name


def test_create_product_with_large_quantity() -> None:
    """Verify that a Product can store a very large quantity value.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        AssertionError: If the quantity or price values do not match the expected values.
    """
    product = Product(
        product_id="P3", product_name="Notebook", quantity=10_000_000, price=2.5
    )

    assert product.quantity == 10_000_000
    assert product.price == 2.5


def test_create_product_with_whitespace_name() -> None:
    """Verify behavior when a Product is created with surrounding whitespace in the name.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        AssertionError: If the stored product_name does not match the expected behavior.
    """
    product = Product(product_id="P5", product_name="   Chair   ", quantity=3, price=500.0)

    assert product.product_name.strip() == "Chair" or product.product_name == "   Chair   "


def test_create_product_with_large_price() -> None:
    """Verify that a Product supports a very large price value.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        AssertionError: If the price does not match the expected value.
    """
    product = Product(product_id="P8", product_name="Diamond", quantity=1, price=1_000_000.0)

    assert product.price == 1_000_000.0


def test_create_product_minimum_valid_quantity() -> None:
    """Verify that a Product accepts the minimum valid quantity value (zero).

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        AssertionError: If the stored quantity does not match the expected value.
    """
    product = Product(product_id="P6", product_name="Bottle", quantity=0, price=50.0)

    assert product.quantity == 0


def test_create_product_minimum_valid_price() -> None:
    """Verify that a Product accepts the minimum valid positive price value.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        AssertionError: If the stored price does not match the expected value.
    """
    product = Product(product_id="P7", product_name="Pencil", quantity=1, price=0.01)

    assert product.price == 0.01


def test_create_product_with_negative_quantity() -> None:
    """Ensure that creating a Product with a negative quantity raises a ValidationError.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        ValidationError: Because quantity must be non-negative.
    """
    with pytest.raises(ValidationError):
        Product(product_id="E1", product_name="Table", quantity=-1, price=100.0)


def test_create_product_with_negative_price() -> None:
    """Ensure that creating a Product with a negative price raises a ValidationError.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        ValidationError: Because price must be positive.
    """
    with pytest.raises(ValidationError):
        Product(product_id="E2", product_name="Phone", quantity=1, price=-10.0)


def test_create_product_with_zero_price() -> None:
    """Ensure that creating a Product with a zero price raises a ValidationError.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        ValidationError: Because price must be greater than zero.
    """
    with pytest.raises(ValidationError):
        Product(product_id="E3", product_name="Cable", quantity=5, price=0.0)


def test_create_product_with_missing_product_id() -> None:
    """Ensure that missing product_id raises a ValidationError.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        ValidationError: Because product_id is required.
    """
    with pytest.raises(ValidationError):
        Product(product_name="Book", quantity=2, price=200.0)  


def test_create_product_with_missing_name() -> None:
    """Ensure that missing product_name raises a ValidationError.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        ValidationError: Because product_name is required.
    """
    with pytest.raises(ValidationError):
        Product(product_id="E4", quantity=2, price=200.0)  


def test_create_product_with_invalid_quantity_type() -> None:
    """Ensure that providing a non-integer quantity raises a ValidationError.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        ValidationError: Because quantity must be an integer.
    """
    with pytest.raises(ValidationError):
        Product(product_id="E5", product_name="Mouse", quantity="five", price=500.0)  


def test_create_product_with_invalid_price() -> None:
    """Ensure that providing a non-numeric price raises a ValidationError.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        ValidationError: Because price must be numeric.
    """
    with pytest.raises(ValidationError):
        Product(product_id="E6", product_name="Keyboard", quantity=2, price="free")  


def test_product_with_invalid_quantity() -> None:
    """Test that a negative quantity raises a ValidationError.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        ValidationError: Raised by Pydantic when quantity is invalid.
    """
    with pytest.raises(ValidationError):
        Product(product_id="P5", product_name="Keyboard", quantity=-1, price=100)


def test_product_raises_error_for_zero_or_negative_price() -> None:
    """Test that zero or negative price values raise a ValidationError.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        ValidationError: When price is zero or negative.
    """
    with pytest.raises(ValidationError):
        Product(product_id="P8", product_name="Monitor", quantity=5, price=0.0)

    with pytest.raises(ValidationError):
        Product(product_id="P9", product_name="Monitor", quantity=5, price=-50.0)

def test_get_total_value() -> None:
    """Test total value calculation for a normal quantity and price.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        AssertionError: If the computed total value is not correct.
    """
    product = Product(product_id="P1", product_name="Laptop", quantity=2, price=500.0)

    assert product.get_total_value() == 1000.0


def test_get_total_value_with_zero_quantity() -> None:
    """Test that total value is zero when quantity is zero.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        AssertionError: If the computed value is not zero.
    """
    product = Product(product_id="P2", product_name="Mouse", quantity=0, price=200.0)

    assert product.get_total_value() == 0.0


def test_get_total_value_with_large_quantity_and_price() -> None:
    """Test total value when both quantity and price are large.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        AssertionError: If the total value is incorrect.
    """
    product = Product(
        product_id="P2", product_name="Desktop", quantity=10, price=1500.0
    )

    assert product.get_total_value() == 15000.0


def test_get_total_value_with_small_price() -> None:
    """Test total value calculation when using a very small price value.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        AssertionError: If the total value computation is inaccurate.
    """
    product = Product(product_id="P3", product_name="Pen", quantity=10, price=0.01)

    assert product.get_total_value() == 0.1


def test_get_total_value_large_quantity_small_price() -> None:
    """Test total value with a large quantity and small price.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        AssertionError: If the total value is incorrect.
    """
    product = Product(
        product_id="P10", product_name="Sticker", quantity=1000, price=0.05
    )

    assert product.get_total_value() == 50.0


def test_get_total_value_with_minimum_quantity_and_small_price() -> None:
    """Test total value when quantity is zero and price is small.

    Args:
        None: This function does not take any parameters.

    Returns:
        None: This function does not return a value. Assertions validate behavior.

    Raises:
        AssertionError: If the total is not zero.
    """
    product = Product(product_id="P4", product_name="Book", quantity=0, price=0.01)

    assert product.get_total_value() == 0.0


