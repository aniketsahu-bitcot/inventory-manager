# Testing & Test-Driven Development (TDD) Practices Guide

## 1. Introduction
This document explains the testing strategy used in this project, the tools involved, and how to write effective and maintainable tests.

---
### 2. Testing Philosophy
- The project follows **Test-Driven Development (TDD)** to ensure correctness and clean design.
- Testing is guided by the **Testing Pyramid**, prioritizing **unit tests** over integration and end-to-end tests.
- Development follows the **Red–Green–Refactor** cycle:
  - **Red**: Write a failing test
  - **Green**: Write minimal code to pass the test
  - **Refactor**: Improve code while keeping tests green
- **Pytest** is used as the primary testing framework.
- **FastAPI TestClient** is used to simulate real HTTP requests in integration tests without running a live server.
- Test functions are written and executed using `pytest` to validate behavior early.
- **Pytest fixtures** provide reusable and pre-configured test data.
- The **Arrange–Act–Assert (AAA)** pattern is followed in every test to improve clarity and consistency.
- **Unit tests** must avoid real filesystem, database, and network access.
- **Integration tests** may interact with real services (e.g., PostgreSQL) in a controlled and temporary test environment.
- **Mocking** is a technique used to replace real external dependencies with controlled fake objects so tests remain fast, stable, and predictable.
- **Patching** is a method used to apply mocks at runtime.
- **Parametrization** allows testing the same logic with different inputs.
- **Test coverage** measures how much of the codebase is exercised by tests.

---

## 3. Learnings
- Red–Green–Refactor cycle
- Importance of fixtures for reusability
- TDD using Pytest
- Pytest fixtures
- Arrange–Act–Assert (AAA) pattern
- Mocking and patching
- Parametrization
- Test coverage
- Using FastAPI TestClient for API integration testing

---

## 4. Key Principles
- TDD with Pytest treats tests as specifications, emphasizing unit tests via the Testing Pyramid and the Red–Green–Refactor cycle.
- Pytest supports reusability through fixtures and simple test execution.
- Unit tests must avoid real filesystem, database, and network access to remain fast, reliable, and deterministic.
- Integration tests validate real interactions (e.g., SQLAlchemy with PostgreSQL) using a temporary test database.
- Mocking replaces real external dependencies with controlled fake objects, enabling isolated and predictable tests.
- Parametrization allows testing a single function against multiple valid, edge, and error scenarios.
- Test coverage highlights untested code paths but does **not** guarantee bug-free software.
- FastAPI TestClient enables realistic request/response testing while running in-process.

---

## 5. Tools Used
- **pytest** – Testing framework  
- **FastAPI TestClient** – API integration testing  
- **pytest fixtures** – Test setup and reuse  
- **pytest-mock** – Mocking and patching support  
- **pytest-cov** – Test coverage analysis  
- **PostgreSQL** – Real but temporary database for integration tests  
- **SQLAlchemy** – ORM layer validation  
- **ruff** – Code linting and quality checks  
- **black** – Code formatting  

---

## 6. Best Practices
- Write tests before implementation (TDD)
- Keep tests small and focused
- Avoid testing implementation details
- Prefer unit tests over integration tests
- Follow the Arrange–Act–Assert (AAA) pattern
- Use fixtures to avoid duplication and improve maintainability
- Mock external dependencies (filesystem, network, third-party services)
- Use parametrization instead of duplicating tests
- Run tests frequently during development
- Use coverage to identify gaps — **but never rely on coverage alone**

---

## 7. Common Mistakes
- Writing overly complex tests
- Sharing state between tests
- Skipping edge cases
- Ignoring failing tests
- Writing tests that depend on real filesystem, database, or network
- Not following the Arrange–Act–Assert (AAA) pattern
- Duplicating setup logic instead of using fixtures
- Assuming 100% coverage means bug-free code

---

## 8. Conclusion
Testing improves correctness, enforces better design, and builds confidence when adding features or refactoring.  
Effective testing with Pytest uses fixtures, mocking, parametrization, and **FastAPI TestClient** to create **fast, reliable, and maintainable** tests.

**Test coverage helps identify missing tests — but meaningful test cases and good design always matter more than numbers.**
