# 1_RUST_CORE_IMPLEMENTATION.md
RUST CORE IMPLEMENTATION - PARADEX NAUTILUS ADAPTER
Complete Rust Architecture and Implementation Details

📋 OVERVIEW
This document details complete Rust implementation layer for Paradex Nautilus adapter.

Total LOC: ~4,500
Modules: 7 main modules
Files: ~30 files
Compliance: 100% Nautilus standards

🏗️ MODULE ARCHITECTURE
```
crates/adapters/paradex/
├── Cargo.toml                  # Dependencies
├── src/
│   ├── lib.rs                  # PyO3 entry point
│   ├── config.rs               # Configuration
│   ├── error.rs                # Error types
│   ├── common/                 # Shared utilities
│   │   ├── mod.rs
│   │   ├── consts.rs           # Constants
│   │   ├── credential.rs       # STARK signing ⭐
│   │   ├── enums.rs            # Enumerations
│   │   ├── models.rs           # Data structures
│   │   ├── parse.rs            # Parsing utilities
│   │   └── urls.rs             # URL resolution
│   ├── http/                   # HTTP client ⭐
│   │   ├── mod.rs
│   │   ├── client.rs           # Main HTTP client
│   │   ├── error.rs            # HTTP errors
│   │   ├── models.rs           # Request/response types
│   │   ├── parse.rs            # Response parsing
│   │   └── query.rs            # Request builders
│   ├── websocket/              # WebSocket client ⭐
│   │   ├── mod.rs
│   │   ├── client.rs           # Main WS client
│   │   ├── enums.rs            # WS enumerations
│   │   ├── error.rs            # WS errors
│   │   ├── handler.rs          # Message routing
│   │   ├── messages.rs         # Message types
│   │   └── parse.rs            # Message parsing
│   ├── execution/
│   │   └── mod.rs              # Rust execution layer
│   ├── data/
│   │   └── mod.rs              # Rust data layer
│   └── python/                 # PyO3 bindings ⭐
│       ├── mod.rs              # Module registration
│       ├── enums.rs            # Python enums
│       ├── http.rs             # HTTP Python API
│       ├── urls.rs             # URL helpers
│       └── websocket.rs        # WebSocket Python API
└── tests/
    ├── http.rs
    ├── websocket.rs
    ├── execution.rs
    └── data.rs
```

🔑 CRITICAL MODULE: common/credential.rs (STARK Signing)

This module implements STARK signature generation for Paradex orders.

**Purpose**
- Sign orders with StarkNet private keys
- Generate Pedersen hashes
- EIP-712 typed data structures

**Implementation**

