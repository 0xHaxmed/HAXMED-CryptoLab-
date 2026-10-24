# HAXMED CryptoLab — Developer Guide

## 1. Prerequisites
- Python 3.10+
- Virtual environment (`.venv`)
- Git

## 2. Environment Setup

### Windows
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

### Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## 3. Running the Test Suite

We use `pytest` with `pytest-qt` for headless and widget-level testing.

Run all tests:
```bash
pytest
```

Run specific test categories:
```bash
pytest tests/unit/
pytest tests/integration/
pytest tests/ui/
pytest tests/security/
```

## 4. Code Quality & Linting

Run `ruff` linter and formatting checks:
```bash
ruff check .
ruff format --check .
```

To auto-format:
```bash
ruff format .
```

## 5. Adding a New Cryptographic Algorithm

1. **Engine Layer**: Implement the algorithm in `src/haxmed_cryptolab/engines/<category>/`. The engine class must be pure Python with zero GUI dependencies.
2. **Models Layer**: Add input and output data models in `src/haxmed_cryptolab/models/`.
3. **Service Layer**: Add orchestration and validation methods in `src/haxmed_cryptolab/services/`.
4. **UI Layer**: Connect the service methods to the appropriate view/page in `src/haxmed_cryptolab/ui/pages/`.
5. **Testing**: Add unit tests in `tests/unit/` covering round-trips, boundary conditions, and invalid inputs.
