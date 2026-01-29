// crates/adapters/paradex/src/signing/types.rs

use serde::{Deserialize, Serialize};
use serde_json::Value;

/// EIP-712 TypedData for Paradex STARK signatures
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TypedData {
    pub types: Vec<String>,
    pub domain: String,
    pub primary_type: String,
    pub message: Value,
}

/// STARK signature parameters
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SignatureParams {
    pub order: OrderSignatureParams,
    pub verifying_contract_address: String,
    pub chain_id: String,
}

/// Order signature parameters
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OrderSignatureParams {
    pub maker: String,
    pub taker: String,
    pub base_asset: String,
    pub quote_asset: String,
    pub base_quantity: String,
    pub quote_quantity: String,
    pub order_id: String,
    pub nonce: String,
    pub expiration: String,
    pub is_post_only: String,
}
