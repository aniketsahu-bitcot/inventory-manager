"""Pydantic models for Product entity with validation for different product types."""

from datetime import date
from typing import Any, Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator


class ProductBase(BaseModel):
    """Base model for Product with common fields."""
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

    @model_validator(mode="before")
    @classmethod
    def validate_create(cls, values: dict[str, Any]) -> dict[str, Any]:
        t = values.get("type")
        if t == "food" and values.get("expiry_date") is None:
            raise ValueError("Food products must have expiry_date")
        if t == "electronic" and values.get("warranty_period") is None:
            raise ValueError("Electronic products must have warranty_period")
        if t == "book":
            author = values.get("author", "")
            if not author.strip():
                raise ValueError("Book products must have author")
        return values


class ProductUpdate(BaseModel):
    """Model for updating an existing Product with optional fields."""
    product_name: Optional[str] = Field(None, min_length=1, max_length=255)
    quantity: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, gt=0)
    type: Optional[str] = Field(None, pattern="^(food|electronic|book)$")
    expiry_date: Optional[date] = None
    warranty_period: Optional[int] = Field(None, gt=0)
    author: Optional[str] = Field(None, min_length=1)

    @model_validator(mode="before")
    @classmethod
    def validate_update(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Only validate explicitly provided type-specific fields."""
        t = values.get("type")
        
        if t == "food" and "expiry_date" in values and values["expiry_date"] is None:
            raise ValueError("Food products must have expiry_date")
        if t == "electronic" and "warranty_period" in values and values["warranty_period"] is None:
            raise ValueError("Electronic products must have warranty_period")
        if t == "book" and "author" in values:
            author = values.get("author", "")
            if not author.strip():
                raise ValueError("Book products must have author")
        return values


class ProductRead(ProductBase):
    """Model for reading a Product from ORM."""
    product_id: str = Field(..., min_length=1, max_length=50)
    model_config = ConfigDict(from_attributes=True)
