"""
Inventory API routes.

This module defines the FastAPI API router and implements CRUD endpoints for managing products in the inventory.
It integrates the existing `inventory_manager` package which handles all inventory operations.
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from pathlib import Path
from week3.inventory_manager.core import Inventory
from week3.inventory_manager.models import Product

router = APIRouter()

inventory = Inventory()

inventory.load_products_from_csv(Path("week3/inventory.csv"))


@router.get("/products", response_model=List[Product])
def list_products() -> List[Product]:
    """
    Retrieve the full list of products in the inventory.
    """
    return inventory.products


@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: str) -> Product:
    """
    Retrieve a single product by its unique product ID.
    """
    product = inventory.get_product(product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product



@router.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: Product) -> Product:
    """
    Create a new product in the inventory.
    """

    try:
        inventory.add_product(product)
    except ValueError as e:

        if "already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e),
            )
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return product

@router.put("/products/{product_id}", response_model=Product)
def update_product(product_id: str, updated: Product) -> Product:
    """
    Update an existing product in the inventory.
    """
    existing = inventory.get_product(product_id)

    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    if updated.product_id != product_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product ID in path and body must match",
        )

    existing.product_name = updated.product_name
    existing.quantity = updated.quantity
    existing.price = updated.price

    return existing
