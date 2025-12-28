"""Inventory Management Module.

Defines the `Inventory` class for managing `Product` objects, including CSV
loading, validation, and low-stock reporting.
"""

import csv
from pathlib import Path
from typing import Iterable
from typing import List
from inventory_manager.models import Product


class Inventory:
    """Manages a collection of Product objects.

    This class is responsible for operations that involve
    multiple products such as loading, storing, and reporting.

    Attributes:
        products (list[Product]): List of valid product objects.
    """

    products: List["Product"]

    def __init__(self) -> None:
        """Initialize the Inventory instance.

        Initializes a new Inventory object with an empty list of products.
        Products can be added later when loading from a CSV file or
        explicitly appended.

        Returns:
            None
        """

        self.products: List[Product] = []
        self._product_map: dict[str, Product] = {}         

    def add_product(self, product: "Product") -> None:
        """Add a product to the inventory.

        Args:
            product (Product): The Product object to add.

        Returns:
            None

        Raises:
            ValueError: If a product with the same ID already exists.
        """
        if product.product_id in self._product_map:
            raise ValueError(f"Product with ID '{product.product_id}' already exists.")
        self.products.append(product)
        self._product_map[product.product_id] = product

    def get_product(self, product_id: str) -> "Product | None":
        """Retrieve a product by its ID.

        Args:
            product_id (str): The unique identifier of the product.

        Returns:
            Product | None: The product if found; otherwise, None.
        """
        return self._product_map.get(product_id)



    def load_products_from_csv(self, csv_file_path: Path | str) -> None:
        """Load products from a CSV file and add them to the inventory.

        Invalid rows are logged to 'errors.log'.

        Args:
            csv_file_path (Path | str): Path to the CSV file.

        Raises:
            FileNotFoundError: If the CSV file does not exist.
            PermissionError: If unable to read CSV file or write errors.log.
            IOError: If other file I/O errors occur.
            ValueError: If the path value is not valid.
        """

        
        try:
            csv_file_path = Path(csv_file_path)
        except TypeError as e:
            raise ValueError("csv_file_path must be a valid path or string") from e

        
        if not csv_file_path.exists():
            raise FileNotFoundError(f"File not found: {csv_file_path}")

        errors_file = csv_file_path.parent / "errors.log"

        try:
            errors_file.write_text("", encoding="utf-8")
        except (PermissionError, OSError) as e:
            raise PermissionError(f"Cannot create/write {errors_file}: {e}") from e

        try:
            with csv_file_path.open("r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row_number, row in enumerate(reader, start=2):
                    try:
                        product = Product(
                            product_id=row["product_id"],
                            product_name=row["product_name"],
                            quantity=row["quantity"],
                            price=row["price"],
                        )
                        self.add_product(product)

                    except Exception as e:
                        try:
                            with errors_file.open("a", encoding="utf-8") as ef:
                                ef.write(f"Row {row_number} failed validation:\n")
                                ef.write(f" - {str(e)}\n\n")
                        except (PermissionError, OSError):
                            pass

        except (PermissionError, OSError) as e:
            raise PermissionError(f"Cannot read CSV file {csv_file_path}: {e}") from e


    def get_low_stock(self, threshold: int = 10) -> Iterable[Product]:
        """Return products with quantity below a defined threshold.

        Args:
            threshold (int, optional): Minimum acceptable quantity.
                Defaults to 10.

        Returns:
            Iterable[Product]: Products considered low in stock.
        """
        return (p for p in self.products if p.quantity < threshold)

    def generate_low_stock_report(
        self,
        threshold: int = 10,
        output_file: Path | str = "week3/low_stock_report.txt",
    ) -> None:
        """Generate a report listing products below the given stock threshold.

        Args:
            threshold (int, optional): Stock limit considered low.
                Defaults to 10.
            output_file (Path | str, optional): Output text file name.
                Defaults to 'low_stock_report.txt'.

        Returns:
            None
        """
        output_file = Path(output_file)
        low_stock_products = list(self.get_low_stock(threshold))

        with output_file.open("w", encoding="utf-8") as f:
            f.write("Low Stock Report:\n\n")

            if not low_stock_products:
                f.write("All products have sufficient stock.\n")
            else:
                for p in low_stock_products:
                    f.write(f"{p.product_name} - Quantity: {p.quantity}\n")
