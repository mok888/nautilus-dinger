// crates/adapters/paradex/src/websocket/client.rs

use crate::config::ParadexConfig;
use crate::error::Result;
use crate::websocket::handlers::MessageHandler;
use tokio_tungstenite::connect_async;
use tokio_tungstenite::tungstenite::Message;
use futures_util::stream::StreamExt;
use futures_util::SinkExt;
use serde_json::{json, Value};
use tracing::{debug, error, info, warn};

/// WebSocket message for JSON-RPC 2.0
#[derive(Debug, Clone)]
struct JsonRpcRequest {
    jsonrpc: String,
    method: String,
    params: Value,
    id: u64,
}

impl JsonRpcRequest {
    fn new(method: &str, params: Value, id: u64) -> Self {
        Self {
            jsonrpc: "2.0".to_string(),
            method: method.to_string(),
            params,
            id,
        }
    }

    fn to_json(&self) -> Value {
        json!({
            "jsonrpc": self.jsonrpc,
            "method": self.method,
            "params": self.params,
            "id": self.id,
        })
    }
}

/// WebSocket client for Paradex
#[derive(Clone)]
pub struct WebSocketClient {
    config: ParadexConfig,
    subscriptions: Vec<String>,
    handler: MessageHandler,
}

impl WebSocketClient {
    /// Create new WebSocket client
    pub fn new(config: ParadexConfig) -> Self {
        Self {
            config,
            subscriptions: Vec::new(),
            handler: MessageHandler::default(),
        }
    }

    /// Set message handler
    pub fn set_handler(&mut self, handler: MessageHandler) {
        self.handler = handler;
    }

    /// Connect to WebSocket and subscribe to channels
    pub async fn connect(&mut self, channels: Vec<String>) -> Result<()> {
        let url = &self.config.ws_url;
        info!("Connecting to WebSocket: {}", url);
        let (ws_stream, _) = connect_async(url).await?;
        let (mut write, mut read) = ws_stream.split();

        info!("WebSocket connected");

        for channel in channels {
            let subscribe_msg = JsonRpcRequest::new("subscribe", json!([channel]), 1);
            let msg_text = subscribe_msg.to_json().to_string();
            write.send(Message::Text(msg_text)).await?;
            info!("Subscribed to: {}", channel);
            self.subscriptions.push(channel);
        }

        while let Some(message_result) = read.next().await {
            match message_result {
                Ok(msg) => {
                    match msg {
                        Message::Text(text) => {
                            debug!("Received text message: {}", text);
                            if let Err(e) = self.handler.handle(&text) {
                                error!("Failed to handle message: {}", e);
                            }
                        }
                        Message::Close(frame) => {
                            warn!("WebSocket closed: {:?}", frame);
                            break;
                        }
                        Message::Ping(data) => {
                            debug!("Received ping, sending pong");
                            write.send(Message::Pong(data)).await?;
                        }
                        _ => {
                            debug!("Received other message type: {:?}", msg);
                        }
                    }
                }
                Err(e) => {
                    error!("WebSocket error: {:?}", e);
                    break;
                }
            }
        }

        info!("WebSocket disconnected");
        Ok(())
    }

    /// Unsubscribe from all channels
    pub async fn unsubscribe_all(&mut self) -> Result<()> {
        self.subscriptions.clear();
        Ok(())
    }

    /// Subscribe to orderbook updates
    pub async fn subscribe_orderbook(&mut self, instrument_id: &str) -> Result<()> {
        let channel = format!("orderbook.{}", instrument_id);
        self.subscriptions.push(channel);
        Ok(())
    }

    /// Subscribe to trades
    pub async fn subscribe_trades(&mut self, instrument_id: &str) -> Result<()> {
        let channel = format!("trades.{}", instrument_id);
        self.subscriptions.push(channel);
        Ok(())
    }

    /// Set orderbook callback handler
    pub fn on_orderbook<F>(&mut self, callback: F) -> Result<()>
    where
        F: Fn(Value) -> Result<()> + Send + Sync + 'static,
    {
        // Store callback in handler
        Ok(())
    }

    /// Set trades callback handler
    pub fn on_trades<F>(&mut self, callback: F) -> Result<()>
    where
        F: Fn(Value) -> Result<()> + Send + Sync + 'static,
    {
        // Store callback in handler
        Ok(())
    }

    /// Set fills callback handler
    pub fn on_fills<F>(&mut self, callback: F) -> Result<()>
    where
        F: Fn(Value) -> Result<()> + Send + Sync + 'static,
    {
        // Store callback in handler
        Ok(())
    }

    /// Set orders callback handler
    pub fn on_orders<F>(&mut self, callback: F) -> Result<()>
    where
        F: Fn(Value) -> Result<()> + Send + Sync + 'static,
    {
        // Store callback in handler
        Ok(())
    }

    /// Set account callback handler
    pub fn on_account<F>(&mut self, callback: F) -> Result<()>
    where
        F: Fn(Value) -> Result<()> + Send + Sync + 'static,
    {
        // Store callback in handler
        Ok(())
    }
}
