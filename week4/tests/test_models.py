"""
This module contains unit tests for the Product model. It verifies correct
initialization, total value calculation, and validation behavior for invalid
inputs. All tests use the Product class from the inventory_manager package.
"""

import pytest
from typing import Dict, Any
from pydantic import ValidationError
from datetime import date
from week3.inventory_manager.models import (
    Product,
    ElectronicProduct,
    FoodProduct,
    BookProduct,
)

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


def test_Product_creation(
    valid_product_data: Dict[str, Any]
) -> None:
    """Validate successful Product creation with valid data."""

    data = valid_product_data
    product = Product(
        product_id=data["product_id"],
        product_name=data["product_name"],
        quantity=data["quantity"],
        price=data["price"],
    )

    assert product.product_id == data["product_id"]
    assert product.product_name == data["product_name"]
    assert product.quantity == data["quantity"]
    assert product.price == data["price"]

def test_Product_creation_large_values(
    edge_large_values_data: Dict[str, Any]
) -> None:
    """Validate Product creation with edge large values."""

    data = edge_large_values_data
    product = Product(
        product_id=data["product_id"],
        product_name=data["product_name"],
        quantity=data["quantity"],
        price=data["price"],
    )

    assert product.quantity == 1_000_000
    assert product.price == 123456.789

def test_Product_creation_missing_name(
    missing_name_data: Dict[str, Any]
) -> None:
    """Ensure missing required field raises ValidationError."""

    data = missing_name_data
    with pytest.raises(ValidationError):
        Product(
            product_id=data["product_id"],
            quantity=data["quantity"],
            price=data["price"],
        )

def test_Product_creation_negative_quantity(
    negative_quantity_data: Dict[str, Any]
) -> None:
    """Ensure negative quantity raises ValidationError."""

    data = negative_quantity_data
    with pytest.raises(ValidationError):
        Product(
            product_id=data["product_id"],
            product_name=data["product_name"],
            quantity=data["quantity"],
            price=data["price"],
        )

def test_Product_creation_zero_price(
    zero_price_data: Dict[str, Any]
) -> None:
    """Ensure zero price raises ValidationError."""

    data = zero_price_data
    with pytest.raises(ValidationError):
        Product(
            product_id=data["product_id"],
            product_name=data["product_name"],
            quantity=data["quantity"],
            price=data["price"],
        )

def test_Product_creation_minimum_valid_values(
    boundary_minimum_values_data: Dict[str, Any]
) -> None:
    """Validate Product creation at boundary valid limits."""

    data = boundary_minimum_values_data
    product = Product(
        product_id=data["product_id"],
        product_name=data["product_name"],
        quantity=data["quantity"],
        price=data["price"],
    )

    assert product.quantity == 0
    assert product.price == 0.01


def test_get_product_total_value(product_laptop: Product) -> None:
    """Verify total value calculation for a product with positive quantity."""
    product: Product = product_laptop
    total_value: float = product.get_total_value()
    assert total_value == product.quantity * product.price


def test_get_product_total_value_zero_quantity(product_zero_qty: Product) -> None:
    """Verify total value is zero for a product with zero quantity."""
    product: Product = product_zero_qty
    total_value: float = product.get_total_value()
    assert total_value == 0


def test_get_product_total_value_large_quantity(product_large_qty: Product) -> None:
    """Verify total value calculation for a product with very large quantity."""
    product: Product = product_large_qty
    total_value: float = product.get_total_value()
    assert total_value == product.quantity * product.price


def test_get_product_total_value_min_price(product_min_price: Product) -> None:
    """Verify total value calculation for a product with minimal positive price."""
    product: Product = product_min_price
    total_value: float = product.get_total_value()
    assert total_value == product.quantity * product.price


def test_get_product_total_value_single_unit(product_single_qty: Product) -> None:
    """Verify total value calculation for a product with quantity equal to one."""
    product: Product = product_single_qty
    total_value: float = product.get_total_value()
    assert total_value == product.price


def test_electronic_product_creation_standard(electronic_tv: ElectronicProduct) -> None:
    """Test standard ElectronicProduct creation."""
  
    device = electronic_tv

    total_value = device.get_total_value()

    assert device.warranty_period == 24
    assert total_value == 4500.0


def test_electronic_product_creation_one_month_warranty(electronic_product_with_one_month_warranty: ElectronicProduct) -> None:
    """Test ElectronicProduct with one month warranty."""
   
    device = electronic_product_with_one_month_warranty

   
    assert device.warranty_period == 1
    assert device.quantity == 5

def test_electronic_product_creation_invalid_zero_warranty(invalid_electronic_zero_warranty_data: dict) -> None:
    """Test ElectronicProduct creation with zero warranty raises ValueError."""
  
    data = invalid_electronic_zero_warranty_data

    with pytest.raises(ValueError):
        ElectronicProduct(
            product_id=data["product_id"],
            product_name=data["product_name"],
            quantity=data["quantity"],
            price=data["price"],
            warranty_period=data["warranty_period"]
        )


