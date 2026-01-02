# inventory-manager
A professional command-line Python package for inventory management.

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
---

### Learning Journey
- [Week 1 to 4 Overview](Docs/INDEX.md)
- [Architecture](Docs/ARCHITECTURE.md)
- [Setup & Installation](Docs/SETUP.md)
- [Testing Guide](Docs/TESTING.md)

---

### Tech Stack
- Language: Python
- Libraries & Frameworks: csv, pathlib, pydantic, pytest, pytest-mock
- Testing & Coverage: pytest-cov
- Code Quality: ruff and black
---
