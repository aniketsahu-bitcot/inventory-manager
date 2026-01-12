"""Pydantic models for Product entity with validation for different product types."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    """Base model for Product with common fields and validation."""
    product_name: str = Field(..., min_length=1, max_length=255)
    quantity: int = Field(..., ge=0)
    price: float = Field(..., gt=0)
    type: str = Field(..., pattern="^(food|electronic|book)$")
    expiry_date: Optional[date] = None
    warranty_period: Optional[int] = Field(None, gt=0)
    author: Optional[str] = None


class ProductCreate(ProductBase):
    """Model for creating a new Product with required product_id."""
    product_id: str = Field(..., min_length=1, max_length=50)


class ProductUpdate(BaseModel):
    """Model for updating an existing Product with optional fields."""
    product_name: Optional[str] = Field(None, min_length=1, max_length=255)
    quantity: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, gt=0)
    type: Optional[str] = Field(None, pattern="^(food|electronic|book)$")
    expiry_date: Optional[date] = None
    warranty_period: Optional[int] = Field(None, gt=0)
    author: Optional[str] = None


class ProductRead(ProductBase):
    """Model for reading a Product with all fields including product_id."""
    product_id: str

    model_config = ConfigDict(from_attributes=True)
