// crates/adapters/paradex/src/websocket/simple_client.rs
//! Simplified WebSocket client with working callbacks

use crate::config::ParadexConfig;
use crate::error::Result;
use futures_util::{SinkExt, StreamExt};
use serde_json::{json, Value};
use std::sync::Arc;
use tokio::sync::Mutex;
use tokio_tungstenite::{connect_async, tungstenite::Message};
use tracing::{debug, error, info};

type Callback = Arc<dyn Fn(Value) + Send + Sync>;

/// Simple WebSocket client with callbacks
pub struct SimpleWebSocketClient {
    config: ParadexConfig,
    orderbook_callback: Arc<Mutex<Option<Callback>>>,
    trades_callback: Arc<Mutex<Option<Callback>>>,
}

impl SimpleWebSocketClient {
    pub fn new(config: ParadexConfig) -> Self {
        Self {
            config,
            orderbook_callback: Arc::new(Mutex::new(None)),
            trades_callback: Arc::new(Mutex::new(None)),
        }
    }

    pub async fn set_orderbook_callback<F>(&self, callback: F)
    where
        F: Fn(Value) + Send + Sync + 'static,
    {
        let mut cb = self.orderbook_callback.lock().await;
        *cb = Some(Arc::new(callback));
    }

    pub async fn set_trades_callback<F>(&self, callback: F)
    where
        F: Fn(Value) + Send + Sync + 'static,
    {
        let mut cb = self.trades_callback.lock().await;
        *cb = Some(Arc::new(callback));
    }

    pub async fn connect_and_subscribe(&self, channels: Vec<String>) -> Result<()> {
        let url = &self.config.ws_url;
        info!("Connecting to WebSocket: {}", url);

        let (ws_stream, _) = connect_async(url).await?;
        let (mut write, mut read) = ws_stream.split();

        info!("WebSocket connected");

        // Subscribe to channels
        for (id, channel) in channels.iter().enumerate() {
            let subscribe_msg = json!({
                "jsonrpc": "2.0",
                "method": "subscribe",
                "params": [channel],
                "id": id + 1
            });
            write
                .send(Message::Text(subscribe_msg.to_string()))
                .await?;
            info!("Subscribed to: {}", channel);
        }

        // Message loop
        while let Some(msg_result) = read.next().await {
            match msg_result {
                Ok(Message::Text(text)) => {
                    debug!("Received: {}", text);
                    if let Ok(data) = serde_json::from_str::<Value>(&text) {
                        self.handle_message(data).await;
                    }
                }
                Ok(Message::Ping(data)) => {
                    write.send(Message::Pong(data)).await?;
                }
                Ok(Message::Close(_)) => {
                    info!("WebSocket closed");
                    break;
                }
                Err(e) => {
                    error!("WebSocket error: {}", e);
                    break;
                }
                _ => {}
            }
        }

        Ok(())
    }

    async fn handle_message(&self, data: Value) {
        // Check if it's a subscription update
        if let Some(params) = data.get("params") {
            if let Some(channel) = params.get("channel").and_then(|c| c.as_str()) {
                if channel.starts_with("orderbook.") {
                    if let Some(cb) = self.orderbook_callback.lock().await.as_ref() {
                        if let Some(result) = params.get("result") {
                            cb(result.clone());
                        }
                    }
                } else if channel.starts_with("trades.") {
                    if let Some(cb) = self.trades_callback.lock().await.as_ref() {
                        if let Some(result) = params.get("result") {
                            cb(result.clone());
                        }
                    }
                }
            }
        }
    }
}
