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

book = BookProduct(
    product_id="B001",
    product_name="Clean Code",
    quantity=12,
    price=499.0,
    author="Robert C. Martin",
)



try:
    
    inventory = Inventory()
    
    
    inventory.add_product(product)
    inventory.add_product(milk)
    inventory.add_product(phone)
    inventory.add_product(book)
    
    
    csv_path = Path("inventory.csv")
    try:
        inventory.load_products_from_csv(csv_path)
    except Exception:
        print(f"CSV optional load skipped: {csv_path}")
    
    
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
    
    
    retrieved = inventory.get_product("P010")
    print(
        f"Retrieved product: {retrieved.product_name} - "
        f"Quantity: {retrieved.quantity} - Price: {retrieved.price}"
    )
    
    
    inventory.generate_low_stock_report(threshold=10)

except Exception as e:
    print(f"Demo failed: {e}")

else:
    print(f"\nProcessed {len(inventory.products)} valid products.")
    print("Low stock report generated: low_stock_report.txt")

    print("\nAll products in inventory:")
    for p in inventory.products:
        print(
            f"{p.product_id}: {p.product_name} - "
            f"Quantity: {p.quantity} - Total Value: {p.get_total_value():.2f}"
        )

