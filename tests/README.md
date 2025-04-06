# Test Setup Instructions

This document explains how to set up and run the automated tests for the TDDD96_2025_PUM14 project.

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Node.js and npm (for running the application)

## Setup Instructions

1. **Install Python Dependencies**

   ```bash
   pip install -r tests/requirements.txt
   ```

2. **Install Playwright Browsers**

   ```bash
   playwright install
   ```

3. **Start the Application**

   In a separate terminal, start the application:

   ```bash
   npm run dev
   ```

## Running Tests

### Running all tests

```bash
python3 -m pytest tests/unittests/
```

### Running specific test files

```bash
python3 -m pytest tests/unittests/test_filter.py
```

### Running tests with HTML reports

```bash
python3 -m pytest tests/unittests/ --html=report.html
```

The HTML report will be generated at the root of the project directory.

### Running tests with XML reports (for CI/CD)

```bash
python3 -m pytest tests/unittests/ --junitxml=test-results.xml
```

## Test Structure

- `tests/unittests/`: Contains all unit and integration tests
  - `test_filter.py`: Tests for the filter functionality
  - `test_document_view.py`: Tests for the document view functionality
  - `test_listvy.py`: Tests for the list view functionality

## Debugging Tests

If a test fails, you can check the HTML report for details about the failure. The report includes:
- Test execution summary
- Detailed error messages
- Screenshots (if enabled)

To enable screenshots for failing tests, modify the `pytest.ini` file at the root of the project:

```ini
[pytest]
addopts = --html=report.html --self-contained-html
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

[pytest-playwright]
screenshot = on
video = on
trace = on
``` 