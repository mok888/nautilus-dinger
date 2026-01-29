// crates/adapters/paradex/src/http/client.rs

use crate::auth::JwtAuthenticator;
use crate::common::{Fill, Market, Order, Position};
use crate::concurrency::RateLimiter;
use crate::config::ParadexConfig;
use crate::error::Result;
use crate::python_wrapper::ParadexPyWrapper;

use reqwest::Client;
use serde_json::Value;
use std::sync::Arc;
use tokio::sync::Mutex;
use tracing::{debug, info};

/// HTTP client for Paradex API
#[derive(Clone)]
pub struct HttpClient {
    config: ParadexConfig,
    client: Client,
    jwt_auth: Arc<Mutex<Option<JwtAuthenticator>>>,
    py_wrapper: Arc<ParadexPyWrapper>,
    rate_limiter: Arc<RateLimiter>,
}

impl HttpClient {
    /// Create new HTTP client using paradex-py SDK
    pub fn new(config: ParadexConfig) -> Self {
        info!("Creating HTTP client for {} (using paradex-py)", config.environment);
        
        let py_wrapper = ParadexPyWrapper::new(&config)
            .expect("Failed to initialize paradex-py wrapper");
        
        Self {
            config,
            client: Client::new(),
            jwt_auth: Arc::new(Mutex::new(None)),
            py_wrapper: Arc::new(py_wrapper),
            rate_limiter: Arc::new(RateLimiter::new(10)), // 10 requests per second
        }
    }

    /// Submit order via paradex-py (JSON version)
    pub async fn submit_order_json(&self, order: Value) -> Result<Value> {
        debug!("Submitting order: {:?}", order);
        self.py_wrapper.submit_order(order)
    }

    /// Make authenticated GET request using paradex-py
    pub async fn get_authenticated(&self, path: &str) -> Result<Value> {
        // Rate limit
        let _permit = self.rate_limiter.acquire().await;
        
        debug!("GET {} (via paradex-py)", path);
        
        // Route to appropriate paradex-py method
        match path {
            "/v1/markets" => self.py_wrapper.fetch_markets(),
            "/v1/positions" => self.py_wrapper.fetch_positions(),
            "/v1/account" => self.py_wrapper.fetch_account(),
            "/v1/orders" => self.py_wrapper.fetch_orders(),
            _ if path.starts_with("/v1/orderbook/") => {
                let market = path.strip_prefix("/v1/orderbook/").unwrap();
                self.py_wrapper.fetch_orderbook(market)
            }
            _ if path.starts_with("/v1/fills?start_at=") => {
                let start_time = path.split("start_at=").nth(1)
                    .and_then(|s| s.parse::<u64>().ok())
                    .unwrap_or(0);
                self.py_wrapper.fetch_fills(start_time)
            }
            _ => self.get_public(path).await,
        }
    }

    /// Make unauthenticated GET request
    async fn get_public(&self, path: &str) -> Result<Value> {
        let url = format!("{}{}", self.config.http_url, path);
        debug!("GET {} (public)", url);
        
        let response = self.client
            .get(&url)
            .header("Accept", "application/json")
            .send()
            .await?;
        
        if !response.status().is_success() {
            let status = response.status();
            let body = response.text().await.unwrap_or_default();
            return Err(crate::error::ParadexError::Http(format!(
                "Request failed with status {}: {}",
                status, body
            )));
        }
        
        Ok(response.json().await?)
    }

    /// Get system time from Paradex
    pub async fn get_system_time(&self) -> Result<u64> {
        let json = self.get_public("/v1/system/time").await?;
        let server_time = json["server_time"]
            .as_u64()
            .ok_or_else(|| crate::error::ParadexError::Parse(
                "server_time not found in response".to_string(),
            ))?;
        debug!("Server time: {}", server_time);
        Ok(server_time)
    }

    /// Get all available markets
    pub async fn get_markets(&self) -> Result<Vec<Market>> {
        let json = self.get_authenticated("/v1/markets").await?;
        // Response is {"results": [...]}
        let results = json["results"].clone();
        let markets: Vec<Market> = serde_json::from_value(results)?;
        debug!("Received {} markets", markets.len());
        Ok(markets)
    }

    /// Get open orders for account
    pub async fn get_open_orders(&self) -> Result<Vec<Order>> {
        let json = self.get_authenticated("/v1/orders").await?;
        let results = json["results"].clone();
        let orders: Vec<Order> = serde_json::from_value(results)?;
        debug!("Received {} open orders", orders.len());
        Ok(orders)
    }

    /// Get fills since timestamp
    pub async fn get_fills(&self, start_time: u64) -> Result<Vec<Fill>> {
        let path = format!("/v1/fills?start_at={}", start_time);
        let json = self.get_authenticated(&path).await?;
        let results = json["results"].clone();
        let fills: Vec<Fill> = serde_json::from_value(results)?;
        debug!("Received {} fills", fills.len());
        Ok(fills)
    }

    /// Get current positions
    pub async fn get_positions(&self) -> Result<Vec<Position>> {
        let json = self.get_authenticated("/v1/positions").await?;
        let results = json["results"].clone();
        let positions: Vec<Position> = serde_json::from_value(results)?;
        debug!("Received {} positions", positions.len());
        Ok(positions)
    }

    /// Submit a new order
    pub async fn submit_order(&self, order: Order) -> Result<Order> {
        let url = format!("{}/v1/orders", self.config.http_url);
        info!("POST {} for order {}", url, order.id);
        let response = self.client.post(&url).json(&order).send().await?;
        let result: Order = response.json().await?;
        info!("Order submitted: {}", result.id);
        Ok(result)
    }

    /// Cancel an existing order
    pub async fn cancel_order(&self, order_id: &str) -> Result<Order> {
        let url = format!("{}/v1/orders/{}", self.config.http_url, order_id);
        info!("DELETE {}", url);
        let response = self.client.delete(&url).send().await?;
        let result: Order = response.json().await?;
        info!("Order cancelled: {}", result.id);
        Ok(result)
    }

    /// Get account balance
    pub async fn get_account(&self) -> Result<Value> {
        self.get_authenticated("/v1/account").await
    }

    /// Get order book for instrument
    pub async fn get_orderbook(&self, instrument_id: &str) -> Result<Value> {
        let path = format!("/v1/orderbook/{}", instrument_id);
        self.get_public(&path).await
    }

    /// Get recent trades for instrument
    pub async fn get_trades(&self, instrument_id: &str) -> Result<Value> {
        let path = format!("/v1/trades/{}", instrument_id);
        self.get_authenticated(&path).await
    }
}
