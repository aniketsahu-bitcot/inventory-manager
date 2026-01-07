# inventory-manager

Inventory-manager is a Python tool for managing product inventory in a clean and reliable way. It reads products from a CSV file, checks that the data is valid, and logs any errors without stopping the program. The project uses simple, modular code so new product types can be added easily. It also includes a FastAPI web API and a full test suite using pytest to make sure everything works correctly.

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

---

### Learning Journey
- [Week 1 to 5 Overview](Docs/INDEX.md)
- [Architecture](Docs/ARCHITECTURE.md)
- [Setup & Installation](Docs/SETUP.md)
- [Testing Guide](Docs/TESTING.md)

---
### Tech Stack
- **Language:** Python
- **Frameworks & Libraries:** FastAPI, Pydantic, csv, pathlib
- **Testing:** pytest, pytest-mock, FastAPI test client
- **Coverage:** pytest-cov
- **Code Quality:** Ruff, Black

---
