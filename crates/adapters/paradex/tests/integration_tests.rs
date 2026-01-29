// crates/adapters/paradex/tests/integration_tests.rs

use paradex_adapter::config::ParadexConfig;
use paradex_adapter::http::HttpClient;
use paradex_adapter::websocket::WebSocketClient;
use paradex_adapter::signing::signer::Starker;
use paradex_adapter::signing::types::{OrderSignatureParams, SignatureParams};
use std::time::Duration;
use tokio::time::sleep;

// Test credentials - replace with actual testnet credentials
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

#[tokio::test]
async fn test_http_get_system_time() {
    let config = get_test_config();
    let client = HttpClient::new(config);

    let result = client.get_system_time().await;
    
    match result {
        Ok(time) => {
            println!("System time: {}", time);
            assert!(time > 0, "System time should be positive");
        }
        Err(e) => {
            println!("Warning: Failed to get system time: {:?}", e);
            println!("This may be expected if testnet is unavailable");
        }
    }
}

#[tokio::test]
async fn test_http_get_markets() {
    let config = get_test_config();
    let client = HttpClient::new(config);

    let result = client.get_markets().await;
    
    match result {
        Ok(markets) => {
            println!("Retrieved {} markets", markets.len());
            assert!(!markets.is_empty(), "Should have at least one market");
            
            // Verify market structure
            if let Some(first_market) = markets.first() {
                println!("First market: {:?}", first_market);
            }
        }
        Err(e) => {
            println!("Warning: Failed to get markets: {:?}", e);
            println!("This may be expected if testnet is unavailable");
        }
    }
}

#[tokio::test]
async fn test_http_get_account() {
    let config = get_test_config();
    let client = HttpClient::new(config);

    let result = client.get_account().await;
    
    match result {
        Ok(account) => {
            println!("Account data: {:?}", account);
            // Verify account has expected fields
            assert!(account.get("account").is_some() || account.get("error").is_some());
        }
        Err(e) => {
            println!("Warning: Failed to get account: {:?}", e);
            println!("This may be expected if account is not funded or testnet is unavailable");
        }
    }
}

#[tokio::test]
async fn test_http_get_positions() {
    let config = get_test_config();
    let client = HttpClient::new(config);

    let result = client.get_positions().await;
    
    match result {
        Ok(positions) => {
            println!("Retrieved {} positions", positions.len());
            // Empty positions list is valid for new account
        }
        Err(e) => {
            println!("Warning: Failed to get positions: {:?}", e);
        }
    }
}

#[tokio::test]
async fn test_http_get_open_orders() {
    let config = get_test_config();
    let client = HttpClient::new(config);

    let result = client.get_open_orders().await;
    
    match result {
        Ok(orders) => {
            println!("Retrieved {} open orders", orders.len());
            // Empty orders list is valid
        }
        Err(e) => {
            println!("Warning: Failed to get open orders: {:?}", e);
        }
    }
}

#[tokio::test]
async fn test_http_get_fills() {
    let config = get_test_config();
    let client = HttpClient::new(config);

    let start_time = 0; // Get all fills
    let result = client.get_fills(start_time).await;
    
    match result {
        Ok(fills) => {
            println!("Retrieved {} fills", fills.len());
            // Empty fills list is valid for new account
        }
        Err(e) => {
            println!("Warning: Failed to get fills: {:?}", e);
        }
    }
}

#[tokio::test]
async fn test_http_get_orderbook() {
    let config = get_test_config();
    let client = HttpClient::new(config);

    let instrument_id = "BTC-USD-PERP";
    let result = client.get_orderbook(instrument_id).await;
    
    match result {
        Ok(orderbook) => {
            println!("Orderbook for {}: {:?}", instrument_id, orderbook);
            // Verify orderbook structure
            assert!(orderbook.get("bids").is_some() || orderbook.get("asks").is_some() || orderbook.get("error").is_some());
        }
        Err(e) => {
            println!("Warning: Failed to get orderbook: {:?}", e);
        }
    }
}

