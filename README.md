# inventory-manager

Inventory-manager is a Python tool for managing product inventory reliably and efficiently. It reads products from a CSV file, validates the data, logs any errors without interrupting processing, and stores valid records in a PostgreSQL database using SQLAlchemy. The project features modular design for easily adding new product types, exposes a FastAPI web API for CRUD operations, and includes a full pytest test suite with unit and integration tests to ensure correctness and maintainability. The API also includes secure JWT-based authentication and role-based access control (RBAC) to protect sensitive operations. The platform integrates LLMs with a Retrieval-Augmented Generation (RAG) pipeline over PostgreSQL (pgvector), enabling accurate, context-aware natural language queries on inventory data.


---

### Features
- Uses a private inventory-manager GitHub repository with a standard Git workflow (main, develop, and feature branches).
- Includes essential project files and maintains version control through structured commits and remote pushes.
- Reads and validates inventory.csv using a Pydantic Product model with strict data constraints.
- Logs invalid rows and detailed validation errors to errors.log without interrupting processing.
- Collects and processes only valid product records.
- Generates low_stock_report.txt for products below a defined quantity threshold.
- Organizes logic into small, well-named functions such as load_and_validate_products and generate_low_stock_report.
- Classes like `Inventory, Product, FoodProduct, ElectronicProduct` and `BookProduct` are following object oriented design and all product types added without modifying Inventory core logic.
- `inventory_manager` is the python package containing `init.py` file with modules.
- `pyproject.toml` file contains configuration data.
- Ruff linter, Black formatter, Google-style docstrings and full type hints are used to make code professionally good.
- Added a tests/ suite with unit tests for all public methods in `Product` and `Inventory`, following TDD and the Arrange–Act–Assert pattern.
- Fixtures are used to supply reusable Product and Inventory objects, following the Arrange–Act–Assert pattern.
- Mocking is used to safely test file I/O, including CSV loading and writing low-stock reports, without touching real files.
- Validation logic is tested using @pytest.mark.parametrize with multiple valid and invalid inputs.
- Test coverage is measured using pytest-cov, achieving 100% coverage for the inventory_manager package.
- RESTful Web APIs using FastAPI are implemented , following HTTP best practices and clear resource-based routing.
- FastAPI project using Blueprints to keep the API modular, scalable, and maintainable instead of relying on a single monolithic app.py.
- `inventory_manager` Python package is used so the API directly works with real inventory logic rather than duplicate code.
- CRUD-style API endpoints are used including:
  - **GET /products** – fetch all products
  - **GET /products/<product_id>** – fetch a single product
  - **POST /products** – validate JSON input and create a product
  - **PUT /products/<product_id>** – update an existing product
- A pytest-based integration test suite is used using FastAPI’s test client to simulate real HTTP requests to the API.
- Achieved full test coverage of the API layer using pytest-cov, ensuring reliability and confidence in changes.
- SQLAlchemy ORM is used for database interaction, replacing CSV-based storage for robust, scalable persistence.
- PostgreSQL is the production-ready relational database used, with proper connection handling and session management.
- Alembic is used to manage database migrations, allowing safe schema evolution and versioning.
- Integration tests interact with a temporary PostgreSQL test database to verify SQLAlchemy logic without affecting production data.
- API endpoints now persist and retrieve data from PostgreSQL, ensuring real-world behavior during testing and development.
- Database seeding scripts populate PostgreSQL with initial inventory data from inventory.csv for development and testing.
- Secure user authentication implemented using JWT (JSON Web Tokens) for stateless API access.
- User registration and login endpoints with securely hashed passwords using industry-standard hashing.
- Role-Based Access Control (RBAC) implemented using FastAPI dependency functions.
- User roles (`admin`, `manager`, `staff`) define permissions for accessing and modifying resources.
- Protected API endpoints enforce authentication and authorization with proper HTTP status codes (401, 403).
- Product-modifying routes (POST, PUT, DELETE) are restricted based on user roles.
- Integration tests validate authentication, JWT handling, and RBAC enforcement using FastAPI TestClient.
- Integrates an LLM-powered natural language query feature using Retrieval-Augmented Generation (RAG) for inventory data.
- Stores and retrieves semantic embeddings with PostgreSQL (pgvector) to provide accurate, context-aware responses.
- Exposes a secure API endpoint for AI-driven inventory queries, with responses grounded strictly in stored product data.


---

### Learning Journey
- [Week 1 to 6 Overview](Docs/INDEX.md)
- [Architecture](Docs/ARCHITECTURE.md)
- [Setup & Installation](Docs/SETUP.md)
- [Testing Guide](Docs/TESTING.md)

---
### Tech Stack
- **Language:** Python
- **Frameworks & Libraries:** FastAPI, Pydantic, SQLAlchemy, Alembic, psycopg2
- **Authentication & Security:** JWT (JSON Web Tokens), password hashing (Werkzeug)
- **Database:** PostgreSQL
- **Testing:** pytest, pytest-mock, FastAPI TestClient
- **Coverage:** pytest-cov
- **Code Quality:** Ruff, Black
- **LLM & AI stack:** langchain, langchain-openai, langchain-core, langchain-community, pgvector

---
