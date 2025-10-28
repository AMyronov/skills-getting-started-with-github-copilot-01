# FastAPI Tests

This directory contains comprehensive tests for the Mergington High School API using pytest and FastAPI's testing framework.

## Test Structure

### Test Files

- `conftest.py` - Test configuration and fixtures
- `test_api.py` - Main API endpoint tests

### Test Categories

#### 1. TestBasicEndpoints
Tests for basic API functionality:
- Root redirect functionality
- Getting activities list
- Response structure validation

#### 2. TestSignupEndpoint  
Tests for student signup functionality:
- Successful signup
- Handling non-existent activities
- Preventing duplicate signups
- Validating participant list updates

#### 3. TestRemoveParticipantEndpoint
Tests for participant removal functionality:
- Successful removal
- Handling non-existent activities
- Handling non-existent participants
- Validating participant list updates
- Testing removal and re-addition workflows

#### 4. TestEdgeCases
Tests for edge cases and special scenarios:
- URL encoding handling
- Email address encoding
- Activity capacity tracking

## Running Tests

### Using pytest directly:
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Run specific test class
pytest tests/test_api.py::TestSignupEndpoint -v

# Run specific test
pytest tests/test_api.py::TestSignupEndpoint::test_signup_success -v
```

### Using the test runner script:
```bash
# Run all tests with coverage
python run_tests.py

# Run specific test categories
python run_tests.py signup
python run_tests.py remove
python run_tests.py endpoints
python run_tests.py edge

# Show help
python run_tests.py help
```

## Test Fixtures

### `client` fixture
Provides a TestClient instance for making HTTP requests to the FastAPI application.

### `sample_activities` fixture  
Provides sample activity data for tests that need predictable data.

### `reset_activities` fixture (autouse)
Automatically resets the activities data to a known state before each test to ensure test isolation.

## Coverage

The current test suite achieves **100% code coverage** for the main application code (`src/app.py`).

## Test Data

Tests use a controlled set of activities:
- **Chess Club** - Pre-populated with 2 participants
- **Programming Class** - Pre-populated with 2 participants  
- **Test Activity** - Empty, designed for testing signup/removal functionality

## Dependencies

The tests require the following packages:
- `pytest` - Testing framework
- `pytest-asyncio` - Async support for pytest
- `pytest-cov` - Coverage reporting
- `httpx` - HTTP client for TestClient
- `fastapi` - Required for TestClient

All dependencies are listed in `requirements.txt` and can be installed with:
```bash
pip install -r requirements.txt
```

## Test Philosophy

These tests follow several key principles:

1. **Isolation** - Each test is independent and doesn't rely on state from other tests
2. **Comprehensive** - Tests cover happy paths, error cases, and edge cases
3. **Realistic** - Tests use realistic data and scenarios
4. **Fast** - Tests run quickly to encourage frequent execution
5. **Readable** - Test names and structure clearly indicate what is being tested

## Continuous Integration

The test suite is designed to be easily integrated into CI/CD pipelines. All tests should pass before code is merged or deployed.