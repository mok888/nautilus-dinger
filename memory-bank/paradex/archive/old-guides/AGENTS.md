# AGENTS.md

**Generated:** 27-01-2026 14:56:00 GMT+8
**Purpose:** Hierarchical knowledge base for AI agents working on this project

## OVERVIEW
Nautilus Paradex Adapter - Production-grade trading system with Rust core and Python bindings. Ready for implementation and deployment.

## STRUCTURE

**Root** (/home/mok/projects/nautilus-dinger/)
├── memory-bank/          # Complete Paradex adapter implementation files
└── nautilus_trader/       # Target integration directory

**Memory Bank** (21 files total - reference documentation)
├── Python Implementation (7 files, ~2,800 LOC)
│   ├── execution.py         # LiveExecutionClient (1,000 LOC) ⭐ CRITICAL
│   ├── data.py             # LiveMarketDataClient (800 LOC) ⭐ CRITICAL
│   ├── providers.py         # InstrumentProvider (300 LOC)
│   ├── factories.py         # Type conversions (450 LOC)
│   ├── config.py           # Configuration classes
│   ├── constants.py         # Adapter constants
│   └── __init__.py         # Package exports
│
├── Rust Files (4 files, ~700 LOC)
│   ├── Cargo.toml           # Dependencies and build config
│   ├── lib.rs               # PyO3 module entry point
│   ├── config.rs             # Rust configuration structs
│   └── error.rs             # Error types and Result
│
└── Documentation (10 files, ~90K total)
    ├── README.md                           # Setup guide (3.7K)
    ├── START_HERE_QUICK_GUIDE.md        # Quick start (4.6K)
    ├── 1_RUST_CORE_IMPLEMENTATION.md     # Rust architecture (13K)
    ├── 2_PYTHON_ADAPTER_IMPLEMENTATION.md  # Python patterns (15K)
    ├── 3_IMPLEMENTATION_ROADMAP.md        # Step-by-step guide (9.6K)
    ├── MASTER_ALL_IN_ONE_COMPLETE.md       # Quick reference (12K)
    ├── Full-Production-Validation.md        # Production setup (17K)
    ├── agent-auto-validation.md             # Validation framework (12K)
    ├── progress.md                          # Project progress
    └── bug-fixes-record.md                 # Bug fixes log

## WHERE TO LOOK

### Paradex Adapter Implementation

| Task | Location | Notes |
|------|----------|-------|
| Execution client | memory-bank/execution.py | LiveExecutionClient with all 11 Nautilus methods |
| Market data client | memory-bank/data.py | LiveMarketDataClient with all 8 Nautilus methods |
| Type conversions | memory-bank/factories.py | Parse instruments, orders, fills |
| Configuration | memory-bank/config.py | ParadexConfig classes |
| Provider | memory-bank/providers.py | InstrumentProvider implementation |

### Rust Core (Production Layer)

| Component | Location | Role |
|-----------|----------|------|
| PyO3 bindings | memory-bank/lib.rs | Python interface |
| Configuration | memory-bank/config.rs | Config structs |
| Error handling | memory-bank/error.rs | ParadexError enum |
| Dependencies | memory-bank/Cargo.toml | Cargo configuration |

### Documentation (By Phase)

| Phase | Document | Purpose |
|-------|----------|---------|
| Quick start | START_HERE_QUICK_GUIDE.md | Begin here first |
| Rust details | 1_RUST_CORE_IMPLEMENTATION.md | STARK signing, HTTP client |
| Python details | 2_PYTHON_ADAPTER_IMPLEMENTATION.md | Idempotent reconciliation |
| Step-by-step | 3_IMPLEMENTATION_ROADMAP.md | 8-12 hour implementation |
| Quick reference | MASTER_ALL_IN_ONE_COMPLETE.md | Pattern lookup |
| Production | Full-Production-Validation.md | Complete setup with CI/CD |

## CODE MAP

### Key Python Classes

