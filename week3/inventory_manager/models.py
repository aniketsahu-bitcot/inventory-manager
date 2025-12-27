"""Inventory Product Models.

Defines the base Product class and specialized subclasses (FoodProduct,
ElectronicProduct, and BookProduct) with validation and utility methods.
"""

from datetime import date
from pydantic import BaseModel, Field, field_validator


class Product(BaseModel):
    """Represents a product in the inventory.

    Attributes:
        product_id (str): Unique identifier for the product.
        product_name (str): Name or description of the product.
        quantity (int): Available quantity in stock (non-negative).
        price (float): Unit price of the product (positive).
    """

    product_id: str
    product_name: str
    quantity: int = Field(ge=0, description="Quantity must be a non-negative integer")
    price: float = Field(gt=0, description="Price must be a positive number")

    @field_validator("quantity")
    @classmethod
    def validate_quantity_non_negative(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Quantity cannot be negative.")
        return value

    @field_validator("price")
    @classmethod
    def validate_price_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Price must be greater than zero.")
        return value

    def get_total_value(self) -> float:
        """Calculate total inventory value for this product.

        Returns:
            float: Total value computed as quantity * price.
        """
        return self.quantity * self.price


class FoodProduct(Product):
    """Represents a food product with an expiry date.

    Attributes:
        expiry_date (date): Expiry date of the food product.
    """

    expiry_date: date

    @field_validator("expiry_date")
    @classmethod
    def validate_expiry_not_past(cls, expiry_date: date) -> date:
        """Ensure the expiry date is not in the past.

        Args:
            expiry_date (date): The expiry date to validate.

        Returns:
            date: The same expiry date if valid.

        Raises:
            ValueError: If the expiry date is in the past.
        """
        if expiry_date < date.today():
            raise ValueError("Expiry date cannot be in the past.")
        return expiry_date


class ElectronicProduct(Product):
    """Represents an electronic product with a warranty period.

    Attributes:
        warranty_period (int): Warranty period in months (positive).
    """

    warranty_period: int = Field(
        gt=0,
        description="Warranty period must be a positive number of months",
    )


class BookProduct(Product):
    """Represents a book product with an author.

    Attributes:
        author (str): Name of the book's author (non-empty).
    """

    author: str

    @field_validator("author")
    @classmethod
    def validate_author_not_empty(cls, author: str) -> str:
        """Ensure the author name is not empty.

        Args:
            author (str): The author name to validate.

        Returns:
            str: The same author name if valid.

        Raises:
            ValueError: If the author name is empty.
        """
        if not author.strip():
            raise ValueError("Author name cannot be empty.")
        return author
