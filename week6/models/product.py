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
    Index,
)

from week6.db.base import Base


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
        nullable=True,
        doc="Type of the product (e.g., 'food', 'electronic', 'book')",
    )

    expiry_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Expiry date for food products (must be set if type is 'food')",
    )

    warranty_period: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        doc="Warranty period in months for electronic products (must be set if type is 'electronic')",
    )

    author: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Author of the book (must be set if type is 'book')",
    )

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="ck_quantity_non_negative"),
        CheckConstraint("price > 0", name="ck_price_positive"),

        CheckConstraint(
            "(type != 'food') OR (expiry_date IS NOT NULL)",
            name="ck_food_requires_expiry_date",
        ),
        CheckConstraint(
            "(type != 'electronic') OR (warranty_period IS NOT NULL AND warranty_period > 0)",
            name="ck_electronic_requires_warranty",
        ),
        CheckConstraint(
            "(type != 'book') OR (author IS NOT NULL AND author <> '')",
            name="ck_book_requires_author",
        ),

        CheckConstraint(
            "type IN ('food', 'electronic', 'book')",
            name="ck_valid_product_type",
        ),
        
        Index("ix_products_type", "type"),
    )

    def get_total_value(self) -> float:
        """Calculate total value of the product stock."""
        return self.quantity * self.price

class FoodProduct(Product):
    """Food product model."""

    __mapper_args__ = {
        "polymorphic_identity": "food",
    }

    @validates("expiry_date")
    def validate_expiry_date(self, key: str, value: date | None) -> date | None:
        """Validate expiry date is not in the past."""
        if value is not None and value < date.today():
            raise ValueError("Expiry date cannot be in the past.")
        return value

class ElectronicProduct(Product):
    """Electronic product model."""

    __mapper_args__ = {
        "polymorphic_identity": "electronic",
    }

class BookProduct(Product):
    """Book product model."""

    __mapper_args__ = {
        "polymorphic_identity": "book",
    }

    @validates("author")
    def validate_author_not_empty(self, key: str, value: str | None) -> str | None:
        """Validate that author name is not empty."""
        if value is not None and not value.strip():
            raise ValueError("Author name cannot be empty.")
        return value
    

Product.__mapper_args__ = {
    "polymorphic_on": Product.type,
    "polymorphic_identity": "product",
    "polymorphic_map": {
        "food": FoodProduct,
        "electronic": ElectronicProduct,
        "book": BookProduct,
        None: Product,  
    },
}