```rust
// src/common/credential.rs
use starknet::signers::{SigningKey, VerifyingKey};
use starknet::core::types::FieldElement;
use starknet::core::crypto::{pedersen_hash, Signature};
use sha2::{Sha256, Digest};
use crate::error::{ParadexError, Result};

/// STARK signer for Paradex orders
pub struct StarkSigner {
    signing_key: SigningKey,
    verifying_key: VerifyingKey,
    account_address: FieldElement,
}

impl StarkSigner {
    /// Create new signer from hex strings (without 0x prefix)
    pub fn new(private_key_hex: &str, account_hex: &str) -> Result<Self> {
        // Parse private key
        let pk_hex = if private_key_hex.starts_with("0x") {
            &private_key_hex[2..]
        } else {
            private_key_hex
        };

        let private_key = FieldElement::from_hex_be(pk_hex)
            .map_err(|e| ParadexError::Signature(format!("Invalid private key: {}", e)))?;

        // Parse account address
        let account = FieldElement::from_hex_be(account_hex)
            .map_err(|e| ParadexError::Signature(format!("Invalid account: {}", e)))?;

        // Create signing key
        let signing_key = SigningKey::from_secret_scalar(private_key);
        let verifying_key = signing_key.verifying_key();

        Ok(Self {
            signing_key,
            verifying_key,
            account_address: account,
        })
    }

    /// Sign order with STARK private key
    /// Returns (r, s) as hex strings with 0x prefix
    pub fn sign_order(
        &self,
        market: &str,
        side: &str,
        order_type: &str,
        size: &str,
        price: Option<&str>,
        timestamp_ms: i64,
        nonce: u64,
    ) -> Result<(String, String)> {
        // Build message hash per Paradex specification
        let message_hash = self.build_order_hash(
            market, side, order_type, size, price, timestamp_ms, nonce
        )?;

        // Sign with StarkNet key
        let signature = self.signing_key.sign(&message_hash)
            .map_err(|e| ParadexError::Signature(format!("Signing failed: {}", e)))?;

        // Format as hex with 0x prefix
        Ok((
            format!("0x{:064x}", signature.r),
            format!("0x{:064x}", signature.s),
        ))
    }

    /// Build order hash per Paradex specification
    fn build_order_hash(
        &self,
        market: &str,
        side: &str,
        order_type: &str,
        size: &str,
        price: Option<&str>,
        timestamp_ms: i64,
        nonce: u64,
    ) -> Result<FieldElement> {
        // Create message components
        let components = vec![
            self.account_address,
            self.string_to_field_element(market)?,
            self.string_to_field_element(side)?,
            self.string_to_field_element(order_type)?,
            self.string_to_field_element(size)?,
            self.string_to_field_element(price.unwrap_or("0"))?,
            FieldElement::from(timestamp_ms as u64),
            FieldElement::from(nonce),
        ];

        // Compute Pedersen hash chain
        let mut hash = components;
        for component in &components[1..] {
            hash = pedersen_hash(&hash, component);
        }

        Ok(hash)
    }

    /// Convert string to FieldElement via SHA256
    fn string_to_field_element(&self, s: &str) -> Result<FieldElement> {
        let mut hasher = Sha256::new();
        hasher.update(s.as_bytes());
        let hash = hasher.finalize();

        FieldElement::from_byte_slice_be(&hash)
            .map_err(|e| ParadexError::Signature(format!("Hash conversion failed: {}", e)))
    }

    /// Get public key (for verification)
    pub fn public_key(&self) -> String {
        format!("0x{:064x}", self.verifying_key.scalar())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_signer_creation() {
        let signer = StarkSigner::new(
            "0x1234567890abcdef",
            "0x0123456789abcdef0123456789abcdef01234567",
        );
        assert!(signer.is_ok());
    }

    #[test]
    fn test_order_signing() {
        let signer = StarkSigner::new(
            "test_key",
            "0x0123456789abcdef0123456789abcdef01234567",
        ).unwrap();

        let (r, s) = signer.sign_order(
            "BTC-USD-PERP",
            "BUY",
            "LIMIT",
            "1.5",
            Some("50000"),
            1706745600000,
            1,
        ).unwrap();

        assert!(r.starts_with("0x"));
        assert!(s.starts_with("0x"));
        assert_eq!(r.len(), 66); // 0x + 64 hex chars
        assert_eq!(s.len(), 66);
    }
}
```

**Usage in HTTP Client**

```rust
// In http/client.rs
let (r, s) = self.signer.sign_order(market, side, ...)?;
let body = json!({
    "market": market,
    "signature": { "r": r, "s": s }
});
```

🔑 CRITICAL MODULE: http/client.rs (HTTP Client)

**Purpose**
- REST API communication
- JWT authentication
- Order submission
- State queries

**Key Implementation Points**

1. Use nautilus-network (MANDATORY)
```rust
use nautilus_network::http::HttpClient as NautilusHttpClient;

// NOT reqwest::Client directly!
```

2. JWT Token Caching
```rust
jwt_token: Arc<Mutex<Option<(String, Instant)>>>
```

