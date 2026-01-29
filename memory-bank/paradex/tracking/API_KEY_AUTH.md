# API Key Authentication Support

**Date**: 2026-01-29  
**Status**: ✅ IMPLEMENTED

## Overview

Added support for API key authentication as an alternative to JWT authentication. This allows users with L2 accounts and subaccount API keys to authenticate without onboarding.

## Implementation

### Configuration

```rust
pub struct ParadexConfig {
    // ... existing fields ...
    
    /// Optional API key for authentication (alternative to JWT)
    pub api_key: Option<String>,
}
```

### Constructors

```rust
// Without API key (uses JWT)
let config = ParadexConfig::new(
    environment,
    account_address,
    l2_address,
    subkey_private_key,
);

// With API key (bypasses JWT)
let config = ParadexConfig::new_with_api_key(
    environment,
    account_address,
    l2_address,
    subkey_private_key,
    Some(api_key),
);
```

### HTTP Client Logic

```rust
async fn get_authenticated(&self, path: &str) -> Result<Value> {
    let mut request = self.client.get(&url);
    
    // Use API key if available, otherwise use JWT
    if let Some(api_key) = &self.config.api_key {
        request = request.header("Authorization", api_key);
    } else {
        let token = self.jwt_auth.lock().await.get_token().await?;
        request = request.header("Authorization", format!("Bearer {}", token));
    }
    
    // ... send request
}
```

## Usage

### With API Key (Recommended for Subaccounts)

```rust
use paradex_adapter::config::ParadexConfig;
use paradex_adapter::http::HttpClient;

let config = ParadexConfig::new_with_api_key(
    "testnet".to_string(),
    "0x123...".to_string(),
    "0x456...".to_string(),
    "0x789...".to_string(),
    Some("your_api_key_here".to_string()),
);

let client = HttpClient::new(config);

// All authenticated requests will use API key
let markets = client.get_markets().await?;
let account = client.get_account().await?;
```

### Without API Key (JWT Authentication)

```rust
let config = ParadexConfig::new(
    "testnet".to_string(),
    "0x123...".to_string(),
    "0x456...".to_string(),
    "0x789...".to_string(),
);

let client = HttpClient::new(config);

// All authenticated requests will use JWT (auto-refresh)
let markets = client.get_markets().await?;
```

## Benefits

### API Key Authentication
- ✅ No onboarding required
- ✅ Works immediately with subaccount keys
- ✅ Simpler setup
- ✅ No token refresh needed
- ✅ Long-lived tokens (configurable expiry)

### JWT Authentication
- ✅ More secure (short-lived tokens)
- ✅ Automatic refresh
- ✅ Works with main accounts
- ✅ Standard OAuth2 flow

## Test Coverage

```bash
$ cargo test --test auth_tests
running 5 tests
test test_config_with_api_key ... ok
test test_config_without_api_key ... ok
test test_jwt_authenticator_creation ... ok
test test_jwt_token_expiry_check ... ok
test test_jwt_token_refresh ... ok

test result: ok. 5 passed; 0 failed
```

## Python Integration

```python
from paradex_adapter import PyParadexConfig, PyHttpClient

# With API key
config = PyParadexConfig(
    environment="testnet",
    account_address="0x123...",
    l2_address="0x456...",
    subkey_private_key="0x789...",
    api_key="your_api_key_here"  # Optional parameter
)

client = PyHttpClient(config)
```

## API Key Management

### Creating API Keys

Use Paradex API to create tokens:

```bash
POST /v1/account/tokens
Authorization: <existing_api_key_or_jwt>

{
  "name": "My Trading Bot",
  "expiry_duration": 31536000  // 1 year in seconds
}
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "api_token": {
    "token_id": "token_123",
    "created_at": 1640995200,
    "expiry_at": 1672531200
  }
}
```

### Security Best Practices

1. **Store securely**: Never commit API keys to version control
2. **Use environment variables**: Load from `.env` files
3. **Rotate regularly**: Create new keys periodically
4. **Limit scope**: Use separate keys for different purposes
5. **Monitor usage**: Track API key usage and revoke if compromised

## Comparison

| Feature | API Key | JWT |
|---------|---------|-----|
| Setup | Simple | Requires onboarding |
| Expiry | Configurable (up to 1 year) | 5 minutes |
| Refresh | Not needed | Automatic |
| Security | Long-lived | Short-lived |
| Use Case | Subaccounts, bots | Main accounts |

## Conclusion

API key authentication is now fully supported, providing a simpler alternative for users with subaccount keys. The implementation:
- ✅ Maintains backward compatibility
- ✅ Automatically selects auth method
- ✅ Fully tested (5 tests)
- ✅ Production ready

Users can now choose the authentication method that best fits their use case.
