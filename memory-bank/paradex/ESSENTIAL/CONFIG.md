# CONFIG - CONFIGURATION GUIDE

**Purpose:** Configuration, credentials, and setup details

---

## 🚀 PREREQUISITES

### Install Nautilus Trader
```bash
# Install Nautilus Trader via pip
pip install nautilus_trader

# Verify installation
python -c "import nautilus_trader; print(f'Nautilus Trader {nautilus_trader.__version__} installed')"
```

---

## 🔐 TESTNET CREDENTIALS

### Location
```bash
/home/mok/projects/nautilus-dinger/.env.testnet
```

### Contents
```bash
PARADEX_ENVIRONMENT=testnet
PARADEX_L2_ADDRESS=0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8
PARADEX_SUBKEY_PRIVATE_KEY=0x0441c1622edc5a77891cf97cd76c4ff097211f3df4493425fb9519e06ff8cf55
```

### Usage
```python
import os
from dotenv import load_dotenv

load_dotenv(".env.testnet")

config = ParadexExecClientConfig(
    environment=os.getenv("PARADEX_ENVIRONMENT"),
    main_account_address=os.getenv("PARADEX_L2_ADDRESS"),
    subkey_private_key=os.getenv("PARADEX_SUBKEY_PRIVATE_KEY"),
)
```

---

## ⚙️ PYTHON CONFIGURATION

### Data Client Config

```python
from nautilus_trader.adapters.paradex.config import ParadexDataClientConfig

config = ParadexDataClientConfig(
    environment="testnet",  # or "mainnet"
    base_url_http=None,     # Auto-detected from environment
    base_url_ws=None,       # Auto-detected from environment
)
```

### Execution Client Config

```python
from nautilus_trader.adapters.paradex.config import ParadexExecClientConfig

config = ParadexExecClientConfig(
    environment="testnet",
    main_account_address="0x...",
    subkey_private_key="0x...",
    reconcile_interval_secs=300.0,  # 5 minutes
)
```

### Full Adapter Config

```python
from nautilus_trader.config import TradingNodeConfig
from nautilus_trader.adapters.paradex.config import ParadexDataClientConfig, ParadexExecClientConfig

config = TradingNodeConfig(
    data_clients={
        "PARADEX": ParadexDataClientConfig(
            environment="testnet",
        ),
    },
    exec_clients={
        "PARADEX": ParadexExecClientConfig(
            environment="testnet",
            main_account_address=os.getenv("PARADEX_L2_ADDRESS"),
            subkey_private_key=os.getenv("PARADEX_SUBKEY_PRIVATE_KEY"),
            reconcile_interval_secs=300.0,
        ),
    },
)
```

---

## 🌐 ENVIRONMENT CONFIGURATION

### Testnet
```python
ENVIRONMENT = "testnet"
BASE_URL_HTTP = "https://api.testnet.paradex.trade/v1"
BASE_URL_WS = "wss://ws.testnet.paradex.trade/v1"
CHAIN_ID = "SEPOLIA"
```

### Mainnet
```python
ENVIRONMENT = "mainnet"
BASE_URL_HTTP = "https://api.paradex.trade/v1"
BASE_URL_WS = "wss://ws.paradex.trade/v1"
CHAIN_ID = "MAINNET"
```

---

## 🔑 AUTHENTICATION

### JWT Token (HTTP)
```python
# Automatically handled by HTTP client
# Token cached for 1 hour
# Auto-refreshed on expiry

headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Content-Type": "application/json",
}
```

### STARK Signature (Orders)
```python
# All orders require STARK signature
# Implemented in Rust layer
# Uses subkey private key

signed_order = await http_client.sign_and_submit_order({
    "market": "BTC-USD-PERP",
    "side": "BUY",
    "type": "LIMIT",
    "size": "0.1",
    "price": "50000",
})
```

---

## 📊 RECONCILIATION CONFIGURATION

### Default Settings
```python
reconcile_interval_secs = 300.0  # 5 minutes
reconcile_on_connect = True      # Always reconcile on connect
deduplicate_fills = True         # Track emitted fills
```

### Custom Settings
```python
config = ParadexExecClientConfig(
    # ... other settings ...
    reconcile_interval_secs=600.0,  # 10 minutes
)
```

### Reconciliation Behavior
- **On Connect:** Always reconcile state from REST
- **Periodic:** Every N seconds (default: 300)
- **Fill Deduplication:** Track emitted fills to prevent duplicates
- **REST Authoritative:** REST data takes priority over WebSocket

---

## 🔧 RUST CONFIGURATION

