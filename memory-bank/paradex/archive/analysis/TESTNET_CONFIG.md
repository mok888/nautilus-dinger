# PARADEX TESTNET CONFIGURATION

**Date:** 2026-01-27  
**Environment:** TESTNET ONLY  
**Status:** Ready for testing

---

## 🔑 TESTNET CREDENTIALS

### Environment Variables:

```bash
# Paradex Testnet Configuration
export PARADEX_ENVIRONMENT="testnet"
export PARADEX_L2_ADDRESS="0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8"
export PARADEX_SUBKEY_PRIVATE_KEY="0x0441c1622edc5a77891cf97cd76c4ff097211f3df4493425fb9519e06ff8cf55"
```

### Configuration File (.env):

```bash
# .env.testnet
PARADEX_ENVIRONMENT=testnet
PARADEX_L2_ADDRESS=0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8
PARADEX_SUBKEY_PRIVATE_KEY=0x0441c1622edc5a77891cf97cd76c4ff097211f3df4493425fb9519e06ff8cf55

# Testnet API URLs
PARADEX_BASE_URL_HTTP=https://api.testnet.paradex.trade/v1
PARADEX_BASE_URL_WS=wss://ws.testnet.paradex.trade/v1
```

---

## 🔧 PYTHON CONFIGURATION

### Using in Code:

```python
import os
from nautilus_trader.adapters.paradex.config import ParadexExecClientConfig

# Load from environment
config = ParadexExecClientConfig(
    environment="testnet",
    main_account_address=os.getenv("PARADEX_L2_ADDRESS"),
    subkey_private_key=os.getenv("PARADEX_SUBKEY_PRIVATE_KEY"),
    reconcile_interval_secs=300.0,
)
```

### Using with python-dotenv:

```python
from dotenv import load_dotenv
import os

# Load .env.testnet
load_dotenv(".env.testnet")

config = ParadexExecClientConfig(
    environment="testnet",
    main_account_address=os.getenv("PARADEX_L2_ADDRESS"),
    subkey_private_key=os.getenv("PARADEX_SUBKEY_PRIVATE_KEY"),
)
```

---

## 🦀 RUST CONFIGURATION

### Using in Rust:

```rust
use std::env;

// Load from environment
let l2_address = env::var("PARADEX_L2_ADDRESS")
    .expect("PARADEX_L2_ADDRESS not set");
let subkey_private_key = env::var("PARADEX_SUBKEY_PRIVATE_KEY")
    .expect("PARADEX_SUBKEY_PRIVATE_KEY not set");

let config = ParadexConfig {
    environment: Environment::Testnet,
    l2_address,
    subkey_private_key,
    base_url_http: "https://api.testnet.paradex.trade/v1".to_string(),
    base_url_ws: "wss://ws.testnet.paradex.trade/v1".to_string(),
};
```

---

## ⚠️ SECURITY NOTES

### TESTNET ONLY:
- ✅ These credentials are for TESTNET only
- ✅ Safe to use for development and testing
- ✅ No real funds at risk

### DO NOT:
- ❌ Use these keys on mainnet
- ❌ Commit to public repositories
- ❌ Share mainnet keys in documentation
- ❌ Store keys in code (use environment variables)

### BEST PRACTICES:
- ✅ Use `.env` files (add to `.gitignore`)
- ✅ Use environment variables
- ✅ Rotate keys periodically
- ✅ Use subkeys (not main account keys)

---

## 🧪 TESTING SETUP

### Quick Test Script:

