"""Integration tests for product API endpoints using real test database."""

from fastapi.testclient import TestClient
from typing import Dict, Any

def test_create_product_success(client: TestClient) -> None:
    """Test successful product creation with electronic type."""
    payload: Dict[str, Any] = {
        "product_id": "CP001",
        "product_name": "Wireless Mouse",
        "quantity": 10,
        "price": 499.99,
        "type": "electronic",
        "warranty_period": 12
    }
    response = client.post("/api/products", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == payload["product_id"]
    assert data["product_name"] == payload["product_name"]

def test_create_product_duplicate_id(client: TestClient) -> None:
    """Test creating product with duplicate product_id returns 409."""
    payload: Dict[str, Any] = {
        "product_id": "CP002",
        "product_name": "Keyboard",
        "quantity": 5,
        "price": 999.0,
        "type": "electronic",
        "warranty_period": 6
    }
    client.post("/api/products", json=payload)
    response = client.post("/api/products", json=payload)
    assert response.status_code == 409

def test_create_product_min_quantity(client: TestClient) -> None:
    """Test product creation with minimum quantity (0)."""
    payload: Dict[str, Any] = {
        "product_id": "CP003",
        "product_name": "Pen",
        "quantity": 0,
        "price": 10.0,
        "type": "book",
        "author": "Author A"
    }
    response = client.post("/api/products", json=payload)
    assert response.status_code == 201
    assert response.json()["quantity"] == 0

def test_create_product_large_quantity(client: TestClient) -> None:
    """Test product creation with large quantity (10,000)."""
    payload: Dict[str, Any] = {
        "product_id": "CP004",
        "product_name": "Rice Bag",
        "quantity": 10_000,
        "price": 500.0,
        "type": "food",
        "expiry_date": "2026-12-31"
    }
    response = client.post("/api/products", json=payload)
    assert response.status_code == 201
    assert response.json()["quantity"] == 10_000

def test_create_product_min_price(client: TestClient) -> None:
    """Test product creation with minimum price boundary (0.01)."""
    payload: Dict[str, Any] = {
        "product_id": "CP005",
        "product_name": "Eraser",
        "quantity": 1,
        "price": 0.01,
        "type": "book",
        "author": "Author B"
    }
    response = client.post("/api/products", json=payload)
    assert response.status_code == 201
    assert response.json()["price"] == 0.01

def test_create_product_max_price(client: TestClient) -> None:
    """Test product creation with maximum price boundary."""
    payload: Dict[str, Any] = {
        "product_id": "CP006",
        "product_name": "Premium Laptop",
        "quantity": 1,
        "price": 1_000_000.0,
        "type": "electronic",
        "warranty_period": 24
    }
    response = client.post("/api/products", json=payload)
    assert response.status_code == 201
    assert response.json()["price"] == 1_000_000.0

def test_create_product_negative_price(client: TestClient) -> None:
    """Test product creation with negative price returns 422."""
    payload: Dict[str, Any] = {
        "product_id": "CP007",
        "product_name": "Invalid Item",
        "quantity": 5,
        "price": -50.0,
        "type": "book",
        "author": "Tester"
    }
    response = client.post("/api/products", json=payload)
    assert response.status_code == 422

def test_create_product_negative_quantity(client: TestClient) -> None:
    """Test product creation with negative quantity returns 422."""
    payload: Dict[str, Any] = {
        "product_id": "CP008",
        "product_name": "Invalid Item",
        "quantity": -5,
        "price": 50.0,
        "type": "book",
        "author": "Tester"
    }
    response = client.post("/api/products", json=payload)
    assert response.status_code == 422

def test_create_food_without_expiry(client: TestClient) -> None:
    """Test food product creation without expiry_date returns 422."""
    payload: Dict[str, Any] = {
        "product_id": "CP009",
        "product_name": "Milk",
        "quantity": 10,
        "price": 50.0,
        "type": "food"
    }
    response = client.post("/api/products", json=payload)
    assert response.status_code == 422

def test_create_electronic_without_warranty(client: TestClient) -> None:
    """Test electronic product creation without warranty_period returns 422."""
    payload: Dict[str, Any] = {
        "product_id": "CP010",
        "product_name": "Monitor",
        "quantity": 5,
        "price": 500.0,
        "type": "electronic"
    }
    response = client.post("/api/products", json=payload)
    assert response.status_code == 422

def test_create_book_without_author(client: TestClient) -> None:
    """Test book product creation without author returns 422."""
    payload: Dict[str, Any] = {
        "product_id": "CP011",
        "product_name": "Some Book",
        "quantity": 5,
        "price": 150.0,
        "type": "book"
    }
    response = client.post("/api/products", json=payload)
    assert response.status_code == 422


def test_create_product_empty_payload(client: TestClient) -> None:
    """Test POST with empty JSON body returns 422 (covers validation edge)."""
    response = client.post("/api/products", json={})  
    assert response.status_code == 422

def test_get_product_success(client: TestClient) -> None:
    """Test successful retrieval of existing product."""
    payload: Dict[str, Any] = {
        "product_id": "GP001",
        "product_name": "Test Mouse",
        "quantity": 10,
        "price": 499.99,
        "type": "electronic",
        "warranty_period": 12
    }
    client.post("/api/products", json=payload)
    response = client.get(f"/api/products/{payload['product_id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == payload["product_id"]

def test_get_nonexistent_product(client: TestClient) -> None:
    """Test retrieval of non-existent product returns 404."""
    response = client.get("/api/products/GP999")
    assert response.status_code == 404

def test_get_product_empty_id(client: TestClient) -> None:
    """Test GET with empty product_id hits list endpoint (200)."""
    response = client.get("/api/products/")
    assert response.status_code == 200  
    assert isinstance(response.json(), list)

def test_get_product_with_min_quantity(client: TestClient) -> None:
    """Test retrieval of product with zero quantity."""
    payload: Dict[str, Any] = {
        "product_id": "GP002",
        "product_name": "Zero Quantity Item",
        "quantity": 0,
        "price": 10.0,
        "type": "book",
        "author": "Author A"
    }
    client.post("/api/products", json=payload)
    response = client.get(f"/api/products/{payload['product_id']}")
    assert response.status_code == 200
    assert response.json()["quantity"] == 0

def test_get_product_with_large_quantity(client: TestClient) -> None:
    """Test retrieval of product with large quantity."""
    payload: Dict[str, Any] = {
        "product_id": "GP003",
        "product_name": "Bulk Item",
        "quantity": 10000,
        "price": 500.0,
        "type": "food",
        "expiry_date": "2026-12-31"
    }
    client.post("/api/products", json=payload)
    response = client.get(f"/api/products/{payload['product_id']}")
    assert response.status_code == 200
    assert response.json()["quantity"] == 10000

def test_get_product_min_price(client: TestClient) -> None:
    """Test retrieval of product with minimum price."""
    payload: Dict[str, Any] = {
        "product_id": "GP004",
        "product_name": "Cheap Item",
        "quantity": 1,
        "price": 0.01,
        "type": "book",
        "author": "Author B"
    }
    client.post("/api/products", json=payload)
    response = client.get(f"/api/products/{payload['product_id']}")
    assert response.status_code == 200
    assert response.json()["price"] == 0.01

def test_get_product_max_price(client: TestClient) -> None:
    """Test retrieval of product with maximum price."""
    payload: Dict[str, Any] = {
        "product_id": "GP005",
        "product_name": "Luxury Item",
        "quantity": 1,
        "price": 1_000_000.0,
        "type": "electronic",
        "warranty_period": 24
    }
    client.post("/api/products", json=payload)
    response = client.get(f"/api/products/{payload['product_id']}")
    assert response.status_code == 200
    assert response.json()["price"] == 1_000_000.0

def test_get_product_invalid_id_format(client: TestClient) -> None:
    """Test retrieval with invalid product_id format returns 404."""
    response = client.get("/api/products/@@@")
    assert response.status_code == 404

def test_get_product_invalid_id_special_chars(client: TestClient) -> None:
    """Test retrieval with special characters in product_id returns 404."""
    response = client.get("/api/products/!@#$")
    assert response.status_code == 404

def test_update_product_quantity_success(client: TestClient) -> None:
    """Test successful quantity update."""
    payload: Dict[str, Any] = {
        "product_id": "UP001",
        "product_name": "Rice Bag",
        "quantity": 2,
        "price": 299.0,
        "type": "food",
        "expiry_date": "2026-12-31"
    }
    client.post("/api/products", json=payload)
    response = client.put("/api/products/UP001", json={"quantity": 10})
    assert response.status_code == 200
    assert response.json()["quantity"] == 10

def test_update_product_price_success(client: TestClient) -> None:
    """Test successful price update."""
    payload: Dict[str, Any] = {
        "product_id": "UP002",
        "product_name": "Book A",
        "quantity": 5,
        "price": 150.0,
        "type": "book",
        "author": "John Doe"
    }
    client.post("/api/products", json=payload)
    response = client.put("/api/products/UP002", json={"price": 200.0})
    assert response.status_code == 200
    assert response.json()["price"] == 200.0

def test_update_product_to_food_without_expiry(client: TestClient) -> None:
    """Test updating to food type without expiry_date returns 422."""
    payload: Dict[str, Any] = {
        "product_id": "UP003",
        "product_name": "Milk Packet",
        "quantity": 1,
        "price": 50.0,
        "type": "food",
        "expiry_date": "2026-01-01"
    }
    client.post("/api/products", json=payload)
    response = client.put("/api/products/UP003", json={"expiry_date": None})
    assert response.status_code == 422

def test_update_product_to_book_without_author(client: TestClient) -> None:
    """Test updating to book type without author returns 422."""
    payload: Dict[str, Any] = {
        "product_id": "UP004",
        "product_name": "Generic Item",
        "quantity": 1,
        "price": 100.0,
        "type": "electronic",
        "warranty_period": 12
    }
    client.post("/api/products", json=payload)
    response = client.put("/api/products/UP004", json={"type": "book"})
    assert response.status_code == 422

def test_update_product_to_electronic_without_warranty(client: TestClient) -> None:
    """Test updating to electronic type without warranty returns 422."""
    payload: Dict[str, Any] = {
        "product_id": "UP005",
        "product_name": "Headphones",
        "quantity": 3,
        "price": 499.0,
        "type": "electronic",
        "warranty_period": 6
    }
    client.post("/api/products", json=payload)
    response = client.put("/api/products/UP005", json={"warranty_period": None})
    assert response.status_code == 422

def test_update_product_price_to_min_boundary(client: TestClient) -> None:
    """Test price update to minimum boundary value."""
    payload: Dict[str, Any] = {
        "product_id": "UP006",
        "product_name": "Cheap Book",
        "quantity": 1,
        "price": 10.0,
        "type": "book",
        "author": "Author A"
    }
    client.post("/api/products", json=payload)
    response = client.put("/api/products/UP006", json={"price": 0.01})
    assert response.status_code == 200
    assert response.json()["price"] == 0.01

def test_update_product_price_to_max_boundary(client: TestClient) -> None:
    """Test price update to maximum boundary value."""
    payload: Dict[str, Any] = {
        "product_id": "UP007",
        "product_name": "Luxury Item",
        "quantity": 1,
        "price": 1000.0,
        "type": "electronic",
        "warranty_period": 12
    }
    client.post("/api/products", json=payload)
    response = client.put("/api/products/UP007", json={"price": 1_000_000.0})
    assert response.status_code == 200
    assert response.json()["price"] == 1_000_000.0

def test_update_nonexistent_product(client: TestClient) -> None:
    """Test updating non-existent product returns 404."""
    response = client.put("/api/products/UP999", json={"quantity": 5})
    assert response.status_code == 404

def test_update_product_invalid_field(client: TestClient) -> None:
    """Test update with invalid field returns 422."""
    payload: Dict[str, Any] = {
        "product_id": "UP008",
        "product_name": "Keyboard",
        "quantity": 5,
        "price": 999.0,
        "type": "electronic",
        "warranty_period": 6
    }
    client.post("/api/products", json=payload)
    response = client.put("/api/products/UP008", json={"nonexistent_field": "value"})
    assert response.status_code == 422

def test_update_negative_quantity(client: TestClient) -> None:
    """Test updating product with negative quantity returns 422."""
    payload: Dict[str, Any] = {
        "product_id": "UP009",
        "product_name": "Test Item",
        "quantity": 10,
        "price": 100.0,
        "type": "electronic",
        "warranty_period": 12
    }
    client.post("/api/products", json=payload)
    
    response = client.put("/api/products/UP009", json={"quantity": -5})
    assert response.status_code == 422

def test_update_product_no_body(client: TestClient) -> None:
    """Test PUT without JSON body returns 422 (covers empty body validation)."""
    payload: Dict[str, Any] = {
        "product_id": "UC001",
        "product_name": "Test Item", 
        "quantity": 10,
        "price": 100.0,
        "type": "electronic",
        "warranty_period": 12
    }
    client.post("/api/products", json=payload)
    response = client.put("/api/products/UC001")  
    assert response.status_code == 422

def test_update_product_not_found(client: TestClient) -> None:
    """Test updating a non-existent product returns 404."""
    response = client.put(
        "/api/products/invalid-id",
        json={
            "product_name": "Test",
            "quantity": 5,
            "price": 10.0,
            "type": "food",
            "expiry_date": "2030-01-01",
        },
    )
    assert response.status_code == 404

def test_update_food_expiry_none(client: TestClient)-> None:
    """Test updating food product to have null expiry_date returns 422."""
    
    payload = {
        "product_id": "TF001",
        "product_name": "Yogurt",
        "quantity": 10,
        "price": 50.0,
        "type": "food",
        "expiry_date": "2026-01-01"
    }
    client.post("/api/products", json=payload)
    
    response = client.put("/api/products/TF001", json={"expiry_date": None})
    assert response.status_code == 422



def test_list_products_success(client: TestClient) -> None:
    """Test listing products with multiple entries."""
    payloads: list[Dict[str, Any]] = [
        {
            "product_id": "LP001",
            "product_name": "Laptop",
            "quantity": 5,
            "price": 49999.0,
            "type": "electronic",
            "warranty_period": 12
        },
        {
            "product_id": "LP002",
            "product_name": "Notebook",
            "quantity": 10,
            "price": 50.0,
            "type": "book",
            "author": "Jane Doe"
        }
    ]
    for payload in payloads:
        client.post("/api/products", json=payload)
    
    response = client.get("/api/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_list_products_single_entry(client: TestClient) -> None:
    """Test list endpoint returns exactly one product (covers single-entry branch)."""
    payload: Dict[str, Any] = {
        "product_id": "LC001",  
        "product_name": "Single Pen", 
        "quantity": 1,
        "price": 5.0,
        "type": "book",
        "author": "Author X"
    }
    client.post("/api/products", json=payload)
    response = client.get("/api/products")
    data = response.json()
    assert len(data) == 1 
    assert data[0]["product_id"] == "LC001"

def test_list_products_empty(client: TestClient) -> None:
    """Test listing products returns empty list when no products exist."""
    response = client.get("/api/products")
    assert response.status_code == 200
    assert response.json() == []

def test_list_products_large_db(client: TestClient) -> None:
    """Test listing products with large dataset (20+ products)."""
    for i in range(20):
        payload: Dict[str, Any] = {
            "product_id": f"LP{i:03d}",
            "product_name": f"Item {i+100}",
            "quantity": i + 1,
            "price": (i + 1) * 10.0,
            "type": "book",
            "author": "Author"
        }
        client.post("/api/products", json=payload)
    
    response = client.get("/api/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 20

def test_root_happy_path(client: TestClient) -> None:
    """GET / returns 200 and the correct message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["message"] == "Inventory API is running"

def test_root_with_trailing_slash(client: TestClient) -> None:
    """GET / with trailing slash returns 200 and correct message."""
    response = client.get("/?")  
    assert response.status_code == 200
    assert response.json() == {"message": "Inventory API is running"}


def test_root_with_query_parameters(client: TestClient) -> None:
    """GET / with query parameters returns 200 and correct message (query ignored)."""
    response = client.get("/?foo=bar&x=123")
    assert response.status_code == 200
    assert response.json() == {"message": "Inventory API is running"}


def test_root_with_headers(client: TestClient) -> None:
    """GET / with custom headers still works."""
    response = client.get("/", headers={"X-Test": "value"})
    assert response.status_code == 200
    assert response.json() == {"message": "Inventory API is running"}

def test_root_invalid_methods(client: TestClient) -> None:
    """POST, PUT, DELETE, PATCH on / return 405 Method Not Allowed."""
    methods = [client.post, client.put, client.delete, client.patch]
    for method in methods:
        response = method("/")
        assert response.status_code == 405
