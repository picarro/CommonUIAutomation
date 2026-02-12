# Running Tests Guide

This guide shows you how to run the test files in this framework.

## Running test_storybook_controls.py

### Method 1: Run all controls tests (Recommended)

```bash
# Using pytest marker
pytest -m controls

# Or using Makefile
make test-controls
```

### Method 2: Run specific test file

```bash
# Run the entire test file
pytest tests/test_storybook_controls.py

# Run with verbose output
pytest tests/test_storybook_controls.py -v

# Run with extra verbose output
pytest tests/test_storybook_controls.py -vv
```

### Method 3: Run specific test function

```bash
# Run a specific test function
pytest tests/test_storybook_controls.py::TestStorybookControls::test_update_single_control

# Run with verbose output
pytest tests/test_storybook_controls.py::TestStorybookControls::test_update_single_control -v
```

### Method 4: Run specific test class

```bash
# Run all tests in the TestStorybookControls class
pytest tests/test_storybook_controls.py::TestStorybookControls
```

## Running Other Test Files

### Property Checker Tests

```bash
# Run all property tests
pytest -m property
# or
make test-property

# Run specific file
pytest tests/test_property_checker.py
```

### Visual Regression Tests

```bash
# Run all visual tests
pytest -m visual
# or
make test-visual

# Run specific file
pytest tests/test_visual_regression.py
```

### Interaction Tests

```bash
# Run all interaction tests
pytest -m interaction
# or
make test-interaction

# Run specific file
pytest tests/test_interaction.py
```

### State Tests

```bash
# Run all state tests
pytest -m state
# or
make test-state

# Run specific file
pytest tests/test_state.py
```

### Snapshot Tests

```bash
# Run all snapshot tests
pytest -m snapshot
# or
make test-snapshot

# Run specific file
pytest tests/test_snapshot.py
```

## Running All Tests

```bash
# Run all tests
pytest

# Or using Makefile
make test

# Run all tests with HTML report
make test-all
```

## Useful pytest Options

### Verbose Output

```bash
# More verbose output
pytest -v

# Even more verbose
pytest -vv

# Show print statements
pytest -s
```

### Stop on First Failure

```bash
# Stop after first failure
pytest -x

# Stop after N failures
pytest --maxfail=3
```

### Run Tests in Parallel

```bash
# Install pytest-xdist first: pip install pytest-xdist
pytest -n auto  # Uses all CPU cores
pytest -n 4    # Uses 4 workers
```

### Show Test Coverage

```bash
# Install pytest-cov first: pip install pytest-cov
pytest --cov=framework --cov-report=html
```

### Run Tests Matching a Pattern

```bash
# Run tests matching a pattern
pytest -k "control"  # Runs all tests with "control" in the name
pytest -k "update"   # Runs all tests with "update" in the name
```

### Run Tests and Show Output

```bash
# Show print statements and output
pytest -s

# Show print statements with verbose
pytest -sv
```

## Viewing Test Reports

After running tests, HTML reports are generated in the `reports/` directory:

```bash
# Open the HTML report
open reports/report.html  # macOS
xdg-open reports/report.html  # Linux
start reports/report.html  # Windows
```

## Common Issues

### Storybook Not Running

Make sure Storybook is running before executing tests:

```bash
# In your Storybook project directory
npm run storybook
# or
yarn storybook
```

### Import Errors

If you get import errors, make sure you're in the virtual environment:

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### Browser Not Found

Install Playwright browsers:

```bash
playwright install
# or
make browsers
```

## Quick Reference

| Command | Description |
|--------|-------------|
| `pytest -m controls` | Run all controls tests |
| `pytest tests/test_storybook_controls.py` | Run specific file |
| `pytest -k "test_update"` | Run tests matching pattern |
| `pytest -v` | Verbose output |
| `pytest -s` | Show print statements |
| `pytest -x` | Stop on first failure |
| `make test-controls` | Run controls tests (Makefile) |
| `make test-all` | Run all tests with HTML report |