```bash
#!/bin/bash
# test_paradex_connection.sh

# Set testnet credentials
export PARADEX_ENVIRONMENT="testnet"
export PARADEX_L2_ADDRESS="0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8"
export PARADEX_SUBKEY_PRIVATE_KEY="0x0441c1622edc5a77891cf97cd76c4ff097211f3df4493425fb9519e06ff8cf55"

# Test connection
python -c "
from nautilus_trader.adapters.paradex.config import ParadexExecClientConfig
import os

config = ParadexExecClientConfig(
    environment='testnet',
    main_account_address=os.getenv('PARADEX_L2_ADDRESS'),
    subkey_private_key=os.getenv('PARADEX_SUBKEY_PRIVATE_KEY'),
)

print('✅ Configuration loaded successfully')
print(f'Environment: {config.environment}')
print(f'L2 Address: {config.main_account_address[:10]}...')
"
```

### Python Test:

```python
# test_connection.py
import asyncio
import os
from nautilus_trader.adapters.paradex.execution import ParadexExecutionClient
from nautilus_trader.adapters.paradex.config import ParadexExecClientConfig

async def test_connection():
    config = ParadexExecClientConfig(
        environment="testnet",
        main_account_address=os.getenv("PARADEX_L2_ADDRESS"),
        subkey_private_key=os.getenv("PARADEX_SUBKEY_PRIVATE_KEY"),
    )
    
    # Create client (requires full Nautilus setup)
    # client = ParadexExecutionClient(...)
    # await client.connect()
    
    print("✅ Configuration valid")

if __name__ == "__main__":
    asyncio.run(test_connection())
```

---

## 📋 VALIDATION CHECKLIST

### Before Testing:
- [ ] Environment variables set
- [ ] Testnet environment confirmed
- [ ] Keys loaded correctly
- [ ] API URLs point to testnet

### During Testing:
- [ ] Connection successful
- [ ] Authentication works
- [ ] Can query account info
- [ ] Can submit test orders

### After Testing:
- [ ] No errors in logs
- [ ] State reconciliation works
- [ ] WebSocket stable
- [ ] Ready for development

---

## 🔗 TESTNET RESOURCES

### Paradex Testnet:
- **API Docs:** https://docs.paradex.trade/
- **Testnet UI:** https://testnet.paradex.trade/
- **Status:** https://status.paradex.trade/

### StarkNet Testnet:
- **Explorer:** https://testnet.starkscan.co/
- **Faucet:** https://faucet.goerli.starknet.io/

---

## 📝 CONFIGURATION REFERENCE

### Required Fields:

| Field | Value | Description |
|-------|-------|-------------|
| `PARADEX_ENVIRONMENT` | `testnet` | Environment selector |
| `PARADEX_L2_ADDRESS` | `0x4b23...2c5e8` | Main account address (L2) |
| `PARADEX_SUBKEY_PRIVATE_KEY` | `0x0441...8cf55` | Subkey for signing (safer) |

### Optional Fields:

| Field | Default | Description |
|-------|---------|-------------|
| `PARADEX_BASE_URL_HTTP` | Auto-detected | REST API endpoint |
| `PARADEX_BASE_URL_WS` | Auto-detected | WebSocket endpoint |
| `PARADEX_RECONCILE_INTERVAL` | `300.0` | Reconciliation interval (seconds) |
| `PARADEX_TIMEOUT_SECS` | `30.0` | HTTP timeout |

---

## 🚀 QUICK START

### 1. Set Environment Variables:
```bash
source .env.testnet
```

### 2. Verify Configuration:
```bash
echo $PARADEX_L2_ADDRESS
echo $PARADEX_SUBKEY_PRIVATE_KEY
```

### 3. Test Connection:
```bash
python test_connection.py
```

### 4. Start Development:
```bash
# Your implementation here
```

---

## ⚠️ IMPORTANT REMINDERS

1. **TESTNET ONLY** - These keys are for testing
2. **NO REAL FUNDS** - Testnet tokens have no value
3. **ROTATE KEYS** - Change keys periodically
4. **USE SUBKEYS** - Safer than main account keys
5. **GITIGNORE** - Never commit `.env` files

---

**TESTNET CONFIGURATION READY**  
**SAFE FOR DEVELOPMENT AND TESTING**  
**DO NOT USE ON MAINNET**