def test_electronic_product_creation_large_warranty(electronic_product_with_large_warranty: ElectronicProduct) -> None:
    """Test ElectronicProduct creation with large warranty period."""

    device = electronic_product_with_large_warranty
 
    assert device.warranty_period == 120
    assert device.price == 100.0


def test_electronic_product_total_value_positive_quantity(electronic_tv: ElectronicProduct) -> None:
    """Verify total value calculation for an electronic product with positive quantity."""
    product: ElectronicProduct = electronic_tv
    total_value: float = product.get_total_value()
    assert total_value == product.quantity * product.price
    assert product.warranty_period == 24


def test_electronic_product_total_value_zero_quantity(electronic_product_with_one_month_warranty: ElectronicProduct) -> None:
    """Verify total value calculation for electronic product with small quantity."""
    product: ElectronicProduct = electronic_product_with_one_month_warranty
    total_value: float = product.get_total_value()
    assert total_value == product.quantity * product.price
    assert product.warranty_period == 1


def test_electronic_product_high_price_low_quantity(electronic_product_with_high_price_low_quantity: ElectronicProduct) -> None:
    """Verify total value calculation for high price, low quantity electronic product."""
    product: ElectronicProduct = electronic_product_with_high_price_low_quantity
    total_value: float = product.get_total_value()
    assert total_value == product.quantity * product.price
    assert product.warranty_period == 36


def test_electronic_product_large_warranty(electronic_product_with_large_warranty: ElectronicProduct) -> None:
    """Verify electronic product with a large warranty period."""
    product: ElectronicProduct = electronic_product_with_large_warranty
    total_value: float = product.get_total_value()
    assert total_value == product.quantity * product.price
    assert product.warranty_period == 120


def test_food_product_creation_standard(food_bread: FoodProduct) -> None:
    """Test standard FoodProduct creation."""
   
    product = food_bread
   
    total_value = product.get_total_value()

    assert product.product_name == "Bread"
    assert product.quantity == 20
    assert total_value == 50.0
    assert product.expiry_date > date.today()


def test_food_product_creation_future_expiry(food_cheese: FoodProduct) -> None:
    """Test FoodProduct creation with future expiry date."""
    
    product = food_cheese
    
   
    assert product.expiry_date > date.today()

def test_food_product_creation_past_expiry(invalid_food_past_expiry_data: dict) -> None:
    """Test FoodProduct creation with past expiry should raise ValueError."""
    
    data = invalid_food_past_expiry_data

   
    with pytest.raises(ValueError):
        FoodProduct(
            product_id=data["product_id"],
            product_name=data["product_name"],
            quantity=data["quantity"],
            price=data["price"],
            expiry_date=data["expiry_date"]
        )


def test_food_product_creation_min_price(food_min_price: FoodProduct) -> None:
    """Test FoodProduct creation with minimal price and quantity."""
    
    product = food_min_price

    
    assert product.price == 0.01
    assert product.quantity == 1

def test_food_product_creation_negative_price(invalid_food_negative_price_data: dict) -> None:
    """Verify creating food product with negative price raises ValidationError."""
    with pytest.raises(ValidationError):
        FoodProduct(
            product_id=invalid_food_negative_price_data["product_id"],
            product_name=invalid_food_negative_price_data["product_name"],
            quantity=invalid_food_negative_price_data["quantity"],
            price=invalid_food_negative_price_data["price"],
            expiry_date=invalid_food_negative_price_data["expiry_date"]
        )


def test_food_product_creation_negative_quantity(invalid_food_negative_quantity_data: dict) -> None:
    """Verify creating food product with negative quantity raises ValidationError."""
    with pytest.raises(ValidationError):
        FoodProduct(
            product_id=invalid_food_negative_quantity_data["product_id"],
            product_name=invalid_food_negative_quantity_data["product_name"],
            quantity=invalid_food_negative_quantity_data["quantity"],
            price=invalid_food_negative_quantity_data["price"],
            expiry_date=invalid_food_negative_quantity_data["expiry_date"]
        )



def test_food_product_total_value_valid_expiry(food_bread: FoodProduct) -> None:
    """Verify total value for a food product with future expiry."""
    product: FoodProduct = food_bread
    total_value: float = product.get_total_value()
    assert total_value == product.quantity * product.price
    assert product.expiry_date > date.today()


def test_food_product_get_total_value_zero_quantity(food_zero_quantity: FoodProduct) -> None:
    """Verify total value is zero when food product quantity is zero."""
    product: FoodProduct = food_zero_quantity
    total_value: float = product.get_total_value()
    assert total_value == 0


def test_food_product_get_total_value_large_quantity(food_large_quantity: FoodProduct) -> None:
    """Verify total value calculation for food product with very large quantity."""
    product: FoodProduct = food_large_quantity
    total_value: float = product.get_total_value()
    assert total_value == product.quantity * product.price


def test_food_product_get_total_value_min_price(food_min_price: FoodProduct) -> None:
    """Verify total value for food product with minimal positive price."""
    product: FoodProduct = food_min_price
    total_value: float = product.get_total_value()
    assert total_value == product.quantity * product.price


