# 3_IMPLEMENTATION_ROADMAP.md
PARADEX NAUTILUS ADAPTER - COMPLETE IMPLEMENTATION ROADMAP
Step-by-Step Guide from Zero to Production

📊 OVERVIEW
This roadmap takes you from the core files you have to a complete, production-ready Paradex adapter.

Estimated Time: 8-12 hours (experienced developer)
Current Status: Core files ready (~3,500 LOC)
To Implement: Additional Rust modules (~4,000 LOC)

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

## PHASE 1: PROJECT SETUP (30 minutes)

### Step 1.1: Verify Prerequisites

```bash
# Check Rust
rustc --version  # Should be 1.75+

# Check Python
python --version  # Should be 3.10+

# Check maturin
maturin --version  # If not installed: pip install maturin

# Check Nautilus
cd nautilus_trader
make install  # This builds nautilus-core, nautilus-model, etc.
```

### Step 1.2: Create Directory Structure

```bash
cd nautilus_trader

# Python adapter
mkdir -p nautilus_trader/adapters/paradex

# Rust adapter
mkdir -p crates/adapters/paradex/src/{common,http,websocket,execution,data,python}
mkdir -p crates/adapters/paradex/tests
mkdir -p crates/adapters/paradex/test_data
```

### Step 1.3: Place Core Files

```bash
# Copy Python files
cp __init__.py config.py constants.py providers.py execution.py data.py factories.py \
   nautilus_trader/adapters/paradex/

# Copy Rust files
cp Cargo.toml crates/adapters/paradex/
cp lib.rs config.rs error.rs crates/adapters/paradex/src/
```

### Step 1.4: Adjust Cargo.toml Paths

Edit crates/adapters/paradex/Cargo.toml:

```text
[dependencies]
# Adjust these paths to match your Nautilus installation
nautilus-core = { path = "../../../nautilus_core/core" }
nautilus-model = { path = "../../../nautilus_core/model" }
nautilus-network = { path = "../../../nautilus_core/network" }
# ... etc
```

---

## PHASE 2: IMPLEMENT RUST COMMON MODULE (1 hour)

### Step 2.1: Create common/mod.rs

```bash
cd crates/adapters/paradex/src/common
touch mod.rs consts.rs credential.rs enums.rs models.rs parse.rs urls.rs
```

### Step 2.2: Implement consts.rs

```rust
// src/common/consts.rs
pub const VENUE: &str = "PARADEX";
pub const TESTNET_REST_URL: &str = "https://api.testnet.paradex.trade/v1";
pub const TESTNET_WS_URL: &str = "wss://ws.testnet.paradex.trade/v1";
pub const MAINNET_REST_URL: &str = "https://api.prod.paradex.trade/v1";
pub const MAINNET_WS_URL: &str = "wss://ws.prod.paradex.trade/v1";
```

### Step 2.3: Implement credential.rs (CRITICAL - STARK Signing)

```rust
// src/common/credential.rs
use starknet::signers::SigningKey;
use starknet::core::types::FieldElement;
use sha2::{Sha256, Digest};
use crate::error::Result;

pub struct StarkSigner {
    signing_key: SigningKey,
    account_address: FieldElement,
}

impl StarkSigner {
    pub fn new(private_key_hex: &str, account_hex: &str) -> Result<Self> {
        let private_key = FieldElement::from_hex_be(private_key_hex)
            .map_err(|e| crate::error::ParadexError::Signature(e.to_string()))?;
        let account = FieldElement::from_hex_be(account_hex)
            .map_err(|e| crate::error::ParadexError::Signature(e.to_string()))?;

        Ok(Self {
            signing_key: SigningKey::from_secret_scalar(private_key),
            account_address: account,
        })
    }

    pub fn sign_order(
        &self,
        market: &str,
        side: &str,
        order_type: &str,
        size: &str,
        price: Option<&str>,
        timestamp: i64,
        nonce: u64,
    ) -> Result<(String, String)> {
        // Build message hash (Paradex-specific format)
        let mut hasher = Sha256::new();
        hasher.update(self.account_address.to_bytes_be());
        hasher.update(market.as_bytes());
        hasher.update(side.as_bytes());
        hasher.update(order_type.as_bytes());
        hasher.update(size.as_bytes());
        if let Some(p) = price {
            hasher.update(p.as_bytes());
        }
        hasher.update(timestamp.to_le_bytes());
        hasher.update(nonce.to_le_bytes());

        let hash = hasher.finalize();
        let message = FieldElement::from_byte_slice_be(&hash)
            .map_err(|e| crate::error::ParadexError::Signature(e.to_string()))?;

        // Sign with StarkNet key
        let signature = self.signing_key.sign(&message)
            .map_err(|e| crate::error::ParadexError::Signature(e.to_string()))?;

        Ok((format!("{:#x}", signature.r), format!("{:#x}", signature.s)))
    }
}
```

### Step 2.4: Implement remaining common files

- enums.rs: Shared enumerations
- models.rs: Shared data structures
- parse.rs: Parsing utilities
- urls.rs: URL resolution helpers

### Step 2.5: Verify Common Module

```bash
cargo check --lib
```

