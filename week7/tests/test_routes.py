"""Tests for FastAPI routes related to products and authentication."""
from sqlalchemy.orm import Session
from week7.tests.conftest import login
from datetime import date
from week7.tests.conftest import PRODUCTS_BASE_URL
from fastapi.testclient import TestClient

def test_admin_can_create_product(client: TestClient)-> None:
    """Admin can create a product → 201"""
    login(client, "admin_user", "password123")
    response = client.post(PRODUCTS_BASE_URL, json={
        "product_id": "a001",
        "product_name": "AdminProduct",
        "type": "electronic",
        "quantity": 1,
        "price": 500,
        "warranty_period": 12
    })
    assert response.status_code == 201

def test_manager_can_post(client: TestClient,users)-> None:
    """Manager can create a product → 201"""
    login(client,"manager_user", "password123")
    response = client.post(
        PRODUCTS_BASE_URL,
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

def test_create_product_edge_case_missing_optional_field(client: TestClient)-> None:
    """Book product missing 'author' → should fail 422"""
    login(client, "manager_user", "password123")
    response = client.post(
        PRODUCTS_BASE_URL,
        json={
            "product_id": "p002",
            "product_name": "Some Book",
            "type": "book",
            "quantity": 5,
            "price": 100
        }
    )
    assert response.status_code == 422

def test_create_product_missing_required_field(client: TestClient)-> None:
    """Creating product missing required field → 422"""
    login(client, "manager_user", "password123")
    response = client.post(PRODUCTS_BASE_URL, json={
        "product_id": "p100"
        
    })
    assert response.status_code == 422

def test_create_product_invalid_type(client: TestClient)-> None:
    """Creating product with invalid type → 422"""
    login(client, "manager_user", "password123")
    response = client.post(PRODUCTS_BASE_URL, json={
        "product_id": "p101",
        "product_name": "Toy Car",
        "type": "toy",  
        "quantity": 5,
        "price": 50
    })
    assert response.status_code == 422

def test_create_product_quantity_min(client: TestClient)-> None:
    """Creating product with quantity = 0 → should succeed"""
    login(client, "manager_user", "password123")
    response = client.post(PRODUCTS_BASE_URL, json={
        "product_id": "b001",
        "product_name": "Zero Quantity",
        "type": "food",
        "quantity": 0,
        "price": 10,
        "expiry_date": "2030-01-01"
    })
    assert response.status_code == 201

def test_create_product_quantity_max(client: TestClient)-> None:
    """Creating product with quantity = 1,000,000 → should succeed"""
    login(client, "manager_user", "password123")
    response = client.post(PRODUCTS_BASE_URL, json={
        "product_id": "b002",
        "product_name": "Max Quantity",
        "type": "food",
        "quantity": 1_000_000,
        "price": 10,
        "expiry_date": "2030-01-01"
    })
    assert response.status_code == 201


def test_create_product_price_max(client: TestClient)-> None:
    """Creating product with price = 1,000,000 → should succeed"""
    login(client, "manager_user", "password123")
    response = client.post(PRODUCTS_BASE_URL, json={
        "product_id": "b005",
        "product_name": "Expensive Product",
        "type": "electronic",
        "quantity": 10,
        "price": 1_000_000,
        "warranty_period": 24
    })
    assert response.status_code == 201

def test_create_product_error_existing_id(client: TestClient)-> None:
    """Creating product with existing product_id → 409"""
    login(client, "manager_user", "password123")

    client.post(PRODUCTS_BASE_URL,
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
        PRODUCTS_BASE_URL,
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

def test_create_product_error_unauthorized(client: TestClient)-> None:
    """Non-logged-in user cannot create product → 401"""
    client.cookies.clear()  
    response = client.post(
        PRODUCTS_BASE_URL,
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

def test_staff_cannot_post(client: TestClient, users)-> None:
    """Staff user cannot create product → 403"""
    login(client, "staff_user", "password123")
    response = client.post(
        PRODUCTS_BASE_URL,
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

def test_manager_can_update_product(client: TestClient)-> None:
    """Update food product quantity and price successfully"""
    login(client, "manager_user", "password123")
   
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": "u001",
        "product_name": "Milk",
        "type": "food",
        "quantity": 10,
        "price": 50,
        "expiry_date": "2030-01-01"
    })
  
    response = client.put(f"{PRODUCTS_BASE_URL}/u001", json={
        "quantity": 20,
        "price": 60
    })
    assert response.status_code == 200
    assert response.json()["quantity"] == 20
    assert response.json()["price"] == 60

def test_admin_can_update_product(client: TestClient)-> None:
    """Admin can update product successfully"""
    login(client, "admin_user", "password123")
    response = client.put(f"{PRODUCTS_BASE_URL}/a001", json={"price": 550})
    assert response.status_code == 200


def test_update_book_product_author(client: TestClient)-> None:
    """Update book product author successfully"""
    login(client, "manager_user", "password123")
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": "u002",
        "product_name": "Book One",
        "type": "book",
        "quantity": 5,
        "price": 100,
        "author": "Author A"
    })
    response = client.put(f"{PRODUCTS_BASE_URL}/u002", json={
        "author": "Author B"
    })
    assert response.status_code == 200
    assert response.json()["author"] == "Author B"

