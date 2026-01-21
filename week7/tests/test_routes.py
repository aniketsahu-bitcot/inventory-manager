"""Tests for FastAPI routes related to products and authentication."""
from sqlalchemy.orm import Session
from week7.tests.conftest import client, login
from datetime import date

def test_admin_can_create_product()-> None:
    """Admin can create a product → 201"""
    login("admin_user", "password123")
    response = client.post("/products/products", json={
        "product_id": "a001",
        "product_name": "AdminProduct",
        "type": "electronic",
        "quantity": 1,
        "price": 500,
        "warranty_period": 12
    })
    assert response.status_code == 201

def test_manager_can_post(users)-> None:
    """Manager can create a product → 201"""
    login("manager_user", "password123")
    response = client.post(
        "/products/products",  
        json={
            "product_id": "p888",
            "product_name": "Manager Product",
            "type": "book",
            "quantity": 2,
            "price": 150,
            "author": "Author Name"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == "p888"

def test_create_product_edge_case_missing_optional_field()-> None:
    """Book product missing 'author' → should fail 422"""
    login("manager_user", "password123")
    response = client.post(
        "/products/products",
        json={
            "product_id": "p002",
            "product_name": "Some Book",
            "type": "book",
            "quantity": 5,
            "price": 100
        }
    )
    assert response.status_code == 422

def test_create_product_missing_required_field()-> None:
    """Creating product missing required field → 422"""
    login("manager_user", "password123")
    response = client.post("/products/products", json={
        "product_id": "p100"
        
    })
    assert response.status_code == 422

def test_create_product_invalid_type()-> None:
    """Creating product with invalid type → 422"""
    login("manager_user", "password123")
    response = client.post("/products/products", json={
        "product_id": "p101",
        "product_name": "Toy Car",
        "type": "toy",  
        "quantity": 5,
        "price": 50
    })
    assert response.status_code == 422

def test_create_product_quantity_min()-> None:
    """Creating product with quantity = 0 → should succeed"""
    login("manager_user", "password123")
    response = client.post("/products/products", json={
        "product_id": "b001",
        "product_name": "Zero Quantity",
        "type": "food",
        "quantity": 0,
        "price": 10,
        "expiry_date": "2030-01-01"
    })
    assert response.status_code == 201

def test_create_product_quantity_max()-> None:
    """Creating product with quantity = 1,000,000 → should succeed"""
    login("manager_user", "password123")
    response = client.post("/products/products", json={
        "product_id": "b002",
        "product_name": "Max Quantity",
        "type": "food",
        "quantity": 1_000_000,
        "price": 10,
        "expiry_date": "2030-01-01"
    })
    assert response.status_code == 201


def test_create_product_price_max()-> None:
    """Creating product with price = 1,000,000 → should succeed"""
    login("manager_user", "password123")
    response = client.post("/products/products", json={
        "product_id": "b005",
        "product_name": "Expensive Product",
        "type": "electronic",
        "quantity": 10,
        "price": 1_000_000,
        "warranty_period": 24
    })
    assert response.status_code == 201

def test_create_product_error_existing_id()-> None:
    """Creating product with existing product_id → 409"""
    login("manager_user", "password123")

    client.post(
        "/products/products",
        json={
            "product_id": "p004",
            "product_name": "Duplicate Test",
            "type": "food",
            "quantity": 5,
            "price": 10,
            "expiry_date": "2030-01-01"
        }
    )

    response = client.post(
        "/products/products",
        json={
            "product_id": "p004",
            "product_name": "Duplicate Test 2",
            "type": "food",
            "quantity": 5,
            "price": 10,
            "expiry_date": "2030-01-01"
        }
    )
    assert response.status_code == 409

def test_create_product_error_unauthorized()-> None:
    """Non-logged-in user cannot create product → 401"""
    client.cookies.clear()  
    response = client.post(
        "/products/products",
        json={
            "product_id": "p005",
            "product_name": "Unauthorized",
            "type": "food",
            "quantity": 5,
            "price": 10,
            "expiry_date": "2030-01-01"
        }
    )
    assert response.status_code == 401

def test_staff_cannot_post(users)-> None:
    """Staff user cannot create product → 403"""
    login("staff_user", "password123")
    response = client.post(
        "/products/products",  
        json={
            "product_id": "p999",
            "product_name": "New Product",
            "type": "food",
            "quantity": 5,
            "price": 50,
            "expiry_date": "2030-01-01"
        },
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient permissions"

def test_manager_can_update_product()-> None:
    """Update food product quantity and price successfully"""
    login("manager_user", "password123")
   
    client.post("/products/products", json={
        "product_id": "u001",
        "product_name": "Milk",
        "type": "food",
        "quantity": 10,
        "price": 50,
        "expiry_date": "2030-01-01"
    })
  
    response = client.put("/products/products/u001", json={
        "quantity": 20,
        "price": 60
    })
    assert response.status_code == 200
    assert response.json()["quantity"] == 20
    assert response.json()["price"] == 60

def test_admin_can_update_product()-> None:
    """Admin can update product successfully"""
    login("admin_user", "password123")
    response = client.put("/products/products/a001", json={"price": 550})
    assert response.status_code == 200


def test_update_book_product_author()-> None:
    """Update book product author successfully"""
    login("manager_user", "password123")
    client.post("/products/products", json={
        "product_id": "u002",
        "product_name": "Book One",
        "type": "book",
        "quantity": 5,
        "price": 100,
        "author": "Author A"
    })
    response = client.put("/products/products/u002", json={
        "author": "Author B"
    })
    assert response.status_code == 200
    assert response.json()["author"] == "Author B"

def test_update_electronic_product_warranty()-> None:
    """Update electronic product warranty period successfully"""
    login("manager_user", "password123")
    client.post("/products/products", json={
        "product_id": "u003",
        "product_name": "Laptop",
        "type": "electronic",
        "quantity": 2,
        "price": 1000,
        "warranty_period": 12
    })
    response = client.put("/products/products/u003", json={
        "warranty_period": 24
    })
    assert response.status_code == 200
    assert response.json()["warranty_period"] == 24


def test_update_only_one_field()-> None:
    """Update only one field, leave others unchanged"""
    login("manager_user", "password123")
    client.post("/products/products", json={
        "product_id": "u004",
        "product_name": "EdgeCaseProduct",
        "type": "food",
        "quantity": 5,
        "price": 50,
        "expiry_date": "2030-01-01"
    })
    response = client.put("/products/products/u004", json={
        "price": 60
    })
    assert response.status_code == 200
    assert response.json()["price"] == 60
    assert response.json()["quantity"] == 5  

def test_change_type_food_to_electronic_missing_field()-> None:
    """Should fail if type-dependent field is missing"""
    login("manager_user", "password123")
    client.post("/products/products", json={
        "product_id": "u005",
        "product_name": "Cheese",
        "type": "food",
        "quantity": 5,
        "price": 20,
        "expiry_date": "2030-01-01"
    })
    response = client.put("/products/products/u005", json={
        "type": "electronic"
        
    })
    assert response.status_code == 422

def test_update_quantity_max()-> None:
    """Update product quantity to a very high value"""
    login("manager_user", "password123")
    client.post("/products/products", json={
        "product_id": "b002",
        "product_name": "MaxQtyFood",
        "type": "food",
        "quantity": 1,
        "price": 10,
        "expiry_date": "2030-01-01"
    })
    response = client.put("/products/products/b002", json={"quantity": 999999})
    assert response.status_code == 200
    assert response.json()["quantity"] == 999999


def test_update_price_max()-> None:
    """Update product price to a very high value"""
    login("manager_user", "password123")
    client.post("/products/products", json={
        "product_id": "b005",
        "product_name": "LuxuryItem",
        "type": "electronic",
        "quantity": 1,
        "price": 1000,
        "warranty_period": 12
    })
    response = client.put("/products/products/b005", json={"price": 9999999})
    assert response.status_code == 200
    assert response.json()["price"] == 9999999

def test_update_food_expiry_today()-> None:
    """Update food product expiry_date to today's date"""
    
    login("manager_user", "password123")
    today = date.today().isoformat()
    client.post("/products/products", json={
        "product_id": "b007",
        "product_name": "TodayFood",
        "type": "food",
        "quantity": 1,
        "price": 10,
        "expiry_date": "2030-01-01"
    })
    response = client.put("/products/products/b007", json={"expiry_date": today})
    assert response.status_code == 200
    assert response.json()["expiry_date"] == today

def test_update_non_existing_product()-> None:
    """Updating a non-existent product → 404"""
    login("manager_user", "password123")
    response = client.put("/products/products/nonexist", json={"price": 10})
    assert response.status_code == 404


def test_update_invalid_data_type()-> None:
    """Updating product with invalid data type → 422"""
    login("manager_user", "password123")
    client.post("/products/products", json={
        "product_id": "u007",
        "product_name": "InvalidType",
        "type": "food",
        "quantity": 5,
        "price": 50,
        "expiry_date": "2030-01-01"
    })
    response = client.put("/products/products/u007", json={
        "quantity": "ten"  
    })
    assert response.status_code == 422

def test_staff_cannot_update_product()-> None:
    """Staff user cannot update product → 403"""
    login("staff_user", "password123")
    response = client.put("/products/products/g001", json={"price": 99})
    assert response.status_code == 403

def test_get_product_staff_role()-> None:
    """Staff can get single product → 200"""
    login("manager_user", "password123")

  
    client.post("/products/products", json={
        "product_id": "g001",
        "product_name": "Test Product",
        "type": "food",
        "quantity": 5,
        "price": 50,
        "expiry_date": "2030-01-01"
    })

   
    login("staff_user", "password123")

    response = client.get("/products/products/g001")
    assert response.status_code == 200

def test_manager_can_get_single_product()-> None:
    """Manager can get single product → 200"""
    login("manager_user", "password123")

    client.post("/products/products", json={
        "product_id": "m001",
        "product_name": "Manager Product",
        "type": "book",
        "quantity": 3,
        "price": 100,
        "author": "Author X"
    })

    response = client.get("/products/products/m001")
    assert response.status_code == 200

def test_admin_can_get_single_product()-> None:
    """Admin can get single product → 200"""
    login("manager_user", "password123")

    client.post("/products/products", json={
        "product_id": "a001",
        "product_name": "Admin View Product",
        "type": "electronic",
        "quantity": 1,
        "price": 500,
        "warranty_period": 12
    })

    login("admin_user", "password123")

    response = client.get("/products/products/a001")
    assert response.status_code == 200



def test_get_product_long_id()-> None:
    """Product ID at maximum length (50 chars)"""
    long_id = "p" * 50
    login("manager_user", "password123")
    client.post("/products/products", json={
        "product_id": long_id,
        "product_name": "LongIDProduct",
        "type": "electronic",
        "quantity": 1,
        "price": 100,
        "warranty_period": 12
    })

    response = client.get(f"/products/products/{long_id}")
    assert response.status_code == 200


def test_get_product_min_length_id()-> None:
    """Product ID with 1 character → should succeed if exists"""
    login("manager_user", "password123")
    client.post("/products/products", json={
        "product_id": "a",
        "product_name": "MiniProduct",
        "type": "food",
        "quantity": 1,
        "price": 10,
        "expiry_date": "2030-01-01"
    })
    response = client.get("/products/products/a")
    assert response.status_code == 200

def test_get_product_max_length_id()-> None:
    """Product ID with max length (50 chars)"""
    long_id = "p" * 50
    login("manager_user", "password123")
    client.post("/products/products", json={
        "product_id": long_id,
        "product_name": "LongProduct",
        "type": "electronic",
        "quantity": 1,
        "price": 100,
        "warranty_period": 12
    })
    response = client.get(f"/products/products/{long_id}")
    assert response.status_code == 200


def test_get_product_max_values()-> None:
    """Product with very high quantity and price"""
    login("manager_user", "password123")
    client.post("/products/products", json={
        "product_id": "maxval",
        "product_name": "ExpensiveGadget",
        "type": "electronic",
        "quantity": 1_000_000,
        "price": 10_000_000,
        "warranty_period": 24
    })
    response = client.get("/products/products/maxval")
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 1_000_000
    assert data["price"] == 10_000_000


def test_get_product_not_found()-> None:
    """Non-existent product → 404"""
    login("manager_user", "password123")
    response = client.get("/products/nonexistent123")
    assert response.status_code == 404

def test_get_product_malformed_id()-> None:
    """Product ID contains invalid characters"""
    login("manager_user", "password123")
    response = client.get("/products/products/@@@###")
    assert response.status_code == 404  


def test_staff_can_list_products()-> None:
    """Staff can list all products → 200"""
    login("staff_user", "password123")
    response = client.get("/products/products")
    assert response.status_code == 200

def test_manager_can_list_products()-> None:
    """Manager can list all products → 200"""
    login("manager_user", "password123")
    response = client.get("/products/products")
    assert response.status_code == 200

def test_admin_can_list_products()-> None:
    """Admin can list all products → 200"""
    login("admin_user", "password123")
    response = client.get("/products/products")
    assert response.status_code == 200


def test_list_products_empty(db: Session)-> None:
    """Return all products (can be empty or non-empty)"""
    login("manager_user", "password123")
    response = client.get("/products/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)



def test_list_products_many()-> None:
    """Return a large number of products"""
    login("manager_user", "password123")
    for i in range(20):
        client.post("/products/products", json={
            "product_id": f"bulk{i}",
            "product_name": f"Product{i}",
            "type": "food",
            "quantity": i,
            "price": i*10,
            "expiry_date": "2030-01-01"
        })
    response = client.get("/products/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 20


def test_list_products_single()-> None:
    """Check that a specific product exists in the list"""
    login("manager_user", "password123")
    product_id = "single_test"
    client.post("/products/products", json={
        "product_id": product_id,
        "product_name": "SoloProduct",
        "type": "book",
        "quantity": 1,
        "price": 10,
        "author": "Author A"
    })
    response = client.get("/products/products")
    data = response.json()
    assert response.status_code == 200
    
    assert any(p["product_id"] == product_id for p in data)


def test_list_products_max_capacity()-> None:
    """Test retrieving a large number of products (boundary)"""
    login("manager_user", "password123")
    for i in range(50): 
        client.post("/products/products", json={
            "product_id": f"max{i}",
            "product_name": f"MaxProduct{i}",
            "type": "electronic",
            "quantity": i,
            "price": i*100,
            "warranty_period": 12
        })
    response = client.get("/products/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 50

def test_list_products_unauthorized()-> None:
    """Non-logged-in user cannot list products → 401"""
    client.cookies.clear() 
    response = client.get("/products/products")
    assert response.status_code == 401


def test_admin_can_delete(users, product)-> None:
    """Admin can delete product → 200"""
    login("admin_user", "password123")
    response = client.delete(f"/products/products/{product.product_id}") 
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Product deleted successfully"
    assert data["product_id"] == product.product_id



def test_delete_product_not_found()-> None:
    """Deleting a non-existent product returns 404"""
    login("admin_user", "password123")
    response = client.delete("/products/products/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_delete_product_max_id_length()-> None:
    """Product ID at maximum length (50 chars)"""
    long_id = "p" * 50
    login("admin_user", "password123")
    client.post("/products/products", json={
        "product_id": long_id,
        "product_name": "MaxIDProduct",
        "type": "electronic",
        "quantity": 1,
        "price": 100,
        "warranty_period": 12
    })
    response = client.delete(f"/products/products/{long_id}")
    assert response.status_code == 200


def test_delete_product_min_id_length()-> None:
    """Product ID at minimum length (1 char)"""
    login("admin_user", "password123")
    client.post("/products/products", json={
        "product_id": "x",
        "product_name": "MinIDProduct",
        "type": "food",
        "quantity": 1,
        "price": 10,
        "expiry_date": "2030-01-01"
    })
    response = client.delete("/products/products/x")
    assert response.status_code == 200


def test_delete_product_immediate()-> None:
    """Delete immediately after creation"""
    login("admin_user", "password123")
    client.post("/products/products", json={
        "product_id": "d002",
        "product_name": "ImmediateDelete",
        "type": "electronic",
        "quantity": 1,
        "price": 100,
        "warranty_period": 12
    })
    response = client.delete("/products/products/d002")
    assert response.status_code == 200


def test_delete_product_unauthorized_role()-> None:
    """Manager user cannot delete (403)"""
    login("manager_user", "password123")
    client.post("/products/products", json={
        "product_id": "d003",
        "product_name": "Protected",
        "type": "food",
        "quantity": 5,
        "price": 25,
        "expiry_date": "2030-01-01"
    })
    response = client.delete("/products/products/d003")
    assert response.status_code == 403


def test_delete_nonexistent_product()-> None:
    """Trying to delete a product that doesn't exist → 404"""
    login("admin_user", "password123")
    response = client.delete("/products/products/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_delete_with_wrong_role()-> None:
    """User without DELETE permissions (e.g., manager) → 403"""
    login("manager_user", "password123")
    client.post("/products/products", json={
        "product_id": "d006",
        "product_name": "WrongRoleTest",
        "type": "food",
        "quantity": 5,
        "price": 25,
        "expiry_date": "2030-01-01"
    })
    response = client.delete("/products/products/d006")
    assert response.status_code == 403


def test_manager_cannot_delete(users, product)-> None:
    """Manager cannot delete product → 403"""
    login("manager_user", "password123")
    response = client.delete(f"/products/products/{product.product_id}")  
    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient permissions"

def test_manager_cannot_delete_product()-> None:
    """Manager user cannot delete product → 403"""
    login("manager_user", "password123")
    response = client.delete("/products/products/m001")
    assert response.status_code == 403