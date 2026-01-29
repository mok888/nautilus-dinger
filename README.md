# Nautilus Dinger

Paradex trading adapter for Nautilus Trader framework.

## Project Structure

```
nautilus-dinger/
├── crates/adapters/paradex/     # Rust core (auth, HTTP, WebSocket, STARK signing)
├── nautilus_trader/adapters/    # Python adapter layer
├── scripts/                     # Utility scripts
│   ├── trading/                 # Trading bots and order management
│   ├── monitoring/              # Live monitoring and dashboards
│   └── utils/                   # Test utilities and examples
├── tests/                       # Test suite
│   ├── python/                  # Python tests
│   └── mocks/                   # Mock servers
├── config/                      # Configuration files
├── docs/                        # Documentation
└── memory-bank/                 # Development notes
```

## Quick Start

```bash
# Install dependencies
source .venv/bin/activate
pip install maturin

# Build Rust adapter
cd crates/adapters/paradex
maturin develop

# Configure
cp config/.env.testnet .env
# Edit .env with your credentials

# Run trading bot
python scripts/trading/live_trader.py
```

## Scripts

**Trading:**
- `scripts/trading/live_trader.py` - Main trading bot
- `scripts/trading/place_order.py` - Place orders
- `scripts/trading/check_account.py` - Check account status

**Monitoring:**
- `scripts/monitoring/monitoring_dashboard.py` - Live dashboard
- `scripts/monitoring/live_btc_price.py` - BTC price feed

**Utils:**
- `scripts/utils/rust_20_trades.py` - Performance testing
- `scripts/utils/simple_trading_loop.py` - Simple example

## Documentation

See `memory-bank/paradex/` for detailed implementation guides and reference.
