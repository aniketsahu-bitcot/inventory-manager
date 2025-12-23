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

---

### Learning Journey
- [Week 1 to 2 Overview](Docs/INDEX.md)
- [Architecture](Docs/ARCHITECTURE.md)
- [Setup & Installation](Docs/SETUP.md)
- [Testing Guide](Docs/TESTING.md)

---

### Tech Stack
- Language: Python

---

### Project Folder Structure:
```
├── Docs/
├── README.md
├── requirements.txt
├── .gitignore
├── Week1/
└── Week2/

```

---

## Installation

1. Clone the repository:

```
git clone <repository-url>
```
2. Navigate to the Project Directory

```
cd project_name
```

3. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

4. Install dependencies:
```
pip install -r requirements.txt
```

