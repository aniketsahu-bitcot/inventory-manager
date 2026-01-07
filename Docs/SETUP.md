# Inventory Manager Project Weekly Installation and Setup guide

### Prerequisites

Make sure the following are installed on your system:

* Python 3.9 or above
* pip (Python package manager)
* Git (optional, but recommended)

### Clone or Download the Project

If using Git:

```bash
git clone <repository-url>
cd <project-folder>
```

Or download the ZIP file and extract it, then open the project folder in terminal.

### Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

* On Linux / macOS:

```bash
source venv/bin/activate
```

* On Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

Install required packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Documentations

Refer to the `Docs` folder for more details:

* `SETUP.md` – setup instructions
* `ARCHITECTURE.md` – project design
* `INDEX.md` – Project overview
* `TESTING.md` – Testing Guide

### Common Issues

* If `python` command fails, try `python3`
* If packages fail to install, update pip:

```bash
pip install --upgrade pip
```

### Week wise Instructions to run the project

#### Week 1 Run Instructions

Navigate to the `week1` folder:

```bash
cd week1
```

Run a Python file:

```bash
python hello.py
```

#### Week 2 Run Instructions

Navigate to the `week2` folder:

```bash
cd week2
```

Run a Python file:

```bash
python process_inventory.py
```

#### Week 3 Run Instructions

Navigate to the `week3` folder:

```bash
cd week3
```

Run a Python file:

```bash
python main.py
```

#### Week 4 Run Instructions

Run all test cases of tests directory:

```bash
PYTHONPATH=./week3 pytest
```
Generate coverage report for the inventory_manager package:

```bash
PYTHONPATH=./week3 pytest --cov=week3 --cov-report=term-missing --cov-config=.coveragerc
```

#### Week 5 Run Instructions

Run all test cases of tests directory:

```bash
PYTHONPATH=./week3 pytest
```
Generate coverage report:

```bash
PYTHONPATH=./week3 pytest --cov=week5 --cov-report=term-missing
```

Access APIs by loading uvicorn server:

```bash
PYTHONPATH=./week3 uvicorn week5.app:app --reload
```
