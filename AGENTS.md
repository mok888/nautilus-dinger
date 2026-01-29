# PROJECT KNOWLEDGE BASE

**Generated:** 2026-01-29 14:54 UTC
**Branch:** master

## OVERVIEW
Nautilus Paradex Adapter - Trading system connecting Nautilus Trader framework to Paradex DEX exchange. Rust core (PyO3 bindings) + Python adapter layer.

## STRUCTURE

```
nautilus-dinger/
├── crates/adapters/paradex/    # Rust core
│   ├── src/
│   │   ├── auth/               # JWT authentication
│   │   ├── http/               # REST API client
│   │   ├── websocket/          # WebSocket client
│   │   ├── signing/            # STARK signature generation
│   │   ├── state/              # Reconciliation & state management
│   │   ├── python/             # PyO3 bindings
│   │   └── common/             # Shared types
│   ├── tests/                  # Rust tests (auth, signing, integration)
│   └── Cargo.toml
├── nautilus_trader/adapters/paradex/  # Python adapter layer
│   ├── execution.py            # LiveExecutionClient
│   ├── data.py                 # LiveMarketDataClient
│   ├── providers.py            # InstrumentProvider
│   ├── factories.py            # Type conversions
│   ├── config.py               # Configuration
│   ├── constants.py            # Constants
│   └── _rust.py                # Rust wrapper
├── scripts/                    # Organized scripts
│   ├── trading/                # Trading bots (7 scripts)
│   ├── monitoring/             # Dashboards (7 scripts)
│   └── utils/                  # Testing utilities (6 scripts)
├── tests/                      # Test suite
│   ├── python/
│   │   ├── integration/        # Integration tests
│   │   ├── performance/        # Performance tests
│   │   └── unit/              # Unit tests
│   └── mocks/                  # Mock servers
├── examples/                   # Usage examples
│   └── order_placement/        # Order placement examples
├── config/                     # Configuration files
├── docs/                       # Documentation
└── memory-bank/                # Development notes
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| **Rust Core** | | |
| HTTP client | `crates/adapters/paradex/src/http/client.rs` | REST API with JWT auth |
| WebSocket | `crates/adapters/paradex/src/websocket/` | JSON-RPC client |
| STARK signing | `crates/adapters/paradex/src/signing/signer.rs` | Order signing |
| Auth/JWT | `crates/adapters/paradex/src/auth/jwt.rs` | JWT tokens |
| State mgmt | `crates/adapters/paradex/src/state/` | Reconciliation |
| PyO3 bindings | `crates/adapters/paradex/src/python/mod.rs` | Python interface |
| **Python Adapter** | | |
| Execution | `nautilus_trader/adapters/paradex/execution.py` | Order execution |
| Market data | `nautilus_trader/adapters/paradex/data.py` | Market data feed |
| Instruments | `nautilus_trader/adapters/paradex/providers.py` | Instrument provider |
| Factories | `nautilus_trader/adapters/paradex/factories.py` | Type conversions |
| **Scripts** | | |
| Trading | `scripts/trading/live_trader.py` | Main trading bot |
| Monitoring | `scripts/monitoring/monitoring_dashboard.py` | Live dashboard |
| Utils | `scripts/utils/rust_20_trades.py` | Performance test |
| **Tests** | | |
| Integration | `tests/python/integration/` | End-to-end tests |
| Performance | `tests/python/performance/` | Stress tests |
| Rust tests | `crates/adapters/paradex/tests/` | Rust unit tests |
| **Examples** | | |
| Orders | `examples/order_placement/` | Order examples |

## COMMANDS

```bash
# Build
make dev              # Development build
make build            # Release build

# Test
make test             # All tests
make test-py          # Python tests only
make test-rust        # Rust tests only

# Run
python scripts/trading/live_trader.py
python scripts/monitoring/monitoring_dashboard.py

# Clean
make clean
```

## KEY FILES

- `Makefile` - Build automation
- `pyproject.toml` - Python project config
- `Cargo.toml` - Rust workspace config
- `config/.env.testnet` - Testnet configuration

---

**Last Updated:** 2026-01-29 14:54 UTC