---

## PHASE 3: IMPLEMENT RUST HTTP MODULE (2-3 hours)

### Step 3.1: Create http/mod.rs

```rust
// src/http/mod.rs
pub mod client;
pub mod error;
pub mod models;
pub mod parse;
pub mod query;

pub use client::HttpClient;
```

### Step 3.2: Implement http/client.rs (CRITICAL)

```rust
// src/http/client.rs
use nautilus_network::http::HttpClient as NautilusHttpClient;
use crate::common::credential::StarkSigner;
use crate::error::Result;

pub struct ParadexHttpClient {
    client: NautilusHttpClient,
    base_url: String,
    signer: StarkSigner,
    jwt_token: parking_lot::Mutex<Option<String>>,
}

impl ParadexHttpClient {
    pub async fn new(
        base_url: String,
        subkey_private_key: String,
        account_address: String,
    ) -> Result<Self> {
        let signer = StarkSigner::new(&subkey_private_key, &account_address)?;

        Ok(Self {
            client: NautilusHttpClient::default(),
            base_url,
            signer,
            jwt_token: parking_lot::Mutex::new(None),
        })
    }

    pub async fn get_markets(&self) -> Result<Vec<serde_json::Value>> {
        let url = format!("{}/markets", self.base_url);
        let response = self.client.get(&url).send().await?;
        let data: serde_json::Value = response.json().await?;
        Ok(data["results"].as_array().unwrap().clone())
    }

    pub async fn submit_order(
        &self,
        market: &str,
        side: &str,
        order_type: &str,
        size: &str,
        price: Option<&str>,
        client_id: Option<&str>,
    ) -> Result<serde_json::Value> {
        // Get JWT token
        let token = self.ensure_authenticated().await?;

        // Sign order with STARK
        let (r, s) = self.signer.sign_order(
            market, side, order_type, size, price,
            chrono::Utc::now().timestamp(),
            1, // nonce
        )?;

        // Submit order
        let url = format!("{}/orders", self.base_url);
        let body = serde_json::json!({
            "market": market,
            "side": side,
            "type": order_type,
            "size": size,
            "price": price,
            "client_id": client_id,
            "signature": { "r": r, "s": s }
        });

        let response = self.client
            .post(&url)
            .bearer_auth(&token)
            .json(&body)
            .send()
            .await?;

        Ok(response.json().await?)
    }

    async fn ensure_authenticated(&self) -> Result<String> {
        // Check if we have a valid token
        if let Some(token) = self.jwt_token.lock().as_ref() {
            return Ok(token.clone());
        }

        // Get new token
        let url = format!("{}/auth", self.base_url);
        let response = self.client.post(&url).send().await?;
        let data: serde_json::Value = response.json().await?;
        let token = data["jwt_token"].as_str().unwrap().to_string();

        *self.jwt_token.lock() = Some(token.clone());
        Ok(token)
    }
}
```

---

## PHASE 4: IMPLEMENT RUST WEBSOCKET MODULE (2 hours)

Similar structure to HTTP module with:
- Connection management
- Subscription handling
- Message parsing
- Auto-reconnection

---

## PHASE 5: IMPLEMENT PYO3 BINDINGS (1-2 hours)

### Step 5.1: Create python/http.rs

```rust
// src/python/http.rs
use pyo3::prelude::*;
use crate::http::ParadexHttpClient;

#[pyclass]
pub struct PyParadexHttpClient {
    inner: ParadexHttpClient,
}

#[pymethods]
impl PyParadexHttpClient {
    #[new]
    pub fn new(
        base_url: String,
        subkey_private_key: String,
        account_address: String,
    ) -> PyResult<Self> {
        let inner = ParadexHttpClient::new(base_url, subkey_private_key, account_address)
            .await
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

        Ok(Self { inner })
    }

    pub fn get_markets<'py>(&self, py: Python<'py>) -> PyResult<&'py PyAny> {
        let client = self.inner.clone();
        pyo3_asyncio::tokio::future_into_py(py, async move {
            client.get_markets()
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
        })
    }
}
```

---

## PHASE 6: BUILD AND TEST (1-2 hours)

### Step 6.1: Build Rust

```bash
cd crates/adapters/paradex
maturin develop
```

### Step 6.2: Test Python Import

```python
from paradex_adapter import PyParadexHttpClient
client = PyParadexHttpClient(
    "https://api.testnet.paradex.trade/v1",
    "YOUR_SUBKEY",
    "YOUR_ACCOUNT"
)
print("✅ Import successful")
```

---

## PHASE 7: PRODUCTION DEPLOYMENT (1 hour)

### Step 7.1: Build Release

```bash
maturin build --release
pip install target/wheels/paradex_adapter-*.whl
```

---

## ✅ COMPLETION CHECKLIST

- [ ] Phase 1: Project setup complete
- [ ] Phase 2: Common module implemented
- [ ] Phase 3: HTTP module implemented
- [ ] Phase 4: WebSocket module implemented
- [ ] Phase 5: PyO3 bindings implemented
- [ ] Phase 6: Tests passing
- [ ] Phase 7: Production deployed

Next: Follow each phase step-by-step for complete implementation
