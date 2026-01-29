// crates/adapters/paradex/tests/signing_tests.rs

use paradex_adapter::signing::signer::Starker;
use paradex_adapter::signing::types::{OrderSignatureParams, SignatureParams};
use paradex_adapter::config::ParadexConfig;

#[test]
fn test_starker_creation() {
    let config = ParadexConfig::new(
        "testnet".to_string(),
        "0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8".to_string(),
        "0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8".to_string(),
        "0x0441c1622edc5a77891cf97cd76c4ff097211f3df4493425fb9519e06ff8cf55".to_string(),
    );

    let starker = Starker::new(&config).expect("Failed to create Starker");
    
    assert!(!starker.get_account_address().is_empty());
    assert!(!starker.get_public_key().is_empty());
    assert!(starker.get_public_key().starts_with("0x"));
}

#[test]
fn test_order_signing() {
    let config = ParadexConfig::new(
        "testnet".to_string(),
        "0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8".to_string(),
        "0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8".to_string(),
        "0x0441c1622edc5a77891cf97cd76c4ff097211f3df4493425fb9519e06ff8cf55".to_string(),
    );

    let starker = Starker::new(&config).expect("Failed to create Starker");
    
    let order_params = OrderSignatureParams {
        maker: "0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8".to_string(),
        taker: "0x0".to_string(),
        base_asset: "0x4254432d5553442d50455250".to_string(),
        quote_asset: "0x555344".to_string(),
        base_quantity: "1000000000000000000".to_string(),
        quote_quantity: "50000000000".to_string(),
        order_id: "0x1".to_string(),
        nonce: "1".to_string(),
        expiration: "9999999999".to_string(),
        is_post_only: "0".to_string(),
    };

    let sig_params = SignatureParams {
        order: order_params,
        verifying_contract_address: "0x0".to_string(),
        chain_id: "SN_SEPOLIA".to_string(),
    };

    let signature = starker.sign_order(&sig_params).expect("Failed to sign order");
    
    // Signature should have non-zero r and s values
    assert_ne!(format!("{:#x}", signature.r), "0x0");
    assert_ne!(format!("{:#x}", signature.s), "0x0");
}

#[test]
fn test_deterministic_signing() {
    let config = ParadexConfig::new(
        "testnet".to_string(),
        "0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8".to_string(),
        "0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8".to_string(),
        "0x0441c1622edc5a77891cf97cd76c4ff097211f3df4493425fb9519e06ff8cf55".to_string(),
    );

    let starker = Starker::new(&config).expect("Failed to create Starker");
    
    let order_params = OrderSignatureParams {
        maker: "0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8".to_string(),
        taker: "0x0".to_string(),
        base_asset: "0x4254432d5553442d50455250".to_string(),
        quote_asset: "0x555344".to_string(),
        base_quantity: "1000000000000000000".to_string(),
        quote_quantity: "50000000".to_string(),
        order_id: "0x1".to_string(),
        nonce: "1".to_string(),
        expiration: "9999999999".to_string(),
        is_post_only: "0".to_string(),
    };

    let sig_params = SignatureParams {
        order: order_params.clone(),
        verifying_contract_address: "0x0".to_string(),
        chain_id: "SN_SEPOLIA".to_string(),
    };

    let sig1 = starker.sign_order(&sig_params).expect("Failed to sign order 1");
    let sig2 = starker.sign_order(&sig_params).expect("Failed to sign order 2");
    
    // Same input should produce same signature (deterministic)
    assert_eq!(format!("{:#x}", sig1.r), format!("{:#x}", sig2.r));
    assert_eq!(format!("{:#x}", sig1.s), format!("{:#x}", sig2.s));
}
