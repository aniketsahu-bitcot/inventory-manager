"""

Create all database tables using the configured SQLAlchemy engine.

"""

from db.session import engine

from db.base import Base

from models.product import Product  # noqa: F401

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")