### Cargo.toml Dependencies
```toml
[dependencies]
nautilus-core = { path = "../../core" }
nautilus-model = { path = "../../model" }
nautilus-network = { path = "../../network" }
pyo3 = "0.20"
pyo3-asyncio = { version = "0.20", features = ["tokio-runtime"] }
tokio = { version = "1", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
dashmap = "5.5"
thiserror = "1.0"
starknet-crypto = "0.6"
```

### Build Configuration
```toml
[lib]
name = "paradex"
crate-type = ["cdylib"]

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
```

---

## 📁 FILE STRUCTURE

### Python Files
```
nautilus_trader/adapters/paradex/
├── __init__.py           # Package exports
├── config.py             # Configuration classes
├── constants.py          # Adapter constants
├── data.py              # LiveMarketDataClient
├── execution.py         # LiveExecutionClient
├── providers.py         # InstrumentProvider
└── factories.py         # Type conversions
```

### Rust Files
```
crates/adapters/paradex/
├── Cargo.toml           # Dependencies
└── src/
    ├── lib.rs           # PyO3 module entry
    ├── config.rs        # Rust config structs
    ├── error.rs         # Error types
    ├── common/
    │   ├── credential.rs  # STARK signing
    │   └── types.rs       # Common types
    ├── http/
    │   ├── client.rs      # HTTP client
    │   └── auth.rs        # JWT auth
    ├── websocket/
    │   ├── client.rs      # WebSocket client
    │   └── protocol.rs    # JSON-RPC
    └── python/
        ├── http.rs        # PyO3 HTTP bindings
        └── websocket.rs   # PyO3 WS bindings
```

---

## 🧪 TEST CONFIGURATION

### Test Environment
```bash
# Use testnet for all tests
export PARADEX_ENVIRONMENT=testnet
export PARADEX_L2_ADDRESS=0x...
export PARADEX_SUBKEY_PRIVATE_KEY=0x...
```

### Pytest Configuration
```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
```

### Test Coverage
```bash
# Run with coverage
pytest tests/ --cov=nautilus_trader/adapters/paradex --cov-report=html

# Target: >85% coverage
```

---

## 💰 CREDIT ESTIMATES

### Phase Breakdown
| Phase | Time | Credits | Notes |
|-------|------|---------|-------|
| Phase 1: Python | 12.5h | 200-250 | Implementation + refactor + tests |
| Phase 2: Rust | 38h | 650-800 | Full Rust layer |
| Phase 3: Testing | 14h | 180-250 | Comprehensive testing |
| Phase 4: Docs | 3.5h | 40-60 | Documentation |
| **TOTAL** | **68h** | **1,100-1,400** | **Full implementation** |

### Credit Rate Assumptions
- Implementation: 15-20 credits/hour
- Refactoring: 12-15 credits/hour
- Testing: 12-18 credits/hour
- Validation: 8-12 credits/hour
- Bug fixing: 18-25 credits/hour

---

## 📊 QUALITY METRICS

### Target Metrics
- **Test Coverage:** >85% (Python), >80% (Rust)
- **Code Quality:** Pylint score >7.0
- **Performance:** <1ms state access, <10ms order submission
- **Reliability:** Zero duplicate fills, zero missed orders
- **Compliance:** 100% Nautilus specification

### Quality Gates
- **After Phase 1:** Python complete, tested, refactored
- **After Phase 2:** Rust complete, tested, optimized
- **After Phase 3:** Full system tested, bugs fixed
- **After Phase 4:** Production ready

---

## 🔒 SECURITY

### Credential Management
```bash
# NEVER commit credentials
# Use .env files (in .gitignore)
# Use environment variables in production

# .gitignore
.env
.env.*
*.key
*.pem
```

### Key Safety
- **Main Account:** Only for authentication
- **Subkey:** Used for order signing (safer)
- **Private Keys:** Never log or expose
- **JWT Tokens:** Cache but don't persist

---

## 🚀 DEPLOYMENT

### Development
```bash
# Use testnet
export PARADEX_ENVIRONMENT=testnet
python main.py
```

### Production
```bash
# Use mainnet
export PARADEX_ENVIRONMENT=mainnet
export PARADEX_L2_ADDRESS=<production_address>
export PARADEX_SUBKEY_PRIVATE_KEY=<production_key>
python main.py
```

### Monitoring
- Log all reconciliation runs
- Track fill deduplication
- Monitor connection state
- Alert on errors

---

## 📚 REFERENCE

### API Documentation
- Paradex API: https://docs.paradex.trade/
- Nautilus Trader: https://nautilustrader.io/docs/

### Code References
- OKX adapter: Primary reference
- BitMEX adapter: Secondary reference
- Bybit adapter: Secondary reference

### Support
- Nautilus Discord: https://discord.gg/nautilus
- Paradex Discord: https://discord.gg/paradex

---

**Next: Begin implementation with WORKFLOW.md**
