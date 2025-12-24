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


### 3. Project Goals
- A private inventory-manager repository is created, a standard Git workflow is followed, core files are added, and changes are committed and pushed.
- Implement core functionality to read inventory.csv, load & validate rows with Pydantic, log invalid entries to errors.log, and create low_stock_report.txt for items under 10 units.