def test_food_product_get_total_value_single_quantity(food_single_quantity: FoodProduct) -> None:
    """Verify total value for food product with quantity equal to one."""
    product: FoodProduct = food_single_quantity
    total_value: float = product.get_total_value()
    assert total_value == product.price

def test_food_product_expiry_today(food_expiry_today: FoodProduct) -> None:
    """Verify food product with expiry date today is valid."""
    product: FoodProduct = food_expiry_today
    total_value: float = product.get_total_value()
    assert total_value == product.quantity * product.price
    assert product.expiry_date == date.today()


def test_book_product_creation_standard(book_python: BookProduct) -> None:
    """Test standard BookProduct creation."""
  
    book = book_python

    total_value = book.get_total_value()

    assert book.author == "Mark Lutz"
    assert total_value == 320.0


def test_book_product_creation_missing_author(book_min_price: BookProduct) -> None:
    """Test BookProduct creation with default author (edge case)."""
   
    book = book_min_price

  
    assert book.author == "Unknown"
    assert book.price == 0.01

def test_book_product_creation_negative_price(invalid_book_negative_price_data: dict) -> None:
    """Verify creating a book with negative price raises ValidationError."""
    with pytest.raises(ValidationError):
        BookProduct(
            product_id=invalid_book_negative_price_data["product_id"],
            product_name=invalid_book_negative_price_data["product_name"],
            quantity=invalid_book_negative_price_data["quantity"],
            price=invalid_book_negative_price_data["price"],
            author="Unknown"
        )


def test_book_product_creation_invalid_negative_quantity(invalid_book_negative_qty_data: dict) -> None:
    """Test BookProduct creation with negative quantity raises ValueError."""
   
    data = invalid_book_negative_qty_data
  
    with pytest.raises(ValueError):
        BookProduct(
            product_id=data["product_id"],
            product_name=data["product_name"],
            quantity=data["quantity"],
            price=data["price"],
            author="Test Author"
        )


def test_book_product_creation_single_quantity(book_single_qty: BookProduct) -> None:
    """Test BookProduct creation with quantity equal to one."""
  
    book = book_single_qty

    assert book.quantity == 1
    assert book.price == 10.0

def test_book_author_creation_standard(book_python: BookProduct) -> None:
    """Test standard BookProduct creation with valid author."""

    book = book_python

    author_name = book.author

    assert author_name == "Mark Lutz"


def test_book_author_creation_whitespace(book_single_qty: BookProduct) -> None:
    """Test BookProduct creation with author having leading/trailing spaces."""
 
    book = BookProduct(
        product_id=book_single_qty.product_id,
        product_name=book_single_qty.product_name,
        quantity=book_single_qty.quantity,
        price=book_single_qty.price,
        author="  John Doe  "
    )

    author_name = book.author

    assert author_name == "  John Doe  "

def test_book_author_creation_empty_string() -> None:
    """Test BookProduct creation with empty author string raises ValueError."""
   
    product_id = "B050"
    product_name = "Some Book"
    quantity = 1
    price = 10.0
    author = ""

    def create_book() -> BookProduct:
        return BookProduct(
            product_id=product_id,
            product_name=product_name,
            quantity=quantity,
            price=price,
            author=author
        )

    import pytest
    with pytest.raises(ValueError):
        create_book()


def test_book_author_creation_single_character() -> None:
    """Test BookProduct creation with a single-character author name."""
   
    book = BookProduct(
        product_id="B051",
        product_name="Tiny Book",
        quantity=1,
        price=5.0,
        author="A"
    )
 
    author_name = book.author
   
    assert author_name == "A"


def test_book_product_get_total_value(book_python: BookProduct) -> None:
    """Verify total value calculation for a book product."""
    product: BookProduct = book_python
    total_value: float = product.get_total_value()
    assert total_value == product.quantity * product.price
    assert product.author == "Mark Lutz"


def test_book_product_get_total_value_zero_quantity(book_zero_qty: BookProduct) -> None:
    """Verify total value is zero when book quantity is zero."""
    product: BookProduct = book_zero_qty
    total_value: float = product.get_total_value()
    assert total_value == 0


def test_book_product_get_total_value_large_quantity(book_large_qty: BookProduct) -> None:
    """Verify total value calculation for a book with large quantity."""
    product: BookProduct = book_large_qty
    total_value: float = product.get_total_value()
    assert total_value == product.quantity * product.price


def test_book_product_get_total_value_min_price(book_min_price: BookProduct) -> None:
    """Verify total value calculation for a book with minimal positive price."""
    product: BookProduct = book_min_price
    total_value: float = product.get_total_value()
    assert total_value == pytest.approx(product.price)


def test_book_product_get_total_value_single_unit(book_single_qty: BookProduct) -> None:
    """Verify total value calculation for a book with quantity equal to one."""
    product: BookProduct = book_single_qty
    total_value: float = product.get_total_value()
    assert total_value == product.price



