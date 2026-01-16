"""API routes for product management with authentication."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from week7.db.session import get_db
from week7.models.product import Product
from week7.schemas.product import ProductRead  
from week7.schemas.product import ProductCreate, ProductUpdate 
from week7.api.dependencies import get_current_user  
from week7.models.user import User

router = APIRouter()

@router.post(
    "/products",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  
) -> Product:
    """Create a new product in the inventory. (AUTH REQUIRED)"""
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

    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.put("/products/{product_id}", response_model=ProductRead)
def update_product(
    product_id: str,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  
) -> Product:
    """Update an existing product with proper type-dependent validation. (AUTH REQUIRED)"""
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    current_type = data.type if data.type is not None else product.type

    update_data = data.model_dump(exclude_unset=True)

    if current_type == "food":
        if "expiry_date" in update_data and update_data["expiry_date"] is None:
            raise HTTPException(
                status_code=422,
                detail="Food products must have a non-null expiry_date"
            )
        if data.type == "food" and product.expiry_date is None:
            raise HTTPException(
                status_code=422,
                detail="Cannot change to food type without providing expiry_date"
            )

    elif current_type == "electronic":
        if "warranty_period" in update_data and update_data["warranty_period"] is None:
            raise HTTPException(
                status_code=422,
                detail="Electronic products must have a non-null warranty_period"
            )
        if data.type == "electronic" and product.warranty_period is None:
            raise HTTPException(
                status_code=422,
                detail="Cannot change to electronic type without providing warranty_period"
            )

    elif current_type == "book":
        if "author" in update_data and not (update_data.get("author") or "").strip():
            raise HTTPException(422, "Book products must have a non-empty author")
        if data.type == "book":
            new_author = update_data.get("author", product.author)
            if not (new_author or "").strip():
                raise HTTPException(
                    status_code=422,
                    detail="Cannot change to book type without providing a valid non-empty author"
                )

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product

