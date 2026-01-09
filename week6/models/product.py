"""
Inventory Product Database Models.

This module defines SQLAlchemy declarative models for inventory products.
It uses SINGLE-TABLE INHERITANCE.
"""

from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import (
    String,
    Integer,
    Float,
    Date,
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
        doc="Unit price of the product (positive value)",
    )

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        doc="Type of the product for polymorphic identity",
    )

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="ck_quantity_non_negative"),
        CheckConstraint("price > 0", name="ck_price_positive"),
    )

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "product",
    }

    def get_total_value(self) -> float:
        """Return the total value of this product based on quantity and unit price."""
 
        return self.quantity * self.price


class FoodProduct(Product):
    """
    Represents a food product with an expiry date.
    """

    expiry_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    __mapper_args__ = {
        "polymorphic_identity": "food",
    }

    @validates("expiry_date")
    def validate_expiry_date(self, key: str, value: date) -> date:
        """Validate that the expiry date is not in the past."""
        if value < date.today():
            raise ValueError("Expiry date cannot be in the past.")
        return value


class ElectronicProduct(Product):
    """
    Represents an electronic product with a warranty period.
    """

    warranty_period: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Warranty period in months",
    )

    __mapper_args__ = {
        "polymorphic_identity": "electronic",
    }

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

    author: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Author of the book",
    )

    __mapper_args__ = {
        "polymorphic_identity": "book",
    }

    @validates("author")
    def validate_author_not_empty(self, key: str, value: str) -> str:
        """Validate that the author name is not empty."""
        if not value.strip():
            raise ValueError("Author name cannot be empty.")
        return value
