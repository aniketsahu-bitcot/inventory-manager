"""
Inventory Management Product Models

This module defines the core product classes for the inventory management system.
It provides a hierarchical structure with Product as the base class and specialized
subclasses for different product categories (Food, Electronic, Book).

Class Hierarchy:
    Product (base)
    ├── FoodProduct
    ├── ElectronicProduct
    └── BookProduct

Dependencies:
    - datetime.date (for expiry date validation)

Usage Example:
    product = Product("P001", "Laptop", 10, 999.99)
    food = FoodProduct("F001", "Milk", 5, 40.0, date(2026, 1, 10))
    total_value = product.get_total_value()  # Returns 9999.90
"""

from datetime import date


class Product:
    """Represents a product in the inventory.

    This class stores product data and provides basic calculation methods.

    Attributes:
        product_id (str): Unique identifier for the product.
        product_name (str): Name or description of the product.
        quantity (int): Available quantity in stock.
        price (float): Unit price of the product.
    """

    def __init__(
        self,
        product_id: str,
        product_name: str,
        quantity: int,
        price: float,
    ) -> None:
        """Initializes a Product instance with validation.

        Args:
            product_id (str): Unique identifier for the product.
            product_name (str): Name or description of the product.
            quantity (int): Available quantity in stock. Must be non-negative.
            price (float): Unit price of the product. Must be positive.

        Returns:
            None

        Raises:
            ValueError: If quantity or price is invalid.
        """
        if quantity < 0:
            raise ValueError("Quantity must be a non-negative integer")
        if price <= 0:
            raise ValueError("Price must be a positive number")

        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.price = price

    def get_total_value(self) -> float:
        """Calculates the total inventory value for a product.

        Returns:
            float: The total value computed as quantity * price.
        """
        return self.quantity * self.price


class FoodProduct(Product):
    """Represents a food product with an expiry date.

    Attributes:
        expiry_date (date): The product's expiry date.
    
    """

    def __init__(
        self,
        product_id: str,
        product_name: str,
        quantity: int,
        price: float,
        expiry_date: date,
    ) -> None:
        """Initializes a FoodProduct instance.

        Args:
            product_id (str): Unique identifier for the product.
            product_name (str): Name of the food product.
            quantity (int): Quantity in stock.
            price (float): Unit price.
            expiry_date (date): Expiry date of the food product.

        Returns:
            None    

        Raises:
            ValueError: If expiry_date is in the past.
        """
        super().__init__(product_id, product_name, quantity, price)

        if expiry_date < date.today():
            raise ValueError("Expiry date cannot be in the past.")

        self.expiry_date = expiry_date


class ElectronicProduct(Product):
    """Represents an electronic product with a warranty period.

    Attributes:
        warranty_period (int): Warranty period in months.
    """

    def __init__(
        self,
        product_id: str,
        product_name: str,
        quantity: int,
        price: float,
        warranty_period: int,
    ) -> None:
        """Initializes an ElectronicProduct instance.

        Args:
            product_id (str): Unique identifier for the product.
            product_name (str): Name of the electronic product.
            quantity (int): Quantity in stock.
            price (float): Unit price.
            warranty_period (int): Warranty duration in months.

        Returns:
             None    

        Raises:
            ValueError: If warranty_period is not positive.
        """
        super().__init__(product_id, product_name, quantity, price)

        if warranty_period <= 0:
            raise ValueError("Warranty period must be a positive number of months.")

        self.warranty_period = warranty_period


class BookProduct(Product):
    """Represents a book product with an author.

    This class extends the base Product class by adding
    book-specific attributes.

    Attributes:
        author (str): Name of the book's author.
    """

    def __init__(
        self,
        product_id: str,
        product_name: str,
        quantity: int,
        price: float,
        author: str,
    ) -> None:
        """Initializes a BookProduct instance.

        Args:
            product_id (str): Unique identifier for the product.
            product_name (str): Name or title of the book.
            quantity (int): Available quantity in stock. Must be non-negative.
            price (float): Unit price of the book. Must be positive.
            author (str): Name of the author.

        Returns:
             None    

        Raises:
            ValueError: If the author name is empty.
        """
        super().__init__(product_id, product_name, quantity, price)

        if not author:
            raise ValueError("Author name cannot be empty.")

        self.author = author
