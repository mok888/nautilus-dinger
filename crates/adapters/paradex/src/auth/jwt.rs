// crates/adapters/paradex/src/auth/jwt.rs

use crate::config::ParadexConfig;
use crate::error::Result;
use crate::signing::signer::Starker;
use reqwest::Client;
use serde::{Deserialize, Serialize};
use std::time::{SystemTime, UNIX_EPOCH};
use tracing::{debug, info};

const JWT_EXPIRY_SECONDS: u64 = 300; // 5 minutes
const JWT_REFRESH_SECONDS: u64 = 180; // Refresh after 3 minutes

#[derive(Debug, Clone, Serialize, Deserialize)]
struct JwtResponse {
    jwt_token: String,
}

/// JWT authenticator for Paradex API
pub struct JwtAuthenticator {
    config: ParadexConfig,
    starker: Starker,
    client: Client,
    current_token: Option<String>,
    token_expiry: u64,
}

impl JwtAuthenticator {
    /// Create new JWT authenticator
    pub fn new(config: ParadexConfig) -> Result<Self> {
        let starker = Starker::new(&config)?;
        let client = Client::new();

        Ok(Self {
            config,
            starker,
            client,
            current_token: None,
            token_expiry: 0,
        })
    }

    /// Get current JWT token, refreshing if needed
    pub async fn get_token(&mut self) -> Result<String> {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();

        // Check if token needs refresh
        if self.current_token.is_none() || now >= self.token_expiry - JWT_REFRESH_SECONDS {
            info!("Refreshing JWT token");
            self.refresh_token().await?;
        }

        Ok(self.current_token.clone().unwrap())
    }

    /// Force refresh JWT token
    async fn refresh_token(&mut self) -> Result<()> {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();

        let expiration = now + 1800; // 30 minutes from now

        // Create auth message hash using proper EIP-712 structure
        let message_hash = self.create_auth_message_hash(now, expiration)?;
        
        // Sign the message directly
        let ext_signature = starknet_crypto::sign(
            &self.starker.private_key,
            &message_hash,
            &starknet_types_core::felt::Felt::ONE
        ).map_err(|e| crate::error::ParadexError::Signature(format!("Sign error: {}", e)))?;

        // Make request to /v1/auth
        let url = format!("{}/v1/auth", self.config.http_url);
        
        debug!("Requesting JWT from {}", url);
        debug!("Account: {}", self.config.account_address);
        debug!("Timestamp: {}", now);
        debug!("Expiration: {}", expiration);
        debug!("Message hash: {:#x}", message_hash);
        debug!("Signature r: {}", ext_signature.r);
        debug!("Signature s: {}", ext_signature.s);
        
        // Format signature as array of decimal strings
        let sig_array = format!("[\"{}\",\"{}\"]", ext_signature.r, ext_signature.s);
        
        let response = self.client
            .post(&url)
            .header("PARADEX-STARKNET-ACCOUNT", &self.config.account_address)
            .header("PARADEX-STARKNET-SIGNATURE", &sig_array)
            .header("PARADEX-TIMESTAMP", now.to_string())
            .header("PARADEX-SIGNATURE-EXPIRATION", expiration.to_string())
            .header("Accept", "application/json")
            .send()
            .await
            .map_err(|e| crate::error::ParadexError::Http(format!("JWT request failed: {}", e)))?;

        if !response.status().is_success() {
            let status = response.status();
            let body = response.text().await.unwrap_or_default();
            return Err(crate::error::ParadexError::Http(format!(
                "JWT request failed with status {}: {}",
                status, body
            )));
        }

        let jwt_response: JwtResponse = response
            .json()
            .await
            .map_err(|e| crate::error::ParadexError::Parse(format!("Failed to parse JWT response: {}", e)))?;

        self.current_token = Some(jwt_response.jwt_token);
        self.token_expiry = now + JWT_EXPIRY_SECONDS;

        info!("JWT token refreshed successfully");
        Ok(())
    }

    /// Create authentication message hash for JWT
    fn create_auth_message_hash(&self, timestamp: u64, expiration: u64) -> Result<starknet_types_core::felt::Felt> {
        use sha3::{Digest, Keccak256};
        use starknet_crypto::poseidon_hash_many;
        use starknet_types_core::felt::Felt;

        // Message structure for JWT auth:
        // hash(PREFIX_MESSAGE, domain_separator, account, hash_struct(message))
        
        // PREFIX_MESSAGE = "StarkNet Message"
        let prefix = Felt::from_bytes_be_slice(b"StarkNet Message");
        
        // Domain separator: hash_struct(StarkNetDomain)
        let domain_type_hash = {
            let mut hasher = Keccak256::new();
            hasher.update(b"StarkNetDomain(name:felt,chainId:felt,version:felt)");
            Felt::from_bytes_be_slice(&hasher.finalize())
        };
        
        let domain_hash = poseidon_hash_many(&[
            domain_type_hash,
            Felt::from_bytes_be_slice(b"Paradex"),
            Felt::from_bytes_be_slice(self.config.chain_id.as_bytes()),
            Felt::ONE,
        ]);
        
        // Message type hash for auth
        let message_type_hash = {
            let mut hasher = Keccak256::new();
            hasher.update(b"Auth(timestamp:felt,expiration:felt)");
            Felt::from_bytes_be_slice(&hasher.finalize())
        };
        
        // Message hash
        let message_hash = poseidon_hash_many(&[
            message_type_hash,
            Felt::from(timestamp),
            Felt::from(expiration),
        ]);
        
        // Account address
        let account = Felt::from_hex(&self.config.account_address)
            .map_err(|e| crate::error::ParadexError::Signature(e.to_string()))?;
        
        // Final hash
        Ok(poseidon_hash_many(&[
            prefix,
            domain_hash,
            account,
            message_hash,
        ]))
    }

    /// Check if token is valid
    pub fn is_token_valid(&self) -> bool {
        if self.current_token.is_none() {
            return false;
        }

        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();

        now < self.token_expiry
    }
}