def test_update_electronic_product_warranty(client: TestClient)-> None:
    """Update electronic product warranty period successfully"""
    login(client, "manager_user", "password123")
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": "u003",
        "product_name": "Laptop",
        "type": "electronic",
        "quantity": 2,
        "price": 1000,
        "warranty_period": 12
    })
    response = client.put(f"{PRODUCTS_BASE_URL}/u003", json={
        "warranty_period": 24
    })
    assert response.status_code == 200
    assert response.json()["warranty_period"] == 24


def test_update_only_one_field(client: TestClient)-> None:
    """Update only one field, leave others unchanged"""
    login(client, "manager_user", "password123")
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": "u004",
        "product_name": "EdgeCaseProduct",
        "type": "food",
        "quantity": 5,
        "price": 50,
        "expiry_date": "2030-01-01"
    })
    response = client.put(f"{PRODUCTS_BASE_URL}/u004", json={
        "price": 60
    })
    assert response.status_code == 200
    assert response.json()["price"] == 60
    assert response.json()["quantity"] == 5  

def test_change_type_food_to_electronic_missing_field(client: TestClient)-> None:
    """Should fail if type-dependent field is missing"""
    login(client, "manager_user", "password123")
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": "u005",
        "product_name": "Cheese",
        "type": "food",
        "quantity": 5,
        "price": 20,
        "expiry_date": "2030-01-01"
    })
    response = client.put(f"{PRODUCTS_BASE_URL}/u005", json={
        "type": "electronic"
        
    })
    assert response.status_code == 422

def test_update_quantity_max(client: TestClient)-> None:
    """Update product quantity to a very high value"""
    login(client, "manager_user", "password123")
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": "b002",
        "product_name": "MaxQtyFood",
        "type": "food",
        "quantity": 1,
        "price": 10,
        "expiry_date": "2030-01-01"
    })
    response = client.put(f"{PRODUCTS_BASE_URL}/b002", json={"quantity": 999999})
    assert response.status_code == 200
    assert response.json()["quantity"] == 999999


def test_update_price_max(client: TestClient)-> None:
    """Update product price to a very high value"""
    login(client, "manager_user", "password123")
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": "b005",
        "product_name": "LuxuryItem",
        "type": "electronic",
        "quantity": 1,
        "price": 1000,
        "warranty_period": 12
    })
    response = client.put(f"{PRODUCTS_BASE_URL}/b005", json={"price": 9999999})
    assert response.status_code == 200
    assert response.json()["price"] == 9999999

def test_update_food_expiry_today(client: TestClient)-> None:
    """Update food product expiry_date to today's date"""
    
    login(client, "manager_user", "password123")
    today = date.today().isoformat()
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": "b007",
        "product_name": "TodayFood",
        "type": "food",
        "quantity": 1,
        "price": 10,
        "expiry_date": "2030-01-01"
    })
    response = client.put(f"{PRODUCTS_BASE_URL}/b007", json={"expiry_date": today})
    assert response.status_code == 200
    assert response.json()["expiry_date"] == today

def test_update_non_existing_product(client: TestClient)-> None:
    """Updating a non-existent product → 404"""
    login(client, "manager_user", "password123")
    response = client.put(f"{PRODUCTS_BASE_URL}/nonexist", json={"price": 10})
    assert response.status_code == 404


def test_update_invalid_data_type(client: TestClient)-> None:
    """Updating product with invalid data type → 422"""
    login(client, "manager_user", "password123")
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": "u007",
        "product_name": "InvalidType",
        "type": "food",
        "quantity": 5,
        "price": 50,
        "expiry_date": "2030-01-01"
    })
    response = client.put(f"{PRODUCTS_BASE_URL}/u007", json={
        "quantity": "ten"  
    })
    assert response.status_code == 422

def test_staff_cannot_update_product(client: TestClient)-> None:
    """Staff user cannot update product → 403"""
    login(client, "staff_user", "password123")
    response = client.put(f"{PRODUCTS_BASE_URL}/g001", json={"price": 99})
    assert response.status_code == 403

def test_get_product_staff_role(client: TestClient)-> None:
    """Staff can get single product → 200"""
    login(client, "manager_user", "password123")

  
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": "g001",
        "product_name": "Test Product",
        "type": "food",
        "quantity": 5,
        "price": 50,
        "expiry_date": "2030-01-01"
    })

   
    login(client,"staff_user", "password123")

    response = client.get(f"{PRODUCTS_BASE_URL}/g001")
    assert response.status_code == 200

