import csv
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError



class Product(BaseModel):
    product_id: str
    product_name: str
    quantity: int = Field(ge=0, description="Quantity must be a non-negative integer")
    price: float = Field(gt=0, description="Price must be a positive number")



def load_and_validate_products(csv_file_path: str):
    valid_products = []
    errors_file = Path("errors.log")

    
    errors_file.write_text("")

    with open(csv_file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row_number, row in enumerate(reader, start=2):
            try:
                product = Product(
                    product_id=row["product_id"],
                    product_name=row["product_name"],
                    quantity=row["quantity"],
                    price=row["price"],
                )
                valid_products.append(product)

            except ValidationError as e:
                with open(errors_file, "a", encoding="utf-8") as ef:
                    ef.write(f"Row {row_number} failed validation:\n")
                    for err in e.errors():
                        field = err["loc"][0]
                        message = err["msg"]
                        ef.write(f" - {field}: {message}\n")
                    ef.write("\n")

    return valid_products



def generate_low_stock_report(products, threshold=10, output_file="low_stock_report.txt"):
    low_stock_products = [p for p in products if p.quantity < threshold]

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Low Stock Report:\n")
       
        if not low_stock_products:
            f.write("All products have sufficient stock.\n")
        else:
            for p in low_stock_products:
                f.write(f"{p.product_name} - Quantity: {p.quantity}\n")



csv_path = "inventory.csv"  
products = load_and_validate_products(csv_path)
generate_low_stock_report(products, threshold=10)

print(f"Processed {len(products)} valid products.")
print("Errors (if any) are logged in errors.log")
print("Low stock report generated: low_stock_report.txt")


