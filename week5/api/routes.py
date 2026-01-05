"""
Inventory API routes.

This module defines the FastAPI API router and implements CRUD endpoints for managing products in the inventory.
It integrates the existing `inventory_manager` package which handles all inventory operations.
"""
from fastapi import APIRouter, HTTPException
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