def test_manager_can_get_single_product(client: TestClient)-> None:
    """Manager can get single product → 200"""
    login(client, "manager_user", "password123")

    client.post(PRODUCTS_BASE_URL, json={
        "product_id": "m001",
        "product_name": "Manager Product",
        "type": "book",
        "quantity": 3,
        "price": 100,
        "author": "Author X"
    })

    response = client.get(f"{PRODUCTS_BASE_URL}/m001")
    assert response.status_code == 200

def test_admin_can_get_single_product(client: TestClient)-> None:
    """Admin can get single product → 200"""
    login(client, "manager_user", "password123")

    client.post(PRODUCTS_BASE_URL, json={
        "product_id": "a001",
        "product_name": "Admin View Product",
        "type": "electronic",
        "quantity": 1,
        "price": 500,
        "warranty_period": 12
    })

    login(client, "admin_user", "password123")

    response = client.get(f"{PRODUCTS_BASE_URL}/a001")
    assert response.status_code == 200



def test_get_product_long_id(client: TestClient)-> None:
    """Product ID at maximum length (50 chars)"""
    long_id = "p" * 50
    login(client, "manager_user", "password123")
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": long_id,
        "product_name": "LongIDProduct",
        "type": "electronic",
        "quantity": 1,
        "price": 100,
        "warranty_period": 12
    })

    response = client.get(f"{PRODUCTS_BASE_URL}/{long_id}")
    assert response.status_code == 200


def test_get_product_min_length_id(client: TestClient)-> None:
    """Product ID with 1 character → should succeed if exists"""
    login(client, "manager_user", "password123")
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": "a",
        "product_name": "MiniProduct",
        "type": "food",
        "quantity": 1,
        "price": 10,
        "expiry_date": "2030-01-01"
    })
    response = client.get(f"{PRODUCTS_BASE_URL}/a")
    assert response.status_code == 200

def test_get_product_max_length_id(client: TestClient)-> None:
    """Product ID with max length (50 chars)"""
    long_id = "p" * 50
    login(client, "manager_user", "password123")
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": long_id,
        "product_name": "LongProduct",
        "type": "electronic",
        "quantity": 1,
        "price": 100,
        "warranty_period": 12
    })
    response = client.get(f"{PRODUCTS_BASE_URL}/{long_id}")
    assert response.status_code == 200


def test_get_product_max_values(client: TestClient)-> None:
    """Product with very high quantity and price"""
    login(client, "manager_user", "password123")
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": "maxval",
        "product_name": "ExpensiveGadget",
        "type": "electronic",
        "quantity": 1_000_000,
        "price": 10_000_000,
        "warranty_period": 24
    })
    response = client.get(f"{PRODUCTS_BASE_URL}/maxval")
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 1_000_000
    assert data["price"] == 10_000_000


def test_get_product_not_found(client: TestClient)-> None:
    """Non-existent product → 404"""
    login(client, "manager_user", "password123")
    response = client.get(f"{PRODUCTS_BASE_URL}/nonexistent123")
    assert response.status_code == 404

def test_get_product_malformed_id(client: TestClient)-> None:
    """Product ID contains invalid characters"""
    login(client, "manager_user", "password123")
    response = client.get(f"{PRODUCTS_BASE_URL}/@@@###")
    assert response.status_code == 404  


def test_staff_can_list_products(client: TestClient)-> None:
    """Staff can list all products → 200"""
    login(client, "staff_user", "password123")
    response = client.get(PRODUCTS_BASE_URL)
    assert response.status_code == 200

def test_manager_can_list_products(client: TestClient)-> None:
    """Manager can list all products → 200"""
    login(client, "manager_user", "password123")
    response = client.get(PRODUCTS_BASE_URL)
    assert response.status_code == 200

def test_admin_can_list_products(client: TestClient)-> None:
    """Admin can list all products → 200"""
    login(client, "admin_user", "password123")
    response = client.get(PRODUCTS_BASE_URL)
    assert response.status_code == 200


def test_list_products_empty(client: TestClient, db: Session)-> None:
    """Return all products (can be empty or non-empty)"""
    login(client, "manager_user", "password123")
    response = client.get(PRODUCTS_BASE_URL)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_list_products_many(client: TestClient) -> None:
    """Return a large number of products"""
    login(client, "manager_user", "password123")

    for i in range(1, 21):  
        r = client.post(PRODUCTS_BASE_URL, json={
            "product_id": f"bulk{i}",
            "product_name": f"Product{i}",
            "type": "food",
            "quantity": i,        
            "price": i * 10,     
            "expiry_date": "2030-01-01"
        })
        assert r.status_code == 201, r.json()

    response = client.get(f"{PRODUCTS_BASE_URL}?page=1&size=100")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 20




