# inventory-manager Project

### 1. Introduction
Inventory-manager is a Python tool that helps manage product inventory. It reads product data from a CSV file, checks that the data is valid, and logs any errors. It also includes a web API built with FastAPI and a full set of tests to make sure everything works correctly. It uses SQLAlchemy with PostgreSQL for persistent data storage and proper data validation. A comprehensive test suite using pytest and FastAPI TestClient ensures reliability and correctness of all CRUD operations.

### 2. Features

#### Week 1: Initial Functionality
- A new private GitHub repository named inventory-manager ensures controlled access and is cloned locally for development and version control.
- A standard Git workflow is followed by creating a develop branch from main, setting it as the default, and creating a feature branch for isolated development.
- Core project files are created, including .gitignore, README.md, and hello.py.
- All initial files are committed to the feature branch and pushed to the remote repository for collaboration and review.


#### Week 2: Validation and File Processing
- Reads and validates inventory.csv using a Pydantic Product model.
- Logs invalid rows and errors to errors.log.
- Collects valid products.
- Generates low_stock_report.txt for items below a quantity threshold.
- Organized with small, clear functions (load_and_validate_products, generate_low_stock_report).

#### Week 3: OOP Refactoring & Enhancements
- `Product` class bundles data & methods and follows Object-Oriented Design
- `Product` and `Inventory` both classes are following Single Responsibility Principle (SRP).
- Base `Product` with subclasses extensible without modification. This means it is following Inheritance and OCP correctly.
- Ruff linter, Black formatter, Google-style docstrings and full type hints are making code professionally good.
- `inventory_manager` is the proper python package comprises core.py and models.py files.
- `pyproject.toml` comprises the cofiguration data.
- `errors.log` file containing error logs, `inventory.csv` file containing products data in csv format, and `low_stock_report.txt` containing low stock products data.

#### Week 4: Test-Driven Development (TDD) with Pytest
- `tests/` directory contains unit tests for `Inventory` & `Product` public methods and test cases following AAA pattern.
- `Inventory` class contains `get_inventory_value()` which is tested by test cases
- Subclasses of `Product` class containing validation method which are tested with @pytest.mark.parametrize.
- fixtures for pre-configured `Product` and `Inventory` instances are used in test cases.
- pytest-mock is used to mock CSV loading and file writing.
- 100% test coverage for the `inventory_manager` package has achieved using pytest-cov.

#### Week 5: Building a Web API with FastAPI
- `main.py` file contains “Hello, World!” FastAPI app & `@app.route()` maps URLs to Python functions.
- `week5` directory contains structured FastAPI project & integrates `inventory_manager` package.
-  `week5/api/` directory contains `routes.py` file which comprises CRUD-style API endpoints:
  - **GET /products** – fetch all products
  - **GET /products/<product_id>** – fetch a single product
  - **POST /products** – validate JSON input and create a product
  - **PUT /products/<product_id>** – update an existing product
- `week5/tests/` directory contains test cases including FastAPI’s test client and pytest to write integration tests.

#### Week 6: Persistent Data with SQLAlchemy and PostgreSQL
- The `main.py` file initializes the FastAPI application and displays the message  
  **"Inventory API is running"** on startup.  
  It also registers API routes using `app.include_router()` from `week6/api/routes.py`.
- The `week6/` directory contains a well-structured FastAPI project that integrates a
  **PostgreSQL database** using **SQLAlchemy ORM** for persistent data storage.
- The `week6/api/` directory contains the `routes.py` file, which defines
  **CRUD-style API endpoints** for managing products:
  - **GET `/products`** – Fetch all products
  - **GET `/products/{product_id}`** – Fetch a single product by ID
  - **POST `/products`** – Validate JSON input and create a new product
  - **PUT `/products/{product_id}`** – Update an existing product
- The `week6/tests/` directory contains **integration tests** written using
  **pytest** and **FastAPI’s TestClient**, ensuring correct API behavior while
  interacting with a real (temporary) PostgreSQL test database.


### 3. Project Goals
- A private inventory-manager repository is created, a standard Git workflow is followed, core files are added, and changes are committed and pushed.
- Implement core functionality to read inventory.csv, load & validate rows with Pydantic, log invalid entries to errors.log, and create low_stock_report.txt for items under 10 units.
- Implement a Product class and Inventory class with proper methods, Both classes following Single Responsibility Principle (SRP).
- Extend a base Product into types like FoodProduct and ElectronicProduct. Design BookProduct and should follows Open/Closed Principle (OCP).
- Implement Python package `inventory_manager` with modules and __init__.py.
- Create & configure a pyproject.toml file.
- Use Ruff linter, Black formatter, Google-style docstrings and full type hints to make code professionally good.
- Validate all public methods in `Inventory` and `Product` through unit tests.
- Practice TDD by writing a failing test before implementing `get_inventory_value()`.
- Use fixtures and the Arrange-Act-Assert pattern to keep tests clean and readable.
- Learn mocking to safely test file I/O without touching the real filesystem.
- Improve reliability by parametrizing validation tests with multiple inputs.
- Achieve >95% coverage to confirm every part of the package is tested.
- Expose inventory functionality through a clean REST API, following HTTP standards and resource-based routing.
- Reuse business logic across layers so the API calls the real package instead of duplicating logic.
- Encourage scalable software engineering practices, including modular FastAPI blueprints and layered design.
- Ensure comprehensive test coverage of the FastAPI layer using pytest-cov, with integration tests exercising all API endpoints and behaviours to guarantee reliability and safe future enhancements.
- Transition from file-based storage to persistent data storage using PostgreSQL and SQLAlchemy.
- Replace in-memory or CSV-based inventory logic with database-backed CRUD operations.
- Use SQLAlchemy ORM models to map Python objects to relational database tables.
- Implement integration tests that validate API behavior against a real (temporary) PostgreSQL database.
- Apply database migrations to safely evolve the schema as application requirements change.
