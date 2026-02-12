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
├── week6
│   ├── api
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── db
│   │   ├── base.py
│   │   ├── dependencies.py
│   │   ├── __init__.py
│   │   └── session.py
│   ├── __init__.py
│   ├── main.py
│   ├── migrations
│   │   ├── env.py
│   │   ├── README
│   │   ├── script.py.mako
│   │   └── versions
│   ├── models
│   │   ├── __init__.py
│   │   └──  product.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └──  product.py
│   ├── scripts
│   │   ├── __init__.py
│   │   └── load_inventory.py
│   └── tests
│       ├── conftest.py
│       ├── test_dependencies.py
│       ├── test_product.py
│       └── test_routes.py
├── week7
│   ├── api
│   │   ├── auth.py
│   │   ├── dependencies.py
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── auth
│   │   ├── __init__.py
│   │   └── security.py
│   ├── core
│   │   ├── config.py
│   │   └── __init__.py
│   ├── db
│   │   ├── base.py
│   │   ├── __init__.py
│   │   └── session.py
│   ├── __init__.py
│   ├── main.py
│   ├── migrations
│   │   ├── env.py
│   │   ├── README
│   │   ├── script.py.mako
│   │   └── versions
│   ├── models
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── role.py
│   │   └── user.py
│   ├── schemas
│   │   ├── auth.py
│   │   ├── __init__.py
│   │   ├── product.py
│   │   └── user.py
│   └── tests
│       ├── conftest.py
│       ├── test_auth.py
│       └── test_routes.py
├── week8
│   ├── api
│   │   ├── chat.py
│   │   └── __init__.py
│   ├── chat_with_cost.py
│   ├── constants.py
│   ├── create_vectorstore.py
│   ├── __init__.py
│   ├── load_products.py
│   ├── main.py
│   ├── rag_chain_lcel.py
│   ├── split_documents.py
│   └── store_embeddings_index.py
└── week9
    ├── api
    │   ├── chat.py
    │   ├── document.py
    │   └── __init__.py
    ├── cache.py
    ├── constants.py
    ├── create_vectorstore_minilm.py
    ├── __init__.py
    ├── llm_comparison.py
    ├── llm_comparison_report.txt
    ├── main.py
    ├── migrations
    │   ├── env.py
    │   ├── README
    │   ├── script.py.mako
    │   └── versions
    ├── models
    │   └──  document.py
    ├── rag_chain.py
    └── schemas
        ├── __init__.py
        ├── request_model.py
        └── response_model.py

```