// crates/adapters/paradex/src/signing/signer.rs

use crate::config::ParadexConfig;
use crate::error::Result;
use crate::signing::types::SignatureParams;
use starknet_crypto::{sign, poseidon_hash_many};
use starknet_types_core::felt::Felt;
use tracing::{debug, info};

/// STARK signer for Paradex
pub struct Starker {
    pub(crate) private_key: Felt,
    public_key: Felt,
    account_address: String,
    chain_id: String,
}

impl Starker {
    /// Create new STARK signer
    pub fn new(config: &ParadexConfig) -> Result<Self> {
        info!("Creating STARK signer for chain {}", config.chain_id);

        let private_key = Felt::from_hex(&config.subkey_private_key).map_err(|e| {
            crate::error::ParadexError::Signature(format!("Invalid private key: {}", e))
        })?;

        // Derive public key from private key
        let public_key = starknet_crypto::get_public_key(&private_key);
        let account_address = config.account_address.clone();

        Ok(Self {
            private_key,
            public_key,
            account_address,
            chain_id: config.chain_id.clone(),
        })
    }

    /// Sign Paradex order
    pub fn sign_order(&self, params: &SignatureParams) -> Result<starknet_crypto::Signature> {
        debug!("Signing order: {:?}", params);

        let message_hash = self.hash_typed_data(params)?;

        // Use k=1 for deterministic signing (k=0 is invalid)
        let ext_signature = sign(&self.private_key, &message_hash, &Felt::ONE)
            .map_err(|e| crate::error::ParadexError::Signature(format!("Sign error: {}", e)))?;

        let signature = starknet_crypto::Signature {
            r: ext_signature.r,
            s: ext_signature.s,
        };

        debug!(
            "Signature created: r={:?}, s={:?}",
            signature.r, signature.s
        );
        Ok(signature)
    }

    /// Sign auth message for API authentication (like paradex-py)
    pub fn sign_auth_message(&self, timestamp: u64, expiry: u64) -> Result<String> {
        use starknet_crypto::poseidon_hash_many;
        
        // Build auth message (simplified from paradex-py)
        let domain_name = Felt::from_bytes_be_slice(b"Paradex");
        let chain_id = Felt::from_hex(&self.chain_id)
            .map_err(|e| crate::error::ParadexError::Parse(format!("Invalid chain_id: {}", e)))?;
        let version = Felt::ONE;
        
        let method = Felt::from_bytes_be_slice(b"POST");
        let path = Felt::from_bytes_be_slice(b"/v1/auth");
        let body = Felt::ZERO;
        let ts = Felt::from(timestamp);
        let exp = Felt::from(expiry);
        
        // Hash components
        let message_hash = poseidon_hash_many(&[method, path, body, ts, exp]);
        let domain_hash = poseidon_hash_many(&[domain_name, chain_id, version]);
        let final_hash = poseidon_hash_many(&[domain_hash, message_hash]);
        
        // Sign
        let ext_signature = sign(&self.private_key, &final_hash, &Felt::ONE)
            .map_err(|e| crate::error::ParadexError::Signature(format!("Auth sign error: {}", e)))?;
        
        Ok(format!("[\"{}\",\"{}\"]", ext_signature.r, ext_signature.s))
    }

    /// Hash typed data according to EIP-712 for StarkNet
    fn hash_typed_data(&self, params: &SignatureParams) -> Result<Felt> {
        use sha3::{Digest, Keccak256};
        use starknet_crypto::poseidon_hash_many;

        // Compute type hash for domain
        let domain_type_hash = {
            let mut hasher = Keccak256::new();
            hasher.update(b"StarkNetDomain(name:felt,chainId:felt,version:felt)");
            Felt::from_bytes_be_slice(&hasher.finalize())
        };

        // Hash domain separator
        let domain_hash = poseidon_hash_many(&[
            domain_type_hash,
            Felt::from_bytes_be_slice(b"Paradex"),
            Felt::from_bytes_be_slice(params.chain_id.as_bytes()),
            Felt::ONE,
        ]);

        // Compute type hash for Order
        let order_type_hash = {
            let mut hasher = Keccak256::new();
            hasher.update(b"Order(maker:felt,taker:felt,base_asset:felt,quote_asset:felt,base_quantity:felt,quote_quantity:felt,order_id:felt,nonce:felt,expiration:felt,is_post_only:felt)");
            Felt::from_bytes_be_slice(&hasher.finalize())
        };

        // Hash message struct
        let order = &params.order;
        let message_hash = poseidon_hash_many(&[
            order_type_hash,
            Felt::from_hex(&order.maker)
                .map_err(|e| crate::error::ParadexError::Signature(e.to_string()))?,
            Felt::from_hex(&order.taker)
                .map_err(|e| crate::error::ParadexError::Signature(e.to_string()))?,
            Felt::from_hex(&order.base_asset)
                .map_err(|e| crate::error::ParadexError::Signature(e.to_string()))?,
            Felt::from_hex(&order.quote_asset)
                .map_err(|e| crate::error::ParadexError::Signature(e.to_string()))?,
            Felt::from_dec_str(&order.base_quantity)
                .map_err(|e| crate::error::ParadexError::Signature(e.to_string()))?,
            Felt::from_dec_str(&order.quote_quantity)
                .map_err(|e| crate::error::ParadexError::Signature(e.to_string()))?,
            Felt::from_hex(&order.order_id)
                .map_err(|e| crate::error::ParadexError::Signature(e.to_string()))?,
            Felt::from_dec_str(&order.nonce)
                .map_err(|e| crate::error::ParadexError::Signature(e.to_string()))?,
            Felt::from_dec_str(&order.expiration)
                .map_err(|e| crate::error::ParadexError::Signature(e.to_string()))?,
            Felt::from_dec_str(&order.is_post_only)
                .map_err(|e| crate::error::ParadexError::Signature(e.to_string()))?,
        ]);

        // Final EIP-712 hash: hash(domain_hash, account, message_hash)
        Ok(poseidon_hash_many(&[
            domain_hash,
            Felt::from_hex(&self.account_address)
                .map_err(|e| crate::error::ParadexError::Signature(e.to_string()))?,
            message_hash,
        ]))
    }

    /// Get StarkNet account address
    pub fn get_account_address(&self) -> String {
        self.account_address.clone()
    }

    /// Get public key as hex string
    pub fn get_public_key(&self) -> String {
        format!("{:#x}", self.public_key)
    }
}
