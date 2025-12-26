"""
Inventory Management System Demo Script

This script demonstrates the core functionality of the inventory management system,
including product creation (general, food, electronic, and book products), inventory
operations, CSV loading, low stock reporting, and product retrieval.

Key Features Demonstrated:
- Creating diverse product types with validation
- Adding products to inventory with duplicate detection
- Loading and validating products from CSV files
- Retrieving specific products by ID
- Generating low stock reports
- Calculating total product values

Usage:
    Run this script to see a complete workflow of inventory operations,
    including error handling and report generation.

Dependencies:
    - inventory_manager.models (Product, FoodProduct, ElectronicProduct, BookProduct)
    - inventory_manager.core (Inventory)
    - pathlib, datetime

Output:
    - Console output showing product details and operations
    - low_stock_report.txt (low stock products)
    - errors.log (any validation errors)

"""

from datetime import date
from pathlib import Path
from inventory_manager.models import (
    Product,
    FoodProduct,
    ElectronicProduct,
    BookProduct,
)
from inventory_manager.core import Inventory


product = Product("P001", "Laptop", 10, 999.99)
print(f"Total value of {product.product_name}: {product.get_total_value():.2f}")

milk = FoodProduct("F001", "Milk", 5, 40.0, expiry_date=date(2026, 1, 10))
phone = ElectronicProduct("E001", "Smartphone", 8, 29999.0, warranty_period=18)

inventory = Inventory()

book = BookProduct("B001", "Clean Code", 12, 499.0, author="Robert C. Martin")

try:
    inventory.add_product(product)
    inventory.add_product(milk)
    inventory.add_product(phone)
    inventory.add_product(book)
except ValueError as e:
    print(f"Error adding product: {e}")

csv_path = Path("inventory.csv")
try:
    inventory.load_and_validate_products(csv_path)
except FileNotFoundError as e:
    print(e)

try:
    inventory.add_product(Product("P010", "Monitor", 15, 199.99))
    inventory.add_product(Product("P011", "Headset", 30, 49.99))
except ValueError as e:
    print(f"Error adding product: {e}")

product = inventory.get_product("P010")
if product:
    print(
        f"Retrieved product: {product.product_name} - "
        f"Quantity: {product.quantity} - Price: {product.price}"
    )
else:
    print("Product not found.")

inventory.generate_low_stock_report(threshold=10)

print(f"\nProcessed {len(inventory.products)} valid products.")
print("Errors (if any) are logged in errors.log")
print("Low stock report generated: low_stock_report.txt")

print("\nAll products in inventory:")
for p in inventory.products:
    print(
        f"{p.product_id}: {p.product_name} - "
        f"Quantity: {p.quantity} - Total Value: {p.get_total_value():.2f}"
    )
