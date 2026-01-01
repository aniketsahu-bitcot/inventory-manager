## Testing & Test Driven Development Practices Guide

### 1. Introduction
This document explains the testing strategy used in this project, the tools involved, and how to write tests effectively.

---
### 2. Testing Philosophy
- The project follows **Test-Driven Development (TDD)** to ensure correctness and clean design.
- Testing is guided by the **Testing Pyramid**, prioritizing **unit tests** over integration and end-to-end tests.
- Development follows the **Red–Green–Refactor** cycle:
  - **Red**: Write a failing test
  - **Green**: Write minimal code to pass the test
  - **Refactor**: Improve code while keeping tests green
- **Pytest** is used as the primary testing framework.
- Test functions are written and executed using `pytest` to validate behavior early.
- **Pytest fixtures** provide reusable and pre-configured test data.
- The **Arrange–Act–Assert (AAA)** pattern is followed in every test to improve clarity and consistency.
- unit tests should avoid real filesystem, database, and network access during testing.
- **Mocking (also called patching)** is a technique used in testing to replace real external dependencies with fake, controlled versions so your tests run fast, stable, and predictable.
- **Parametrization** helps us to test methods with differnt kind of inputs.
- **Test coverage** is a way to measure how much of your code is tested by your tests.

---
### 3. Learnings:
- Red Green Refactor Cycle
- Importance of Fixtures for resusability
- TDD using Pytest
- Pytest Fixtures
- Arrange Act Assert pattern
- Mocking/Patching
- Parametrization
- Test Coverage

---

### 4. Key Principles
- TDD with Pytest treats tests as specifications, emphasizing unit tests via the Testing Pyramid and the Red-Green-Refactor cycle.
- Pytest supports reusability with simple test execution and reusable fixtures, using the Arrange-Act-Assert pattern to keep tests clean and maintainable
- Unit tests must avoid real filesystem, database, and network access to remain fast, reliable, and deterministic.
- Mocking (patching) replaces real external dependencies with controlled fake objects, enabling isolated and predictable tests.
- Parametrization allows testing a single method against multiple input scenarios, including edge and error cases.
- Test coverage measures which parts of the code are executed by tests, helping identify untested logic (but not guaranteeing bug-free code).

--- 

### 5. Tools Used
- **pytest** – Test framework
- **fixtures** – Test setup and reuse
- **ruff** – Code quality and linting
- **black**  – For code formatting
- **pytest-mock** – Provides the mocker fixture
- **pytest-cov** – Plugin for measuring and analyzing test coverage


### 6. Best Practices

- Write tests before code (TDD)
- Keep tests small and focused
- Avoid testing implementation details
- Prefer unit tests over integration tests
- Follow the Arrange–Act–Assert (AAA) pattern for clear and consistent test structure
- Use fixtures to avoid duplication and improve test maintainability
- Mock external dependencies (filesystem, database, network) to keep tests fast and deterministic
- Prefer parametrization over duplicate test functions for multiple input scenarios
- Run tests frequently and automatically during development
- Monitor test coverage to find untested code paths, but never rely on coverage alone for quality assurance

### 7. Common Mistakes

- Writing overly complex tests
- Sharing state between tests
- Skipping edge cases
- Ignoring failing tests12. Conclusion
- Writing tests that depend on the real filesystem, database, or network, making them slow and flaky
- Not following the Arrange–Act–Assert (AAA) pattern, leading to confusing test structure
- Duplicating setup code instead of using fixtures
- Ignoring edge cases and error scenarios
- Assuming 100% test coverage means bug-free code

### 8. Conclusion
Testing ensures code correctness, improves design, and provides confidence during refactoring and feature development. Effective unit testing with Pytest uses fixtures, mocking, and parametrization to create fast, reliable, and maintainable tests, while coverage helps identify gaps but does not guarantee bug-free code.