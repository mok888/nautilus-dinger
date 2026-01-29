# PROJECT KNOWLEDGE BASE

**Generated:** 2026-01-29 14:38 UTC
**Commit:** N/A
**Branch:** master

## OVERVIEW
Nautilus Paradex Adapter - Trading system connecting Nautilus Trader framework to Paradex DEX exchange. Rust core (PyO3 bindings) + Python adapter layer.

## STRUCTURE

```
.
├── crates/adapters/paradex/    # Rust core: auth, HTTP, WebSocket, STARK signing
│   ├── src/
│   │   ├── auth/               # JWT authentication
│   │   ├── http/               # REST API client
│   │   ├── websocket/          # WebSocket client
│   │   ├── signing/            # STARK signature generation
│   │   ├── state/              # Reconciliation & state management
│   │   ├── python/             # PyO3 bindings
│   │   └── common/             # Shared types
│   └── Cargo.toml              # Rust dependencies
├── nautilus_trader/adapters/paradex/  # Python adapter layer
│   ├── execution.py            # LiveExecutionClient (11 methods)
│   ├── data.py                 # LiveMarketDataClient (8 methods)
│   ├── providers.py            # InstrumentProvider (3 methods)
│   ├── factories.py            # Type conversions
│   ├── config.py               # Configuration classes
│   ├── constants.py            # Constants
│   └── _rust.py                # Rust Python wrapper
├── tests/                      # Test suite
│   ├── python/integration/     # Integration tests
│   └── mocks/                  # Test fixtures
├── memory-bank/paradex/        # Documentation & reference
└── [*.py scripts]             # Trading bot scripts (root level)
    ├── live_trader.py         # Main trading bot
    ├── place_order.py         # Order placement
    ├── check_account.py       # Account checks
    └── monitoring_dashboard.py # Dashboard
    ├── tracking/               # Progress tracking
    └── archive/                # Historical docs
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| **Rust Core** | | |
| HTTP client | `crates/adapters/paradex/src/http/client.rs` | ParadexHttpClient with JWT auth |
| WebSocket client | `crates/adapters/paradex/src/websocket/` | JSON-RPC, message handlers |
| STARK signing | `crates/adapters/paradex/src/signing/signer.rs` | Order signing with lambdaworks |
| Auth/JWT | `crates/adapters/paradex/src/auth/jwt.rs` | JWT token generation |
| State management | `crates/adapters/paradex/src/state/` | Reconciliation, DashMap for concurrency |
| **Python Adapter** | | |
| Execution client | `nautilus_trader/adapters/paradex/execution.py` | LiveExecutionClient |
| Market data client | `nautilus_trader/adapters/paradex/data.py` | LiveMarketDataClient |
| Instrument provider | `nautilus_trader/adapters/paradex/providers.py` | ParadexInstrumentProvider |
| Type conversions | `nautilus_trader/adapters/paradex/factories.py` | Parse instruments, orders, fills |
| **Scripts** | | |
| Trading bots | `scripts/trading/` | live_trader.py, place_order.py, etc. |
| Monitoring | `scripts/monitoring/` | monitoring_dashboard.py, live_btc_price.py |
| Utilities | `scripts/utils/` | Examples, performance tests |
| **Documentation** | | |
| Quick start | `README.md` | Setup guide |
| Reference | `memory-bank/paradex/` | Implementation guides |

## COMMANDS

```bash
# Build Rust layer
cd crates/adapters/paradex
maturin develop

# Run tests
cd tests
pytest

# Run trading bot
python scripts/trading/live_trader.py

# Check account
python scripts/trading/check_account.py

# Place order
python scripts/trading/place_order.py

# Monitor dashboard
python scripts/monitoring/monitoring_dashboard.py
```

---

**Last Updated:** 2026-01-29 14:38 UTC
