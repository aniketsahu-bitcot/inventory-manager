"""
Inventory Product Database Models.

This module defines SQLAlchemy declarative models for inventory products.
It mirrors the Pydantic product models and persists them in a relational
database using joined-table inheritance.
"""

from datetime import date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import validates
from sqlalchemy import (
    String,
    Integer,
    Float,
    Date,
    ForeignKey,
    CheckConstraint,
)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy declarative models.

    This class is used as the foundation for all ORM-mapped
    database models in the inventory system.
    """
    pass


class Product(Base):
    """
    Represents a generic product stored in the inventory.

    This model contains fields common to all product types
    and is mapped to the `products` database table.
    """

    __tablename__ = "products"

    product_id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
        doc="Unique identifier for the product",
    )

    product_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Name or description of the product",
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Available quantity in stock (non-negative)",
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        doc="Unit price of the product (positive)",
    )

    __table_args__ = (
        CheckConstraint(
            "quantity >= 0",
            name="ck_quantity_non_negative",
        ),
        CheckConstraint(
            "price > 0",
            name="ck_price_positive",
        ),
    )

    def get_total_value(self) -> float:
        """
        Calculate the total inventory value for this product.
        """
        return self.quantity * self.price


class FoodProduct(Product):
    """
    Represents a food product with an expiry date.

    This model extends the base Product model and is mapped
    to the `food_products` table.
    """

    __tablename__ = "food_products"

    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.product_id"),
        primary_key=True,
    )

    expiry_date: Mapped[date] = mapped_column(Date, nullable=False)

    @validates("expiry_date")
    def validate_expiry_date(self, key: str, value: date) -> date:
        """
        Ensure the expiry date is not in the past.
        """
        if value < date.today():
            raise ValueError("Expiry date cannot be in the past.")
        return value


class ElectronicProduct(Product):
    """
    Represents an electronic product with a warranty period.

    This model extends the base Product model and is mapped
    to the `electronic_products` table.
    """

    __tablename__ = "electronic_products"

    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.product_id"),
        primary_key=True,
        doc="Reference to the base product ID",
    )

    warranty_period: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Warranty period in months (positive integer)",
    )

    __table_args__ = (
        CheckConstraint(
            "warranty_period > 0",
            name="ck_warranty_positive",
        ),
    )



class BookProduct(Product):
    """
    Represents a book product with an author.

    This model extends the base Product model and is mapped
    to the `book_products` table.
    """

    __tablename__ = "book_products"

    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.product_id"),
        primary_key=True,
        doc="Reference to the base product ID",
    )

    author: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Name of the book's author",
    )

    @validates("author")
    def validate_author_not_empty(self, key: str, value: str) -> str:
        """
        Ensure the author name is not empty or just whitespace.
        """
        if not value.strip():
            raise ValueError("Author name cannot be empty.")
        return value
