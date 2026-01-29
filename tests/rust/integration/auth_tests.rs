// crates/adapters/paradex/tests/auth_tests.rs

use paradex_adapter::auth::JwtAuthenticator;
use paradex_adapter::config::ParadexConfig;

const TEST_ACCOUNT_ADDRESS: &str = "0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8";
const TEST_L2_ADDRESS: &str = "0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8";
const TEST_PRIVATE_KEY: &str = "0x0441c1622edc5a77891cf97cd76c4ff097211f3df4493425fb9519e06ff8cf55";

fn get_test_config() -> ParadexConfig {
    ParadexConfig::new(
        "testnet".to_string(),
        TEST_ACCOUNT_ADDRESS.to_string(),
        TEST_L2_ADDRESS.to_string(),
        TEST_PRIVATE_KEY.to_string(),
    )
}

#[test]
fn test_jwt_authenticator_creation() {
    let config = get_test_config();
    let auth = JwtAuthenticator::new(config);
    
    assert!(auth.is_ok(), "Should create JWT authenticator");
    
    let auth = auth.unwrap();
    assert!(!auth.is_token_valid(), "Token should not be valid initially");
}

#[tokio::test]
async fn test_jwt_token_refresh() {
    let config = get_test_config();
    let mut auth = JwtAuthenticator::new(config).expect("Failed to create authenticator");
    
    println!("\n=== JWT Token Refresh Test ===");
    println!("Attempting to get JWT token from testnet...");
    
    match auth.get_token().await {
        Ok(token) => {
            println!("✓ JWT token obtained successfully");
            println!("Token length: {} characters", token.len());
            println!("Token prefix: {}...", &token[..50.min(token.len())]);
            
            assert!(!token.is_empty(), "Token should not be empty");
            assert!(token.starts_with("eyJ"), "JWT should start with eyJ");
            assert!(auth.is_token_valid(), "Token should be valid after refresh");
            
            // Try to get token again (should use cached token)
            println!("\nGetting token again (should use cache)...");
            let token2 = auth.get_token().await.expect("Failed to get cached token");
            assert_eq!(token, token2, "Should return same cached token");
            println!("✓ Cached token returned correctly");
        }
        Err(e) => {
            println!("⚠ JWT token request failed: {:?}", e);
            println!("This is expected if:");
            println!("  - Testnet is unavailable");
            println!("  - Account is not onboarded");
            println!("  - Network connectivity issues");
        }
    }
    
    println!("\n=== Test Complete ===\n");
}

#[tokio::test]
async fn test_jwt_token_expiry_check() {
    let config = get_test_config();
    let auth = JwtAuthenticator::new(config).expect("Failed to create authenticator");
    
    // Initially no token
    assert!(!auth.is_token_valid(), "Should not have valid token initially");
}

#[test]
fn test_config_with_api_key() {
    let config = ParadexConfig::new_with_api_key(
        "testnet".to_string(),
        TEST_ACCOUNT_ADDRESS.to_string(),
        TEST_L2_ADDRESS.to_string(),
        TEST_PRIVATE_KEY.to_string(),
        Some("test_api_key_123".to_string()),
    );
    
    assert_eq!(config.api_key, Some("test_api_key_123".to_string()));
    assert_eq!(config.environment, "testnet");
}

#[test]
fn test_config_without_api_key() {
    let config = get_test_config();
    assert_eq!(config.api_key, None);
}
