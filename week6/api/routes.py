"""
Inventory API routes using SQLAlchemy ORM.

CRUD endpoints for products using validated Pydantic schemas
and safe ORM serialization.
"""

from week6.db.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from week6.models.product import Product
from week6.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductRead,
)

router = APIRouter()


@router.get("/products", response_model=List[ProductRead])
def list_products(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> List[Product]:
    """List products with pagination."""
    offset = (page - 1) * size
    return db.query(Product).offset(offset).limit(size).all()



@router.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: str, db: Session = Depends(get_db)) -> Product:
    """Retrieve a single product by ID."""
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post(
    "/products",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
) -> Product:
    """Create a new product in the inventory."""
    existing = (
        db.query(Product)
        .filter(Product.product_id == data.product_id)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Product with this ID already exists",
        )

    try:
        product = Product(**data.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create product: {str(exc)}",
        )


@router.put("/products/{product_id}", response_model=ProductRead)
def update_product(
    product_id: str,
    data: ProductUpdate,
    db: Session = Depends(get_db),
) -> Product:
    """Update an existing product in the inventory."""
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = data.model_dump(exclude_unset=True)

    try:
        for field, value in update_data.items():
            setattr(product, field, value)

        db.commit()
        db.refresh(product)
        return product

    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Failed to update product: {str(exc)}",
        )
