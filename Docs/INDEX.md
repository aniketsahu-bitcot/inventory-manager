# inventory-manager Project

### 1. Introduction
A professional command-line Python package for inventory management that reads inventory.csv, validates products using Pydantic, logs errors, and generates low-stock reports.

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