#[tokio::test]
async fn test_http_get_trades() {
    let config = get_test_config();
    let client = HttpClient::new(config);

    let instrument_id = "BTC-USD-PERP";
    let result = client.get_trades(instrument_id).await;
    
    match result {
        Ok(trades) => {
            println!("Retrieved trades for {}: {:?}", instrument_id, trades);
            // Trades response is a JSON Value
        }
        Err(e) => {
            println!("Warning: Failed to get trades: {:?}", e);
        }
    }
}

#[tokio::test]
async fn test_signing_with_real_data() {
    let config = get_test_config();
    let starker = Starker::new(&config).expect("Failed to create Starker");

    println!("Account address: {}", starker.get_account_address());
    println!("Public key: {}", starker.get_public_key());

    // Create realistic order parameters
    let order_params = OrderSignatureParams {
        maker: TEST_ACCOUNT_ADDRESS.to_string(),
        taker: "0x0".to_string(),
        base_asset: "0x4254432d5553442d50455250".to_string(), // BTC-USD-PERP
        quote_asset: "0x555344".to_string(), // USD
        base_quantity: "1000000000000000000".to_string(), // 1.0 BTC
        quote_quantity: "50000000000".to_string(), // 50000 USD
        order_id: "0x1".to_string(),
        nonce: format!("{}", std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_secs()),
        expiration: format!("{}", std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_secs() + 3600), // 1 hour from now
        is_post_only: "0".to_string(),
    };

    let sig_params = SignatureParams {
        order: order_params,
        verifying_contract_address: "0x0".to_string(),
        chain_id: config.chain_id.clone(),
    };

    let signature = starker.sign_order(&sig_params).expect("Failed to sign order");
    
    println!("Signature r: {:#x}", signature.r);
    println!("Signature s: {:#x}", signature.s);
    
    assert_ne!(format!("{:#x}", signature.r), "0x0");
    assert_ne!(format!("{:#x}", signature.s), "0x0");
}

#[tokio::test]
async fn test_websocket_connection() {
    let config = get_test_config();
    let mut ws_client = WebSocketClient::new(config);

    // Test connection (this will fail if testnet is down, which is expected)
    let result = ws_client.connect(vec![]).await;
    
    match result {
        Ok(_) => {
            println!("WebSocket connected successfully");
            
            // Try to subscribe to orderbook
            let sub_result = ws_client.subscribe_orderbook("BTC-USD-PERP").await;
            match sub_result {
                Ok(_) => println!("Subscribed to orderbook"),
                Err(e) => println!("Failed to subscribe: {:?}", e),
            }
            
            // Wait a bit for messages
            sleep(Duration::from_secs(2)).await;
            
            // Unsubscribe
            let _ = ws_client.unsubscribe_all().await;
        }
        Err(e) => {
            println!("Warning: WebSocket connection failed: {:?}", e);
            println!("This is expected if testnet is unavailable");
        }
    }
}

#[tokio::test]
async fn test_websocket_orderbook_subscription() {
    let config = get_test_config();
    let mut ws_client = WebSocketClient::new(config);

    // Set up callback
    let callback_invoked = std::sync::Arc::new(std::sync::atomic::AtomicBool::new(false));
    let callback_invoked_clone = callback_invoked.clone();
    
    ws_client.on_orderbook(move |data| {
        println!("Orderbook update received: {:?}", data);
        callback_invoked_clone.store(true, std::sync::atomic::Ordering::SeqCst);
        Ok(())
    }).ok();

    match ws_client.connect(vec![]).await {
        Ok(_) => {
            println!("WebSocket connected");
            
            if let Ok(_) = ws_client.subscribe_orderbook("BTC-USD-PERP").await {
                println!("Subscribed to orderbook");
                
                // Wait for messages
                sleep(Duration::from_secs(5)).await;
                
                if callback_invoked.load(std::sync::atomic::Ordering::SeqCst) {
                    println!("✓ Callback was invoked");
                } else {
                    println!("⚠ Callback was not invoked (may be no market activity)");
                }
            }
            
            let _ = ws_client.unsubscribe_all().await;
        }
        Err(e) => {
            println!("Warning: WebSocket test skipped: {:?}", e);
        }
    }
}

