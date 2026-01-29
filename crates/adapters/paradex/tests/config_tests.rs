// crates/adapters/paradex/tests/config_tests.rs

use paradex_adapter::config::ParadexConfig;

#[test]
fn test_testnet_config() {
    let config = ParadexConfig::new(
        "testnet".to_string(),
        "0x123".to_string(),
        "0x456".to_string(),
        "0x789".to_string(),
    );

    assert_eq!(config.environment, "testnet");
    assert_eq!(config.http_url, "https://api.testnet.paradex.trade");
    assert_eq!(config.ws_url, "wss://ws.testnet.paradex.trade/v1");
    assert_eq!(config.chain_id, "SN_SEPOLIA");
    assert_eq!(config.account_address, "0x123");
    assert_eq!(config.l2_address, "0x456");
    assert_eq!(config.subkey_private_key, "0x789");
}

#[test]
fn test_mainnet_config() {
    let config = ParadexConfig::new(
        "mainnet".to_string(),
        "0x123".to_string(),
        "0x456".to_string(),
        "0x789".to_string(),
    );

    assert_eq!(config.environment, "mainnet");
    assert_eq!(config.http_url, "https://api.paradex.trade");
    assert_eq!(config.ws_url, "wss://ws.paradex.trade/v1");
    assert_eq!(config.chain_id, "SN_MAIN");
}

#[test]
#[should_panic(expected = "Invalid environment")]
fn test_invalid_environment() {
    ParadexConfig::new(
        "invalid".to_string(),
        "0x123".to_string(),
        "0x456".to_string(),
        "0x789".to_string(),
    );
}
