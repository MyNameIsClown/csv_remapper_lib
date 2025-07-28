
# Contributing to CSV Remapper Library

First of all, thank you for your interest in contributing to this project!
Your help is highly appreciated. This document outlines the process for contributing and the standards we expect.

## Table of Contents

* [Getting Started](#getting-started)
* [How to Contribute](#how-to-contribute)
* [Code Style](#code-style)
* [Running Tests](#running-tests)
* [Pull Request Guidelines](#pull-request-guidelines)
* [Reporting Issues](#reporting-issues)
* [License](#license)

---

## Getting Started

1. Fork the repository.

2. Clone your fork:

   ```bash
   git clone https://github.com/MyNameIsClown/csv-remapper-lib.git
   cd csv-remapper-lib
   ```

3. Install dependencies with [Poetry](https://python-poetry.org/):

   ```bash
   poetry install
   ```

4. Activate the virtual environment:

   ```bash
   poetry shell
   ```

---

## How to Contribute

* 🐛 **Report bugs** using [GitHub Issues](https://github.com/your-username/csv-remapper-lib/issues)
* 📚 **Improve the documentation**
* 💡 **Propose features** or enhancements
* 🔧 **Fix bugs** or implement missing functionality
* ✅ **Write and improve tests**

---

## Code Style

This project follows:

* [PEP8](https://peps.python.org/pep-0008/)
* [Black](https://black.readthedocs.io/en/stable/) for formatting
* [isort](https://pycqa.github.io/isort/) for import order

You can format your code with:

```bash
poetry run black .
poetry run isort .
```

---

## Running Tests

Before submitting a PR, make sure all tests pass:

```bash
poetry run pytest
```

To check test coverage:

```bash
poetry run pytest --cov=csv_remapper_lib
```

---

## Pull Request Guidelines

* Base your PR on the latest `main` branch.
* Use clear and descriptive titles.
* Add related issue number if applicable (e.g., `Fixes #42`).
* Include tests for new functionality.
* Keep commits clean and focused.

---

## Reporting Issues

Please include:

* A clear and descriptive title
* Steps to reproduce the issue
* Expected vs actual behavior
* Stack trace or error message if applicable
* Environment (OS, Python version, etc.)

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project: **AGPL v3**.