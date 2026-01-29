# Makefile for Nautilus Dinger

.PHONY: help build test clean install dev

help:
	@echo "Nautilus Dinger - Paradex Trading Adapter"
	@echo ""
	@echo "Available targets:"
	@echo "  make install    - Install dependencies"
	@echo "  make build      - Build Rust adapter"
	@echo "  make dev        - Build in development mode"
	@echo "  make test       - Run all tests"
	@echo "  make test-py    - Run Python tests only"
	@echo "  make test-rust  - Run Rust tests only"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make format     - Format code"
	@echo "  make lint       - Lint code"

install:
	pip install -e ".[dev]"

build:
	cd crates/adapters/paradex && maturin build --release

dev:
	cd crates/adapters/paradex && maturin develop

test: test-rust test-py

test-py:
	pytest tests/python/

test-rust:
	cd crates/adapters/paradex && cargo test

clean:
	rm -rf target/
	rm -rf .pytest_cache/
	rm -f paradex_adapter.so
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

format:
	cd crates/adapters/paradex && cargo fmt
	black nautilus_trader/ scripts/ tests/python/ examples/

lint:
	cd crates/adapters/paradex && cargo clippy
	ruff check nautilus_trader/ scripts/ tests/python/ examples/
