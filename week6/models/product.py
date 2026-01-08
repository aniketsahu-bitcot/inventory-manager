"""
Inventory Product Database Models.

This module defines SQLAlchemy declarative models for inventory products.
It mirrors the Pydantic product models and persists them in a relational
database using joined-table inheritance.
"""

from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import (
    String,
    Integer,
    Float,
    Date,
    ForeignKey,
    CheckConstraint,
)

from db.base import Base


class Product(Base):
    """
    Represents a generic product stored in the inventory.
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
        """Calculate total inventory value for this product."""
        return self.quantity * self.price


class FoodProduct(Product):
    """
    Represents a food product with an expiry date.
    """

    __tablename__ = "food_products"

    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.product_id"),
        primary_key=True,
    )

    expiry_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    @validates("expiry_date")
    def validate_expiry_date(self, key: str, value: date) -> date:
        """Ensure expiry date is not in the past."""
        if value < date.today():
            raise ValueError("Expiry date cannot be in the past.")
        return value


class ElectronicProduct(Product):
    """
    Represents an electronic product with a warranty period.
    """

    __tablename__ = "electronic_products"

    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.product_id"),
        primary_key=True,
    )

    warranty_period: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Warranty period in months",
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
    """

    __tablename__ = "book_products"

    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.product_id"),
        primary_key=True,
    )

    author: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    @validates("author")
    def validate_author_not_empty(self, key: str, value: str) -> str:
        """Ensure author name is not empty."""
        if not value.strip():
            raise ValueError("Author name cannot be empty.")
        return value
