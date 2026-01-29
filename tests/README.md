# Test Directory

This directory contains all test files consolidated from across the project.

## Structure

- `python/` - Python test files
  - `integration/` - Integration tests
  - `unit/` - Unit tests
  - `performance/` - Performance and robustness tests
- `rust/` - Rust test files
  - `integration/` - Integration tests
  - `unit/` - Unit tests
- `mocks/` - Mock servers and test utilities

## Running Tests

### Python Tests
```bash
# Run all Python tests
python -m pytest tests/python/

# Run specific test categories
python -m pytest tests/python/integration/
python -m pytest tests/python/unit/
python -m pytest tests/python/performance/
```

### Rust Tests
```bash
# Run all Rust tests
cd crates/adapters/paradex && cargo test

# Run specific test files
cargo test --test integration_tests
cargo test --test auth_tests
```
