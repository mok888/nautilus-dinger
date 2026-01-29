.PHONY: test test-python test-rust test-integration test-unit test-performance clean

# Run all tests
test: test-python test-rust

# Python tests
test-python:
	cd tests && python -m pytest python/ -v

test-python-integration:
	cd tests && python -m pytest python/integration/ -v

test-python-unit:
	cd tests && python -m pytest python/unit/ -v

test-python-performance:
	cd tests && python -m pytest python/performance/ -v

# Rust tests
test-rust:
	cd crates/adapters/paradex && cargo test

test-rust-integration:
	cd crates/adapters/paradex && cargo test --test integration_tests
	cd crates/adapters/paradex && cargo test --test auth_tests
	cd crates/adapters/paradex && cargo test --test signing_tests
	cd crates/adapters/paradex && cargo test --test config_tests

# Clean test artifacts
clean:
	find tests/ -name "*.pyc" -delete
	find tests/ -name "__pycache__" -type d -exec rm -rf {} +
	cd crates/adapters/paradex && cargo clean
