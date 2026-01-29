// crates/adapters/paradex/src/websocket/handlers.rs

use crate::error::Result;
use serde_json::Value;
use tracing::{debug, warn};

/// Callback for message handling
pub type MessageCallback = Box<dyn Fn(&Value) -> Result<()> + Send + Sync + 'static>;

/// WebSocket message handler with callbacks
pub struct MessageHandler {
    on_orderbook: Option<MessageCallback>,
    on_trades: Option<MessageCallback>,
    on_fills: Option<MessageCallback>,
    on_orders: Option<MessageCallback>,
    on_account: Option<MessageCallback>,
}

impl Clone for MessageHandler {
    fn clone(&self) -> Self {
        Self::default()
    }
}

impl Default for MessageHandler {
    fn default() -> Self {
        Self {
            on_orderbook: None,
            on_trades: None,
            on_fills: None,
            on_orders: None,
            on_account: None,
        }
    }
}

impl MessageHandler {
    /// Set callback for orderbook updates
    pub fn on_orderbook<F>(&mut self, callback: F)
    where
        F: Fn(&Value) -> Result<()> + Send + Sync + 'static,
    {
        self.on_orderbook = Some(Box::new(callback));
    }

    /// Set callback for trades
    pub fn on_trades<F>(&mut self, callback: F)
    where
        F: Fn(&Value) -> Result<()> + Send + Sync + 'static,
    {
        self.on_trades = Some(Box::new(callback));
    }

    /// Set callback for fills
    pub fn on_fills<F>(&mut self, callback: F)
    where
        F: Fn(&Value) -> Result<()> + Send + Sync + 'static,
    {
        self.on_fills = Some(Box::new(callback));
    }

    /// Set callback for orders
    pub fn on_orders<F>(&mut self, callback: F)
    where
        F: Fn(&Value) -> Result<()> + Send + Send + Sync + 'static,
    {
        self.on_orders = Some(Box::new(callback));
    }

    /// Set callback for account updates
    pub fn on_account<F>(&mut self, callback: F)
    where
        F: Fn(&Value) -> Result<()> + Send + Sync + 'static,
    {
        self.on_account = Some(Box::new(callback));
    }

    /// Handle incoming message and route to appropriate callback
    pub fn handle(&self, message: &str) -> Result<()> {
        let value: Value = serde_json::from_str(message)?;
        debug!("Handling message: {:?}", value);

        if let Some(method) = value.get("method") {
            if let Some(method_str) = method.as_str() {
                match method_str {
                    "subscription" => self.handle_subscription(&value)?,
                    "notification" => self.handle_notification(&value)?,
                    _ => {
                        warn!("Unknown method: {}", method_str);
                    }
                }
            }
        } else if let Some(result) = value.get("result") {
            debug!("Subscription successful: {:?}", result);
        } else if let Some(params) = value.get("params") {
            if let Some(array) = params.as_array() {
                if array.len() >= 2 {
                    let channel = array[0].as_str().unwrap_or("");
                    let data = array.get(1).unwrap();

                    match channel {
                        channel if channel.starts_with("orderbook.") => {
                            if let Some(cb) = &self.on_orderbook {
                                cb(data)?;
                            }
                        }
                        channel if channel.starts_with("trades.") => {
                            if let Some(cb) = &self.on_trades {
                                cb(data)?;
                            }
                        }
                        channel if channel.starts_with("fills.") => {
                            if let Some(cb) = &self.on_fills {
                                cb(data)?;
                            }
                        }
                        channel if channel.starts_with("orders.") => {
                            if let Some(cb) = &self.on_orders {
                                cb(data)?;
                            }
                        }
                        channel if channel.starts_with("account.") => {
                            if let Some(cb) = &self.on_account {
                                cb(data)?;
                            }
                        }
                        _ => {
                            debug!("Unhandled channel: {}", channel);
                        }
                    }
                }
            }
        } else {
            warn!("Message without method or result: {:?}", value);
        }

        Ok(())
    }

    /// Handle subscription message
    fn handle_subscription(&self, message: &Value) -> Result<()> {
        debug!("Subscription message: {:?}", message);
        if let Some(result) = message.get("result") {
            debug!("Subscription successful: {:?}", result);
        }
        Ok(())
    }

    /// Handle notification message
    fn handle_notification(&self, message: &Value) -> Result<()> {
        debug!("Notification message: {:?}", message);
        if let Some(params) = message.get("params") {
            debug!("Notification params: {:?}", params);
        }
        Ok(())
    }
}