```python
# LiveExecutionClient - Order management
from nautilus_trader.adapters.paradex.execution import ParadexExecutionClient
# Required: 11 methods
# Critical: Idempotent reconciliation, fill deduplication

# LiveMarketDataClient - Market data
from nautilus_trader.adapters.paradex.data import ParadexDataClient
# Required: 8 methods
# Critical: WebSocket message routing

# InstrumentProvider - Instrument data
from nautilus_trader.adapters.paradex.providers import ParadexInstrumentProvider
# Required: 3 methods
# Critical: Load instruments from Paradex API
```

### Key Rust Modules

```rust
// STARK signing for order authentication
use crate::common::credential::StarkSigner;
// Signs orders with StarkNet private keys

// HTTP client with JWT auth
use crate::http::client::ParadexHttpClient;
// REST API communication

// PyO3 bindings
use crate::python::http::PyParadexHttpClient;
// Expose Rust to Python
```

## CONVENTIONS

### This Project

- **REST is authoritative**: Never trust WebSocket, always reconcile from REST
- **Idempotent operations**: Safe to restart/reconnect at any time
- **Fill deduplication**: Track emitted fills to prevent duplicates
- **STARK signatures**: All orders require StarkNet signing
- **Subkey authentication**: Safer than main account keys

### Python Style

- Type hints required on all functions
- Async/await for all I/O operations
- Pydantic for configuration validation
- pytest-asyncio for testing

### Rust Style

- Result<T> for error handling
- tokio for async runtime
- serde for serialization
- nautilus-network for HTTP (NOT reqwest directly)

## ANTI-PATTERNS (THIS PROJECT)

### FORBIDDEN

- ❌ DO NOT skip reconciliation on `_connect()`
- ❌ DO NOT trust WebSocket data over REST
- ❌ DO NOT omit type hints
- ❌ DO NOT skip fill deduplication
- ❌ DO NOT use reqwest directly (must use nautilus-network)
- ❌ DO NOT assume market data without caching
- ❌ DO NOT expose private keys in logs

### REQUIRED

- ✅ MUST implement all 11 LiveExecutionClient methods
- ✅ MUST implement all 8 LiveMarketDataClient methods
- ✅ MUST track emitted orders and fills
- ✅ MUST reconcile state from REST on connect
- ✅ MUST validate all configuration
- ✅ MUST write tests for all production code

## COMMANDS

```bash
# Setup directory structure
mkdir -p nautilus_trader/adapters/paradex
mkdir -p crates/adapters/paradex/src/{common,http,websocket,python}

# Copy implementation files
cp memory-bank/*.py nautilus_trader/adapters/paradex/
cp memory-bank/Cargo.toml crates/adapters/paradex/
cp memory-bank/*.rs crates/adapters/paradex/src/

# Build Rust layer
cd crates/adapters/paradex
maturin develop

# Test import
python -c "from nautilus_trader.adapters.paradex import PARADEX; print(PARADEX)"
```

## NOTES

### Implementation Status

**Complete in memory-bank:**
- All 7 Python adapter files ✅
- All 4 Rust core files ✅
- All 10 documentation files ✅

**To Implement (for full production):**
- Rust HTTP client (~500 LOC)
- Rust WebSocket client (~400 LOC)
- Rust STARK signing module (~200 LOC)
- Rust PyO3 bindings (~300 LOC)
- Python unit tests (~800 LOC)
- Python integration tests (~400 LOC)

### Gotchas

1. **STARK keys**: Subkey private key is 64 chars without "0x" prefix
2. **Account address**: Main account needs "0x" prefix
3. **Timestamp conversion**: Paradex uses milliseconds, Nautilus uses nanoseconds
4. **JWT caching**: Tokens expire after 1 hour
5. **Testnet vs Mainnet**: Different base URLs and chain IDs

### Integration Points

- **Nautilus Trader**: nautilus_trader package must be in PYTHONPATH
- **Paradex API**: Testnet for development, Mainnet for production
- **Maturin**: Required to build Rust-Python bindings
- **Python 3.10+**: Minimum version requirement

---

**Last Updated:** 27-01-2026 14:56:00 GMT+8
**Total Files in Memory Bank:** 21
**Total LOC:** ~3,500 (implementation) + ~90K (documentation)
