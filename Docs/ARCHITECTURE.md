# Inventory Manager Project Folder Structure

### Project Folder Structure:

```
INVENTORY-MANAGER
├── Docs
│   ├── ARCHITECTURE.md
│   ├── INDEX.md
│   ├── SETUP.md
│   └── TESTING.md
├── pyproject.toml
├── README.md
├── requirements.txt
├── venv
├── week1
│   └── hello.py
├── week2
│   ├── errors.log
│   ├── inventory.csv
│   ├── low_stock_report.txt
│   └── process_inventory.py
├── week3
│   ├── errors.log
│   ├── __init__.py
│   ├── inventory.csv
│   ├── inventory_manager
│   │   ├── core.py
│   │   ├── __init__.py
│   │   ├── models.py
│   ├── low_stock_report.txt
│   └──  main.py
├── week4
│   └── tests
│       ├── conftest.py
│       ├── test_core.py
│       └── test_models.py
├── week5
│   ├── api
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── app.py
│   ├── main.py
│   └── tests
│       ├── conftest.py
│       ├── __init__.py
│       └── test_routes.py
└── week6
    ├── api
    │   ├── __init__.py
    │   └── routes.py
    ├── db
    │   ├── base.py
    │   ├── dependencies.py
    │   ├── __init__.py
    │   └── session.py
    ├── __init__.py
    ├── main.py
    ├── migrations
    │   ├── env.py
    │   ├── README
    │   ├── script.py.mako
    │   └── versions
    ├── models
    │   ├── __init__.py
    │   ├── product.py
    ├── schemas
    │   ├── __init__.py
    │   ├── product.py
    ├── scripts
    │   ├── __init__.py
    │   ├── load_inventory.py
    └── tests
        ├── conftest.py
        └── test_routes.py


```