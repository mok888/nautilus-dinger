// crates/adapters/paradex/src/config.rs

use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

/// Paradex adapter configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ParadexConfig {
    /// Environment (testnet or mainnet)
    pub environment: String,

    /// HTTP base URL
    pub http_url: String,

    /// WebSocket base URL
    pub ws_url: String,

    /// Chain ID for STARK signatures
    pub chain_id: String,

    /// Account address (derived from public key)
    pub account_address: String,

    /// L2 address (main account)
    pub l2_address: String,

    /// Subkey private key for order signing
    pub subkey_private_key: String,

    /// Optional API key for authentication (alternative to JWT)
    pub api_key: Option<String>,
}

impl ParadexConfig {
    /// Create new configuration
    pub fn new(environment: String, account_address: String, l2_address: String, subkey_private_key: String) -> Self {
        Self::new_with_api_key(environment, account_address, l2_address, subkey_private_key, None)
    }

    /// Create new configuration with API key
    pub fn new_with_api_key(
        environment: String,
        account_address: String,
        l2_address: String,
        subkey_private_key: String,
        api_key: Option<String>,
    ) -> Self {
        let (http_url, ws_url, chain_id) = match environment.as_str() {
            "testnet" => (
                "https://api.testnet.paradex.trade".to_string(),
                "wss://ws.testnet.paradex.trade/v1".to_string(),
                "0x505249564154455f534e5f504f54435f5345504f4c4941".to_string(), // PRIVATE_SN_POTC_SEPOLIA
            ),
            "mainnet" => (
                "https://api.paradex.trade".to_string(),
                "wss://ws.paradex.trade/v1".to_string(),
                "0x534e5f4d41494e".to_string(), // SN_MAIN
            ),
            _ => panic!("Invalid environment: {}", environment),
        };

        Self {
            environment,
            http_url,
            ws_url,
            chain_id,
            account_address,
            l2_address,
            subkey_private_key,
            api_key,
        }
    }
}

#[pyclass]
pub struct PyParadexConfig {
    pub config: ParadexConfig,
}

#[pymethods]
impl PyParadexConfig {
    #[new]
    fn new(
        environment: String,
        account_address: String,
        l2_address: String,
        subkey_private_key: String,
    ) -> Self {
        Self {
            config: ParadexConfig::new(environment, account_address, l2_address, subkey_private_key),
        }
    }

    fn http_url(&self) -> String {
        self.config.http_url.clone()
    }

    fn ws_url(&self) -> String {
        self.config.ws_url.clone()
    }
}
