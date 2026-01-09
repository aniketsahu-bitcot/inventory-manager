"""
Inventory API routes using SQLAlchemy ORM (Task 1).

CRUD endpoints for products using direct SQLAlchemy sessions.
No Pydantic schemas are used yet; responses and requests are raw dictionaries.
"""

from fastapi import APIRouter, HTTPException, status, Depends, Body
from typing import List
from sqlalchemy.orm import Session
from week6.models.product import Product
from week6.db.dependencies import get_db

router = APIRouter()

@router.get("/products", response_model=None)
def list_products(db: Session = Depends(get_db)) -> List[dict]:
    """
    Retrieve all products as a list of dictionaries.
    """
    products = db.query(Product).all()
    return [product.__dict__ for product in products]


@router.get("/products/{product_id}", response_model=None)
def get_product(product_id: str, db: Session = Depends(get_db)) -> dict:
    """
    Retrieve a single product by its product_id.
    """
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.__dict__


@router.post("/products", response_model=None, status_code=status.HTTP_201_CREATED)
def create_product(product_data: dict = Body(...), db: Session = Depends(get_db)) -> dict:
    """
    Create a new product from a dictionary of attributes.
    """
    existing = db.query(Product).filter(Product.product_id == product_data.get("product_id")).first()
    if existing:
        raise HTTPException(status_code=409, detail="Product with this ID already exists")

    product = Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product.__dict__


@router.put("/products/{product_id}", response_model=None)
def update_product(product_id: str, updated_data: dict = Body(...), db: Session = Depends(get_db)) -> dict:
    """
    Update an existing product with new data from a dictionary.
    """
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if "product_id" in updated_data and updated_data["product_id"] != product_id:
        raise HTTPException(status_code=400, detail="Product ID in path and body must match")

    for key, value in updated_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product.__dict__
