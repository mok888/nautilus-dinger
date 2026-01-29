# Tests

Comprehensive test suite for Nautilus Paradex Adapter.

## Structure

```
tests/
├── python/
│   ├── integration/     # Integration tests (adapter, websocket, end-to-end)
│   ├── performance/     # Performance and stress tests
│   └── unit/           # Unit tests
├── rust/               # Rust unit tests
└── mocks/              # Mock servers for testing
```

## Running Tests

### Python Tests

```bash
# All tests
pytest tests/python/

# Integration tests only
pytest tests/python/integration/

# Performance tests
pytest tests/python/performance/

# Specific test
pytest tests/python/integration/test_end_to_end.py
```

### Rust Tests

```bash
# All Rust tests
cd crates/adapters/paradex
cargo test

# Specific test module
cargo test --test integration_tests
cargo test --test auth_tests
```

### Mock Servers

Start mock servers for local testing:

```bash
# HTTP mock server
python tests/mocks/http_server.py

# WebSocket mock server
python tests/mocks/ws_server.py
```

## Test Categories

### Integration Tests
- `test_end_to_end.py` - Full adapter flow
- `test_live_flow.py` - Live trading flow
- `test_adapter_loop.py` - Adapter event loop
- `test_rust_adapter.py` - Rust adapter integration
- `test_websocket_*.py` - WebSocket client tests
- `nautilus_*_test.py` - Nautilus framework integration

### Performance Tests
- `test_robustness_20_trades.py` - 20 trade robustness
- `test_race_conditions.py` - Concurrency tests
- `test_race_rust_vs_rest.py` - Rust vs REST performance
- `robustness_test.py` - Network resilience

### Rust Tests
- `integration_tests.rs` - Full integration suite
- `auth_tests.rs` - JWT authentication
- `signing_tests.rs` - STARK signature generation
- `config_tests.rs` - Configuration validation

## Configuration

Test configuration in `pytest.ini`:
- Test discovery patterns
- Async test support
- Coverage settings

## CI/CD

Tests run automatically on:
- Pull requests
- Main branch commits
- Release tags
