"""
Inventory Management Demo

Demonstrates creation of products, inventory operations, CSV loading,
product retrieval, and low stock reporting.

Dependencies:
    - inventory_manager.models
    - inventory_manager.core
    - pathlib, datetime
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

product = Product(
    product_id="P001",
    product_name="Laptop",
    quantity=10,
    price=999.99,
)
print(f"Total value of {product.product_name}: {product.get_total_value():.2f}")

milk = FoodProduct(
    product_id="F001",
    product_name="Milk",
    quantity=5,
    price=40.0,
    expiry_date=date(2026, 1, 10),
)

phone = ElectronicProduct(
    product_id="E001",
    product_name="Smartphone",
    quantity=8,
    price=29999.0,
    warranty_period=18,
)

inventory = Inventory()

book = BookProduct(
    product_id="B001",
    product_name="Clean Code",
    quantity=12,
    price=499.0,
    author="Robert C. Martin",
)

try:
    inventory.add_product(product)
    inventory.add_product(milk)
    inventory.add_product(phone)
    inventory.add_product(book)
except ValueError as e:
    print(f"Error adding product: {e}")

csv_path = Path("inventory.csv")
try:
    inventory.load_products_from_csv(csv_path)
except FileNotFoundError as e:
    print(e)

try:
    inventory.add_product(Product(
        product_id="P010",
        product_name="Monitor",
        quantity=15,
        price=199.99,
    ))
    inventory.add_product(Product(
        product_id="P011",
        product_name="Headset",
        quantity=30,
        price=49.99,
    ))
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
