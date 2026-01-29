use anyhow::{Context, Result};
use futures_util::{SinkExt, StreamExt};
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;
use tokio::net::TcpStream;
use tokio::sync::Mutex;
use tokio_tungstenite::{connect_async, tungstenite::Message, MaybeTlsStream, WebSocketStream};

type WsStream = WebSocketStream<MaybeTlsStream<TcpStream>>;

#[derive(Debug, Serialize)]
struct JsonRpcRequest {
    jsonrpc: String,
    method: String,
    params: Value,
    id: u64,
}

#[derive(Debug, Deserialize)]
struct JsonRpcResponse {
    jsonrpc: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    result: Option<Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    error: Option<Value>,
    id: u64,
}

pub struct ParadexWebSocket {
    ws: Arc<Mutex<WsStream>>,
    message_id: AtomicU64,
}

impl ParadexWebSocket {
    pub async fn connect(url: &str) -> Result<Self> {
        let (ws, _) = connect_async(url)
            .await
            .context("Failed to connect to WebSocket")?;

        Ok(Self {
            ws: Arc::new(Mutex::new(ws)),
            message_id: AtomicU64::new(0),
        })
    }

    fn next_id(&self) -> u64 {
        self.message_id.fetch_add(1, Ordering::SeqCst)
    }

    pub async fn authenticate(&self, jwt_token: &str) -> Result<()> {
        let request = JsonRpcRequest {
            jsonrpc: "2.0".to_string(),
            method: "auth".to_string(),
            params: json!({ "bearer": jwt_token }),
            id: self.next_id(),
        };

        let msg = serde_json::to_string(&request)?;
        self.ws.lock().await.send(Message::Text(msg)).await?;

        Ok(())
    }

    pub async fn subscribe(&self, channel: &str) -> Result<()> {
        let request = JsonRpcRequest {
            jsonrpc: "2.0".to_string(),
            method: "subscribe".to_string(),
            params: json!({ "channel": channel }),
            id: self.next_id(),
        };

        let msg = serde_json::to_string(&request)?;
        self.ws.lock().await.send(Message::Text(msg)).await?;

        Ok(())
    }

    pub async fn recv(&self) -> Result<Option<Value>> {
        let mut ws = self.ws.lock().await;
        
        // Add timeout
        let timeout_duration = std::time::Duration::from_secs(1);
        match tokio::time::timeout(timeout_duration, ws.next()).await {
            Ok(Some(msg)) => {
                let msg = msg?;
                match msg {
                    Message::Text(text) => {
                        let value: Value = serde_json::from_str(&text)?;
                        return Ok(Some(value));
                    }
                    Message::Ping(data) => {
                        ws.send(Message::Pong(data)).await?;
                    }
                    Message::Close(_) => return Ok(None),
                    _ => {}
                }
            }
            Ok(None) => return Ok(None),
            Err(_) => return Ok(None), // Timeout
        }

        Ok(None)
    }

    pub async fn close(&self) -> Result<()> {
        self.ws.lock().await.close(None).await?;
        Ok(())
    }
}