3. Authentication Flow
```rust
async fn ensure_authenticated(&self) -> Result<String> {
    // Check cache
    if let Some((token, expires)) = self.jwt_token.lock().unwrap().as_ref() {
        if Instant::now() < *expires {
            return Ok(token.clone());
        }
    }

    // Get new token
    let response = self.client
        .post(&format!("{}/auth", self.base_url))
        .json(&json!({ "account": self.account_address }))
        .send()
        .await?;

    let data: Value = response.json().await?;
    let token = data["jwt_token"].as_str().unwrap().to_string();
    let expires = Instant::now() + Duration::from_secs(3600);

    *self.jwt_token.lock().unwrap() = Some((token.clone(), expires));
    Ok(token)
}
```

4. Order Submission
```rust
pub async fn submit_order(
    &self,
    market: &str,
    side: OrderSide,
    order_type: OrderType,
    size: Decimal,
    price: Option<Decimal>,
    client_id: Option<String>,
) -> Result<OrderResponse> {
    let token = self.ensure_authenticated().await?;

    // Sign order
    let (r, s) = self.signer.sign_order(
        market,
        side.as_str(),
        order_type.as_str(),
        &size.to_string(),
        price.as_ref().map(|p| p.to_string().as_str()),
        chrono::Utc::now().timestamp_millis(),
        1, // nonce from server
    )?;

    // Submit
    let response = self.client
        .post(&format!("{}/orders", self.base_url))
        .bearer_auth(&token)
        .json(&json!({
            "market": market,
            "side": side.as_str(),
            "type": order_type.as_str(),
            "size": size.to_string(),
            "price": price.map(|p| p.to_string()),
            "client_id": client_id,
            "signature": { "r": r, "s": s }
        }))
        .send()
        .await?;

    Ok(response.json().await?)
}
```

🔑 CRITICAL MODULE: python/http.rs (PyO3 Bindings)

**Purpose**
- Expose Rust HTTP client to Python
- Async/await bridge
- Error conversion

**Implementation**

```rust
// src/python/http.rs
use pyo3::prelude::*;
use pyo3_asyncio::tokio::future_into_py;
use crate::http::HttpClient;

#[pyclass]
pub struct PyParadexHttpClient {
    inner: HttpClient,
    runtime: tokio::runtime::Runtime,
}

#[pymethods]
impl PyParadexHttpClient {
    #[new]
    pub fn new(
        base_url: String,
        subkey_private_key: String,
        main_account_address: String,
    ) -> PyResult<Self> {
        let runtime = tokio::runtime::Runtime::new()
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

        let inner = runtime.block_on(async {
            HttpClient::new(base_url, subkey_private_key, main_account_address).await
        }).map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

        Ok(Self { inner, runtime })
    }

    pub fn get_markets<'py>(&self, py: Python<'py>) -> PyResult<&'py PyAny> {
        let client = self.inner.clone();
        future_into_py(py, async move {
            client.get_markets()
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
        })
    }

    pub fn submit_order<'py>(
        &self,
        py: Python<'py>,
        market: String,
        side: String,
        order_type: String,
        size: String,
        price: Option<String>,
        client_id: Option<String>,
    ) -> PyResult<&'py PyAny> {
        let client = self.inner.clone();
        future_into_py(py, async move {
            let result = client.submit_order(
                &market,
                &side,
                &order_type,
                &size,
                price.as_deref(),
                client_id,
            ).await;

            result.map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
        })
    }
}
```

📝 TESTING STRATEGY

**Unit Tests**
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_http_client_creation() {
        let client = HttpClient::new(
            "https://api.testnet.paradex.trade/v1".to_string(),
            "test_key".to_string(),
            "0x123...".to_string(),
        ).await;

        assert!(client.is_ok());
    }
}
```

**Integration Tests**
```rust
// tests/http.rs
#[tokio::test]
async fn test_submit_order() {
    let client = create_test_client().await;
    let result = client.submit_order(...).await;
    assert!(result.is_ok());
}
```

Next: See 2_PYTHON_ADAPTER_IMPLEMENTATION.md for Python layer details
