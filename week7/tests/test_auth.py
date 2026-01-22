"""Tests for authentication and protected routes in the FastAPI application."""
from week7.tests.conftest import set_invalid_token
from fastapi.testclient import TestClient
from week7.tests.conftest import login_and_get_refresh_token
from sqlalchemy.orm import Session
from fastapi import status
from week7.tests.conftest import PRODUCTS_BASE_URL


def test_login_success_admin(client: TestClient)-> None:
    """Valid admin credentials → 200 and tokens returned"""
    response = client.post(
        "/auth/login",
        json={"username": "admin_user", "password": "password123"}
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_sets_cookies(client: TestClient)-> None:
    """Login should set access_token and refresh_token cookies"""
    response = client.post(
        "/auth/login",
        json={"username": "manager_user", "password": "password123"}
    )

    assert response.status_code == 200
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


def test_login_username_case_sensitive(client: TestClient)-> None:
    """Username case mismatch → 401"""
    response = client.post(
        "/auth/login",
        json={"username": "Admin_User", "password": "password123"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_with_extra_fields(client: TestClient)-> None:
    """Extra fields in request body should be ignored"""
    response = client.post(
        "/auth/login",
        json={
            "username": "admin_user",
            "password": "password123",
            "extra": "ignored"
        }
    )

    assert response.status_code == 200


def test_login_with_whitespace_username(client: TestClient)-> None:
    """Username with leading/trailing spaces → 401"""
    response = client.post(
        "/auth/login",
        json={"username": " admin_user ", "password": "password123"}
    )

    assert response.status_code == 401


def test_login_min_length_username(client: TestClient)-> None:
    """Minimum length username (1 char) → 401 if not found"""
    response = client.post(
        "/auth/login",
        json={"username": "a", "password": "password123"}
    )

    assert response.status_code == 401


def test_login_max_length_username(client: TestClient)-> None:
    """Very long username → 401"""
    long_username = "u" * 255
    response = client.post(
        "/auth/login",
        json={"username": long_username, "password": "password123"}
    )

    assert response.status_code == 401


def test_login_empty_password(client: TestClient)-> None:
    """Empty password → 401"""
    response = client.post(
        "/auth/login",
        json={"username": "admin_user", "password": ""}
    )

    assert response.status_code == 401




def test_login_invalid_username(client: TestClient)-> None:
    """Non-existent username → 401"""
    response = client.post(
        "/auth/login",
        json={"username": "unknown_user", "password": "password123"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_invalid_password(client: TestClient)-> None:
    """Wrong password → 401"""
    response = client.post(
        "/auth/login",
        json={"username": "admin_user", "password": "wrongpassword"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_missing_username(client: TestClient)-> None:
    """Missing username field → 422"""
    response = client.post(
        "/auth/login",
        json={"password": "password123"}
    )

    assert response.status_code == 422


def test_login_missing_password(client: TestClient)-> None:
    """Missing password field → 422"""
    response = client.post(
        "/auth/login",
        json={"username": "admin_user"}
    )

    assert response.status_code == 422


def test_login_empty_body(client: TestClient)-> None:
    """Empty JSON body → 422"""
    response = client.post("/auth/login", json={})

    assert response.status_code == 422


def test_login_wrong_data_types(client: TestClient)-> None:
    """Password not string → 422"""
    response = client.post(
        "/auth/login",
        json={"username": "admin_user", "password": 12345}
    )

    assert response.status_code == 422

def test_logout_when_logged_in(client: TestClient)-> None:
    """Logout when logged in should clear cookies and return 200"""
    client.post(
        "/auth/login",
        json={"username": "admin_user", "password": "password123"}
    )

    response = client.post("/auth/logout")

    assert response.status_code == 200
    assert response.json()["message"] == "You were not logged in"


def test_logout_clears_cookies(client: TestClient)-> None:
    """Logout should clear access_token and refresh_token cookies"""
    client.post(
        "/auth/login",
        json={"username": "manager_user", "password": "password123"}
    )

    response = client.post("/auth/logout")

    assert response.status_code == 200
    assert response.cookies.get("access_token") is None
    assert response.cookies.get("refresh_token") is None



def test_logout_twice(client: TestClient)-> None:
    """Calling logout twice should not fail"""
    client.post(
        "/auth/login",
        json={"username": "staff_user", "password": "password123"}
    )

    first_response = client.post("/auth/logout")
    second_response = client.post("/auth/logout")

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert second_response.json()["message"] == "You were not logged in"


def test_logout_without_login(client: TestClient)-> None:
    """Logout without login → still 200"""
    client.cookies.clear()

    response = client.post("/auth/logout")

    assert response.status_code == 200
    assert response.json()["message"] == "You were not logged in"


def test_logout_only_access_token_present(client: TestClient)-> None:
    """Logout works when only access token cookie exists."""
    client.post(
        "/auth/login",
        json={"username": "admin_user", "password": "password123"}
    )

    client.cookies.pop("refresh_token", None)

    response = client.post("/auth/logout")

    assert response.status_code == 200
    assert response.json()["message"] == "You were not logged in"


def test_logout_only_refresh_token_present(client: TestClient)-> None:
    """Logout works when only refresh token cookie exists."""
    client.post(
        "/auth/login",
        json={"username": "admin_user", "password": "password123"}
    )

    client.cookies.pop("access_token", None)

    response = client.post("/auth/logout")

    assert response.status_code == 200
    assert response.json()["message"] == "You were not logged in"


def test_logout_with_invalid_cookie_values(client: TestClient)-> None:
    """Invalid token values in cookies should not crash logout"""
    client.cookies.set("access_token", "invalid.token.value")
    client.cookies.set("refresh_token", "invalid.token.value")

    response = client.post("/auth/logout")

    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"


def test_logout_wrong_http_method(client: TestClient)-> None:
    """GET method not allowed on logout"""
    response = client.get("/auth/logout")

    assert response.status_code == 405



def test_refresh_token_success(client: TestClient) -> None:
    """Refresh token returns new access token when cookie is valid."""
    refresh_token = login_and_get_refresh_token(client,"admin_user", "password123")
    client.cookies.set("refresh_token", refresh_token)

    response = client.post("/auth/refresh")

    assert response.status_code == 200
    assert response.json()["message"] == "Token refreshed"


def test_refresh_token_multiple_times(client: TestClient) -> None:
    """Refresh token can be used multiple times before expiry."""
    refresh_token = login_and_get_refresh_token(client,"admin_user", "password123")
    client.cookies.clear()
    client.cookies.set("refresh_token", refresh_token)

    response1 = client.post("/auth/refresh")
    response2 = client.post("/auth/refresh")

    assert response1.status_code == 200
    assert response2.status_code == 200


def test_refresh_token_only_refresh_cookie_present(client: TestClient) -> None:
    """Refresh works when only refresh token cookie exists."""
    refresh_token = login_and_get_refresh_token(client,"admin_user", "password123")
    client.cookies.clear()
    client.cookies.set("refresh_token", refresh_token)

    response = client.post("/auth/refresh")

    assert response.status_code == 200
    assert response.json()["message"] == "Token refreshed"


def test_refresh_token_after_logout(client: TestClient) -> None:
    """Refresh token fails after logout clears cookies."""

    client.post("/auth/login", json={"username": "admin_user", "password": "password123"})
    client.post("/auth/logout")

    response = client.post("/auth/refresh")

    assert response.status_code == 401


def test_refresh_token_empty_cookie_value(client: TestClient) -> None:
    """Empty refresh token cookie is treated as invalid."""

    client.cookies.set("refresh_token", "")
    response = client.post("/auth/refresh")

    assert response.status_code == 401


def test_refresh_token_with_minimal_cookie_value(client: TestClient) -> None:
    """Very short refresh token value is rejected."""

    client.cookies.set("refresh_token", "x")
    response = client.post("/auth/refresh")

    assert response.status_code == 401


def test_refresh_token_large_cookie_value(client: TestClient) -> None:
    """Oversized refresh token value is rejected."""

    client.cookies.set("refresh_token", "x" * 5000)
    response = client.post("/auth/refresh")

    assert response.status_code == 401

def test_refresh_token_missing_cookie(client: TestClient) -> None:
    """Refresh token request without cookie fails."""

    response = client.post("/auth/refresh")

    assert response.status_code == 401
    assert response.json()["detail"] == "Missing refresh token"


def test_refresh_token_invalid_cookie(client: TestClient) -> None:
    """Invalid refresh token value is rejected."""

    client.cookies.set("refresh_token", "invalid.token.value")
    response = client.post("/auth/refresh")

    assert response.status_code == 401


def test_refresh_token_tampered_payload(client: TestClient) -> None:
    """Tampered refresh token payload is rejected."""

    client.cookies.set("refresh_token", "abc.def.ghi")
    response = client.post("/auth/refresh")

    assert response.status_code == 401


def test_refresh_token_only_access_token_present(client: TestClient) -> None:
    """Refresh fails if only access token exists."""

    client.post("/auth/login", json={"username": "admin_user", "password": "password123"})
    client.cookies.pop("refresh_token", None)

    response = client.post("/auth/refresh")

    assert response.status_code == 401


def test_refresh_token_wrong_http_method(client: TestClient) -> None:
    """Refresh endpoint fails on GET requests."""
    refresh_token = login_and_get_refresh_token(client,"admin_user", "password123")
    client.cookies.set("refresh_token", refresh_token)

    response = client.get("/auth/refresh")

    assert response.status_code == 405

def test_register_user_happy_path(client: TestClient, db: Session, roles)-> None:
    """Register a new user successfully."""
    payload = {
        "username": "new_user",
        "email": "new_user@example.com",
        "password": "StrongPassword123!"
    }

    response = client.post("/auth/register", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert data["role"] == "staff"

def test_register_username_edge_case_max_length(client: TestClient)-> None:
    """Register user with maximum length username."""
    payload = {
        "username": "u" * 50,  
        "email": "maxlenuser@example.com",
        "password": "StrongPassword123!"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == payload["username"]

def test_register_email_edge_case_long_email(client: TestClient)-> None:
    """Register user with very long email."""
    email = "a" * 200 + "@example.com" 
    payload = {
        "username": "longemailuser",
        "email": email,
        "password": "StrongPassword123!"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == email

def test_register_password_boundary_min_length(client: TestClient)-> None:
    """Register user with minimum length password."""
    payload = {
        "username": "minpassuser",
        "email": "minpass@example.com",
        "password": "a" * 8  
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

def test_register_password_boundary_max_length(client: TestClient)-> None:
    """Register user with maximum length password."""
    payload = {
        "username": "maxpassuser",
        "email": "maxpass@example.com",
        "password": "a" * 128  
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == status.HTTP_201_CREATED


def test_register_duplicate_username(client: TestClient)-> None:
    """Register user with duplicate username should fail."""
 
    client.post("/auth/register", json={
        "username": "dupuser",
        "email": "dupuser1@example.com",
        "password": "Password123!"
    })
   
    response = client.post("/auth/register", json={
        "username": "dupuser",
        "email": "dupuser2@example.com",
        "password": "Password123!"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]

def test_register_duplicate_email(client: TestClient)-> None:
    """Register user with duplicate email should fail."""
    
    client.post("/auth/register", json={
        "username": "emailuser1",
        "email": "dupemail@example.com",
        "password": "Password123!"
    })
    
    response = client.post("/auth/register", json={
        "username": "emailuser2",
        "email": "dupemail@example.com",
        "password": "Password123!"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]

def test_register_missing_required_fields(client: TestClient)-> None:
    """Register user with missing required fields should fail."""
    response = client.post("/auth/register", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  

def test_register_invalid_email_format(client: TestClient)-> None:
    """Register user with invalid email format should fail."""
    payload = {
        "username": "bademailuser",
        "email": "invalid-email-format",
        "password": "Password123!"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  

def test_no_token_cannot_list_products(client: TestClient)-> None:
    """Access list products route without token → 401"""
    client.cookies.clear()
    response = client.get(PRODUCTS_BASE_URL)
    assert response.status_code == 401

def test_list_products_invalid_token(client: TestClient)-> None:
    """Access list products route with invalid token → 401"""
    set_invalid_token(client)

    response = client.get(PRODUCTS_BASE_URL)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired access token"


def test_get_product_by_id_no_token(client: TestClient)-> None:
    """Access GET product by ID without token → 401"""
    client.cookies.clear()  

    response = client.get(f"{PRODUCTS_BASE_URL}/g001")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_product_by_id_invalid_token(client: TestClient)-> None:
    """Access GET product by ID with invalid token → 401"""
    set_invalid_token(client)

    response = client.get(f"{PRODUCTS_BASE_URL}/p123")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired access token"


def test_no_token_cannot_create_product(client: TestClient)-> None:
    """Access create product route without token → 401"""
    client.cookies.clear()
    response = client.post(PRODUCTS_BASE_URL, json={})
    assert response.status_code == 401

def test_create_product_invalid_token(client: TestClient)-> None:
    """Access create product route with invalid token → 401"""
    set_invalid_token(client)

    response = client.post(PRODUCTS_BASE_URL, json={
        "product_id": "inv001",
        "product_name": "InvalidTokenProduct",
        "type": "food",
        "quantity": 5,
        "price": 10,
        "expiry_date": "2030-01-01"
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired access token"


def test_no_token_cannot_update_product(client: TestClient)-> None:
    """Access update product route without token → 401"""
    client.cookies.clear()
    response = client.put(f"{PRODUCTS_BASE_URL}/x", json={"price": 10})
    assert response.status_code == 401

def test_update_product_invalid_token(client: TestClient)-> None:
    """Access update product route with invalid token → 401"""
    set_invalid_token(client)

    response = client.put(f"{PRODUCTS_BASE_URL}/p123", json={
        "price": 99
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired access token"


def test_no_token_cannot_delete_product(client: TestClient)-> None:
    """Access delete product route without token → 401"""
    client.cookies.clear()
    response = client.delete(f"{PRODUCTS_BASE_URL}/x")
    assert response.status_code == 401

def test_delete_product_invalid_token(client: TestClient)-> None:
    """Access delete product route with invalid token → 401"""
    set_invalid_token(client)

    response = client.delete(f"{PRODUCTS_BASE_URL}/p123")

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired access token"
