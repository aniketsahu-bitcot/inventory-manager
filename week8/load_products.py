"""Load products from the database and convert them into LangChain Document objects."""
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from langchain_core.documents import Document
from week7.models.product import Product
from week7.db.session import get_db


def load_products() -> list[Document]:
    """
    Load all products from the database and convert them into
    LangChain Document objects.
    """
    documents: list[Document] = []
    db: Session = None

    try:
        db = next(get_db())
        products = db.query(Product).all()

        for p in products:
            description = (
                f"Product name: {p.product_name}. "
                f"Price: {p.price}. "
                f"Quantity available: {p.quantity}."
            )

            if p.type == "food" and p.expiry_date:
                description += f" Expiry date: {p.expiry_date}."

            if p.type == "electronic" and p.warranty_period:
                description += f" Warranty period: {p.warranty_period} months."

            if p.type == "book" and p.author:
                description += f" Author: {p.author}."

            documents.append(
                Document(
                    page_content=description,
                    metadata={
                        "product_id": p.product_id,
                        "type": p.type,
                    },
                )
            )

    except SQLAlchemyError as e:
        
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if db:
            db.close()

    return documents
