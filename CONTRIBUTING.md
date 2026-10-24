# Contributing to HAXMED CryptoLab

Thank you for your interest in contributing to HAXMED CryptoLab.

## Code Standards

- Follow PEP 8 guidelines enforced via `ruff`.
- Include full type annotations where appropriate (`typing`).
- Ensure unit and integration tests are provided for every new cryptographic engine or UI component.
- Keep business and cryptographic logic decoupled from Qt UI classes.
- Ensure all user-facing strings are translatable (support both English LTR and Arabic RTL).

## Workflow

1. Clone or set up the repository:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux:
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```
2. Run tests:
   ```bash
   pytest
   ```
3. Run linting:
   ```bash
   ruff check .
   ```