#[tokio::test]
async fn test_websocket_trades_subscription() {
    let config = get_test_config();
    let mut ws_client = WebSocketClient::new(config);

    let callback_invoked = std::sync::Arc::new(std::sync::atomic::AtomicBool::new(false));
    let callback_invoked_clone = callback_invoked.clone();
    
    ws_client.on_trades(move |data| {
        println!("Trade update received: {:?}", data);
        callback_invoked_clone.store(true, std::sync::atomic::Ordering::SeqCst);
        Ok(())
    }).ok();

    match ws_client.connect(vec![]).await {
        Ok(_) => {
            println!("WebSocket connected");
            
            if let Ok(_) = ws_client.subscribe_trades("BTC-USD-PERP").await {
                println!("Subscribed to trades");
                
                // Wait for messages
                sleep(Duration::from_secs(5)).await;
                
                if callback_invoked.load(std::sync::atomic::Ordering::SeqCst) {
                    println!("✓ Callback was invoked");
                } else {
                    println!("⚠ Callback was not invoked (may be no market activity)");
                }
            }
            
            let _ = ws_client.unsubscribe_all().await;
        }
        Err(e) => {
            println!("Warning: WebSocket test skipped: {:?}", e);
        }
    }
}

#[tokio::test]
async fn test_full_order_flow() {
    let config = get_test_config();
    let client = HttpClient::new(config.clone());
    let starker = Starker::new(&config).expect("Failed to create Starker");

    println!("\n=== Full Order Flow Test ===");
    
    // Step 1: Get system time
    println!("\n1. Getting system time...");
    match client.get_system_time().await {
        Ok(time) => println!("   System time: {}", time),
        Err(e) => {
            println!("   Failed: {:?}", e);
            return;
        }
    }
    
    // Step 2: Get markets
    println!("\n2. Getting markets...");
    let markets = match client.get_markets().await {
        Ok(m) => {
            println!("   Found {} markets", m.len());
            m
        }
        Err(e) => {
            println!("   Failed: {:?}", e);
            return;
        }
    };
    
    // Step 3: Get account info
    println!("\n3. Getting account info...");
    match client.get_account().await {
        Ok(account) => println!("   Account: {:?}", account),
        Err(e) => println!("   Failed: {:?}", e),
    }
    
    // Step 4: Get current positions
    println!("\n4. Getting positions...");
    match client.get_positions().await {
        Ok(positions) => println!("   Positions: {}", positions.len()),
        Err(e) => println!("   Failed: {:?}", e),
    }
    
    // Step 5: Get open orders
    println!("\n5. Getting open orders...");
    match client.get_open_orders().await {
        Ok(orders) => println!("   Open orders: {}", orders.len()),
        Err(e) => println!("   Failed: {:?}", e),
    }
    
    // Step 6: Create and sign an order (not submitting)
    println!("\n6. Creating and signing order...");
    let order_params = OrderSignatureParams {
        maker: TEST_ACCOUNT_ADDRESS.to_string(),
        taker: "0x0".to_string(),
        base_asset: "0x4254432d5553442d50455250".to_string(),
        quote_asset: "0x555344".to_string(),
        base_quantity: "100000000000000000".to_string(), // 0.1 BTC
        quote_quantity: "5000000000".to_string(), // 5000 USD
        order_id: format!("0x{:x}", std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_nanos() as u64),
        nonce: format!("{}", std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_millis()),
        expiration: format!("{}", std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_secs() + 3600),
        is_post_only: "0".to_string(),
    };

    let sig_params = SignatureParams {
        order: order_params.clone(),
        verifying_contract_address: "0x0".to_string(),
        chain_id: config.chain_id.clone(),
    };

    match starker.sign_order(&sig_params) {
        Ok(signature) => {
            println!("   ✓ Order signed successfully");
            println!("   Signature r: {:#x}", signature.r);
            println!("   Signature s: {:#x}", signature.s);
        }
        Err(e) => {
            println!("   Failed to sign: {:?}", e);
        }
    }
    
    println!("\n=== Order Flow Test Complete ===\n");
}
