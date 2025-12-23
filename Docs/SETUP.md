# Inventory Manager Project Weekly Installation and Setup guide

## Week1 Installation and Setup Guide

This guide explains how to install and set up the project step by step.

### Prerequisites

Make sure the following are installed on your system:

* Python 3.9 or above
* pip (Python package manager)
* Git (optional, but recommended)

### Step 1: Clone or Download the Project

If using Git:

```bash
git clone <repository-url>
cd <project-folder>
```

Or download the ZIP file and extract it, then open the project folder in terminal.

### Step 2: Create a Virtual Environment (Recommended)

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

### Step 3: Install Dependencies

Install required packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```


### Step 4: Project Structure Overview

```
Docs/           # Documentation files
week1/          # Python source files
  hello.py
README.md       # Project overview
.gitignore      # Git ignore file
requirements.txt  # Contains dependencies
```

### Step 5: Run the Project

Navigate to the `week1` folder:

```bash
cd week1
```

Run a Python file:

```bash
python hello.py
```

### Step 6: Documentation

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

## Week2 Installation and Setup Guide

This guide explains how to install and set up the project step by step.

### Prerequisites

Make sure the following are installed on your system:

* Python 3.9 or above
* pip (Python package manager)
* Git (optional, but recommended)

### Step 1: Clone or Download the Project

If using Git:

```bash
git clone <repository-url>
cd <project-folder>
```

Or download the ZIP file and extract it, then open the project folder in terminal.

### Step 2: Create a Virtual Environment (Recommended)

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

### Step 3: Install Dependencies

Install required packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```


### Step 4: Project Structure Overview

```
Docs/           # Documentation files
week1/          # week1 files
week2/          # week2 files
  errors.log
  inventory.csv
  low_stock_report.txt
  process_inventory.py
README.md       # Project overview
.gitignore      # Git ignore file
requirements.txt  # Contains dependencies
```

### Step 5: Run the Project

Navigate to the `week2` folder:

```bash
cd week2
```

Run a Python file:

```bash
python process_inventory.py
```

### Step 6: Documentation

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