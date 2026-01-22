"""Fixtures for testing the FastAPI application."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from week7.main import app
from week7.db.session import SessionLocal
from week7.models.user import User
from week7.models.role import Role
from week7.models.product import Product
from week7.auth.security import hash_password
from typing import Any

PRODUCTS_BASE_URL = "/products/products"

@pytest.fixture(scope="function")
def client() -> Any:
    """Provide a fresh TestClient per test."""
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def db() -> Any:
    """Provide a database session for tests."""
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="module")
def roles(db: Session)-> Any:
    """Create roles for testing."""
    role_names = ["staff", "manager", "admin"]
    role_objs = []
    for name in role_names:
        r = db.query(Role).filter(Role.name == name).first()
        if not r:
            r = Role(name=name)
            db.add(r)
    db.commit()
    for name in role_names:
        role_objs.append(db.query(Role).filter(Role.name == name).first())
    return role_objs


@pytest.fixture(scope="module")
def users(db: Session, roles)-> Any:
    """Create test users with different roles."""
    db.query(User).delete()
    db.commit()

    staff = User(
        username="staff_user",
        email="staff@example.com",
        hashed_password=hash_password("password123"),
        role="staff",
        role_ref=roles[0],
    )
    manager = User(
        username="manager_user",
        email="manager@example.com",
        hashed_password=hash_password("password123"),
        role="manager",
        role_ref=roles[1],
    )
    admin = User(
        username="admin_user",
        email="admin@example.com",
        hashed_password=hash_password("password123"),
        role="admin",
        role_ref=roles[2],
    )

    db.add_all([staff, manager, admin])
    db.commit()
    db.refresh(staff)
    db.refresh(manager)
    db.refresh(admin)
    return {"staff": staff, "manager": manager, "admin": admin}


@pytest.fixture(scope="module")
def product(db: Session)-> Any:
    """Create a sample product for testing."""
    db.query(Product).delete()
    db.commit()
    p = Product(
        product_id="p123",
        product_name="Test Product",
        type="food",
        quantity=10,
        price=100,
        expiry_date="2030-01-01"
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def login(client:TestClient,username: str, password: str)-> Any:
    """Login helper: sets access_token in TestClient cookies for further requests."""
    client.cookies.clear()
    response = client.post("/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200

    tokens = response.json()

    client.cookies.set("access_token", tokens["access_token"])
    client.cookies.set("refresh_token", tokens["refresh_token"])
    return tokens

def set_invalid_token(client: TestClient)-> None:
    """Set an invalid access token in the TestClient cookies."""
    client.cookies.clear()
    client.cookies.set("access_token", "this.is.an.invalid.token")

def login_and_get_refresh_token(client: TestClient, username: str, password: str) -> str:
    """Helper to login and return the refresh token from cookies."""
    response = client.post("/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200
    refresh_token = response.cookies.get("refresh_token")
    assert refresh_token is not None
    return refresh_token