def test_list_products_single(client: TestClient) -> None:
    """Check that a specific product exists in the list"""
    login(client, "manager_user", "password123")
    product_id = "single_test"
    
    r = client.post(PRODUCTS_BASE_URL, json={
        "product_id": product_id,
        "product_name": "SoloProduct",
        "type": "book",
        "quantity": 1,
        "price": 10,
        "author": "Author A"
    })
    assert r.status_code == 201, r.json() 

    response = client.get(f"{PRODUCTS_BASE_URL}?page=1&size=50")
    assert response.status_code == 200
    data = response.json()
    
    assert any(p["product_id"] == product_id for p in data)

def test_list_products_max_capacity(client: TestClient) -> None:
    """Test retrieving a large number of products (boundary)"""
    login(client, "manager_user", "password123")

    for i in range(1, 51):  
        r = client.post(PRODUCTS_BASE_URL, json={
            "product_id": f"max{i}",
            "product_name": f"MaxProduct{i}",
            "type": "electronic",
            "quantity": i,     
            "price": i * 100,    
            "warranty_period": 12
        })
        assert r.status_code == 201, r.json()

    response = client.get(f"{PRODUCTS_BASE_URL}?page=1&size=100")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 50


def test_list_products_unauthorized(client: TestClient)-> None:
    """Non-logged-in user cannot list products → 401"""
    client.cookies.clear() 
    response = client.get(PRODUCTS_BASE_URL)
    assert response.status_code == 401


def test_admin_can_delete(users, product, client: TestClient)-> None:
    """Admin can delete product → 200"""
    login(client, "admin_user", "password123")
    response = client.delete(f"{PRODUCTS_BASE_URL}/{product.product_id}") 
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Product deleted successfully"
    assert data["product_id"] == product.product_id


def test_delete_product_max_id_length(client: TestClient)-> None:
    """Product ID at maximum length (50 chars)"""
    long_id = "p" * 50
    login(client, "admin_user", "password123")
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": long_id,
        "product_name": "MaxIDProduct",
        "type": "electronic",
        "quantity": 1,
        "price": 100,
        "warranty_period": 12
    })
    response = client.delete(f"{PRODUCTS_BASE_URL}/{long_id}")
    assert response.status_code == 200


def test_delete_product_min_id_length(client: TestClient)-> None:
    """Product ID at minimum length (1 char)"""
    login(client, "admin_user", "password123")
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": "x",
        "product_name": "MinIDProduct",
        "type": "food",
        "quantity": 1,
        "price": 10,
        "expiry_date": "2030-01-01"
    })
    response = client.delete(f"{PRODUCTS_BASE_URL}/x")
    assert response.status_code == 200


def test_delete_product_immediate(client: TestClient)-> None:
    """Delete immediately after creation"""
    login(client, "admin_user", "password123")
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": "d002",
        "product_name": "ImmediateDelete",
        "type": "electronic",
        "quantity": 1,
        "price": 100,
        "warranty_period": 12
    })
    response = client.delete(f"{PRODUCTS_BASE_URL}/d002")
    assert response.status_code == 200


def test_delete_product_unauthorized_role(client: TestClient)-> None:
    """Manager user cannot delete (403)"""
    login(client, "manager_user", "password123")
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": "d003",
        "product_name": "Protected",
        "type": "food",
        "quantity": 5,
        "price": 25,
        "expiry_date": "2030-01-01"
    })
    response = client.delete(f"{PRODUCTS_BASE_URL}/d003")
    assert response.status_code == 403


def test_delete_nonexistent_product(client: TestClient)-> None:
    """Trying to delete a product that doesn't exist → 404"""
    login(client, "admin_user", "password123")
    response = client.delete(f"{PRODUCTS_BASE_URL}/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_delete_with_wrong_role(client: TestClient)-> None:
    """User without DELETE permissions (e.g., manager) → 403"""
    login(client, "manager_user", "password123")
    client.post(PRODUCTS_BASE_URL, json={
        "product_id": "d006",
        "product_name": "WrongRoleTest",
        "type": "food",
        "quantity": 5,
        "price": 25,
        "expiry_date": "2030-01-01"
    })
    response = client.delete(f"{PRODUCTS_BASE_URL}/d006")
    assert response.status_code == 403


def test_manager_cannot_delete(users, product, client: TestClient)-> None:
    """Manager cannot delete product → 403"""
    login(client, "manager_user", "password123")
    response = client.delete(f"{PRODUCTS_BASE_URL}/{product.product_id}")  
    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient permissions"

def test_manager_cannot_delete_product(client: TestClient)-> None:
    """Manager user cannot delete product → 403"""
    login(client, "manager_user", "password123")
    response = client.delete(f"{PRODUCTS_BASE_URL}/m001")
    assert response.status_code == 403