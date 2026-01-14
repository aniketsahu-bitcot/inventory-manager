"""
Comprehensive unit tests for Product SQLAlchemy models.
"""

from datetime import date, timedelta

from week6.models.product import (
    Product,
    FoodProduct,
    ElectronicProduct,
    BookProduct,
)


def test_product_creation_success()-> None:
    """Base Product can be created with valid data."""
    product = Product(
        product_id="p1",
        product_name="Generic Product",
        quantity=10,
        price=50.0,
        type="electronic",
        warranty_period=12,
    )

    assert product.product_id == "p1"
    assert product.quantity == 10
    assert product.price == 50.0


def test_product_total_value_calculation()-> None:
    """get_total_value returns quantity * price."""
    product = Product(
        product_id="p2",
        product_name="Value Test",
        quantity=4,
        price=25.5,
        type="book",
        author="Someone",
    )

    assert product.get_total_value() == 102.0


def test_product_zero_quantity_value()-> None:
    """Total value should be zero if quantity is zero."""
    product = Product(
        product_id="p3",
        product_name="Zero Quantity",
        quantity=0,
        price=99.9,
        type="electronic",
        warranty_period=6,
    )

    assert product.get_total_value() == 0.0


def test_food_product_valid_future_expiry()-> None:
    """FoodProduct accepts future expiry date."""
    product = FoodProduct(
        product_id="f1",
        product_name="Cheese",
        quantity=5,
        price=20.0,
        expiry_date=date.today() + timedelta(days=10),
    )

    assert product.expiry_date is not None
    assert product.type == "food"


def test_food_product_today_expiry_allowed()-> None:
    """FoodProduct allows expiry date equal to today."""
    product = FoodProduct(
        product_id="f2",
        product_name="Fresh Bread",
        quantity=1,
        price=15.0,
        expiry_date=date.today(),
    )

    assert product.expiry_date == date.today()


def test_food_product_without_expiry_python_level()-> None:
    """
    Python allows creation without expiry_date.
    DB constraint enforces this later.
    """
    product = FoodProduct(
        product_id="f4",
        product_name="Pending Expiry",
        quantity=3,
        price=12.0,
    )

    assert product.expiry_date is None



def test_book_product_valid_author()-> None:
    """BookProduct accepts non-empty author."""
    product = BookProduct(
        product_id="b1",
        product_name="Clean Code",
        quantity=2,
        price=500.0,
        author="Robert C. Martin",
    )

    assert product.author == "Robert C. Martin"
    assert product.type == "book"




def test_book_product_none_author_python_level()-> None:
    """
    Python allows author=None.
    DB constraint enforces author presence.
    """
    product = BookProduct(
        product_id="b3",
        product_name="Unknown Author",
        quantity=1,
        price=50.0,
    )

    assert product.author is None


def test_electronic_product_valid_warranty()-> None:
    """ElectronicProduct accepts positive warranty period."""
    product = ElectronicProduct(
        product_id="e1",
        product_name="Laptop",
        quantity=2,
        price=75000.0,
        warranty_period=24,
    )

    assert product.warranty_period == 24
    assert product.type == "electronic"


def test_electronic_product_without_warranty_python_level()-> None:
    """
    Python allows missing warranty_period.
    DB constraint enforces it.
    """
    product = ElectronicProduct(
        product_id="e2",
        product_name="TV",
        quantity=1,
        price=40000.0,
    )

    assert product.warranty_period is None


def test_polymorphic_identity_food()-> None:
    """FoodProduct has correct polymorphic identity."""
    product = FoodProduct(
        product_id="pf",
        product_name="Apple",
        quantity=5,
        price=3.0,
        expiry_date=date.today() + timedelta(days=3),
    )

    assert product.type == "food"


def test_polymorphic_identity_book()-> None:
    """BookProduct has correct polymorphic identity."""
    product = BookProduct(
        product_id="pb",
        product_name="Python Book",
        quantity=1,
        price=800.0,
        author="Author",
    )

    assert product.type == "book"


def test_polymorphic_identity_electronic()-> None:
    """ElectronicProduct has correct polymorphic identity."""
    product = ElectronicProduct(
        product_id="pe",
        product_name="Phone",
        quantity=1,
        price=30000.0,
        warranty_period=12,
    )

    assert product.type == "electronic"
