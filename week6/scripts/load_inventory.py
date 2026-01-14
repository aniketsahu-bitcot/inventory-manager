"""Script to load inventory data from a CSV file into the database."""
import csv
import logging
from pathlib import Path
from sqlalchemy.exc import IntegrityError
from week6.db.session import SessionLocal
from week6.models.product import Product

logging.basicConfig(level=logging.INFO)

BASE_DIR = Path(__file__).resolve().parents[2]  
CSV_FILE = BASE_DIR / "week3" / "inventory.csv"


def safe_int(value: str | None) -> int | None:
    """Convert a string to an integer safely."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def safe_float(value: str | None) -> float | None:
    """Convert a string to a float safely."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def main() -> None:
    """Load inventory data from CSV file into the database."""
    db = SessionLocal()
    inserted = 0

    with CSV_FILE.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            quantity = safe_int(row.get("quantity"))
            price = safe_float(row.get("price"))

            if quantity is None or quantity < 0:
                logging.warning("Skipping row due to invalid quantity: %s", row)
                continue

            if price is None or price <= 0:
                logging.warning("Skipping row due to invalid price: %s", row)
                continue

            product = Product(
                product_id=row["product_id"],
                product_name=row["product_name"],
                quantity=quantity,
                price=price,
                type=None,  
            )

            db.add(product)

            try:
                db.commit()
                inserted += 1
            except IntegrityError:
                db.rollback()
                logging.warning(
                    "Skipping duplicate product_id: %s", row["product_id"]
                )

    db.close()
    logging.info("Inventory loading completed. Total inserted: %d", inserted)


if __name__ == "__main__":
    main()
