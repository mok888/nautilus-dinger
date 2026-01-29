// crates/adapters/paradex/src/python/mod.rs

use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3_asyncio::tokio::future_into_py;
use std::sync::Arc;

use crate::config::PyParadexConfig;
use crate::signing::types::{OrderSignatureParams, SignatureParams};

/// Python wrapper for HttpClient
#[pyclass]
pub struct PyHttpClient {
    client: crate::http::HttpClient,
}

#[pymethods]
impl PyHttpClient {
    #[new]
    fn new(config: &PyParadexConfig) -> Self {
        Self {
            client: crate::http::HttpClient::new(config.config.clone()),
        }
    }

    fn get_system_time<'py>(&self, py: Python<'py>) -> PyResult<&'py PyAny> {
        let client = self.client.clone();
        future_into_py(py, async move {
            let result = client.get_system_time().await
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))?;
            Ok(result)
        })
    }

    fn get_markets<'py>(&self, py: Python<'py>) -> PyResult<&'py PyAny> {
        let client = self.client.clone();
        future_into_py(py, async move {
            let result = client.get_authenticated("/v1/markets").await
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))?;
            Ok(result.to_string())
        })
    }

    fn get_open_orders<'py>(&self, py: Python<'py>) -> PyResult<&'py PyAny> {
        let client = self.client.clone();
        future_into_py(py, async move {
            let result = client.get_authenticated("/v1/orders").await
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))?;
            Ok(result.to_string())
        })
    }

    fn get_fills<'py>(&self, py: Python<'py>, start_time: u64) -> PyResult<&'py PyAny> {
        let client = self.client.clone();
        future_into_py(py, async move {
            let path = format!("/v1/fills?start_at={}", start_time);
            let result = client.get_authenticated(&path).await
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))?;
            Ok(result.to_string())
        })
    }

    fn get_positions<'py>(&self, py: Python<'py>) -> PyResult<&'py PyAny> {
        let client = self.client.clone();
        future_into_py(py, async move {
            let result = client.get_authenticated("/v1/positions").await
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))?;
            Ok(result.to_string())
        })
    }

    fn get_account<'py>(&self, py: Python<'py>) -> PyResult<&'py PyAny> {
        let client = self.client.clone();
        future_into_py(py, async move {
            let result = client.get_authenticated("/v1/account").await
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))?;
            Ok(result.to_string())
        })
    }

    fn get_orderbook<'py>(&self, py: Python<'py>, instrument_id: String) -> PyResult<&'py PyAny> {
        let client = self.client.clone();
        future_into_py(py, async move {
            let result = client.get_orderbook(&instrument_id).await
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))?;
            let json = serde_json::to_string(&result)
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))?;
            Ok(json)
        })
    }

    fn get_trades<'py>(&self, py: Python<'py>, instrument_id: String) -> PyResult<&'py PyAny> {
        let client = self.client.clone();
        future_into_py(py, async move {
            let result = client.get_trades(&instrument_id).await
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))?;
            let json = serde_json::to_string(&result)
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))?;
            Ok(json)
        })
    }
    
    fn submit_order<'py>(
        &self,
        py: Python<'py>,
        market: String,
        side: String,
        order_type: String,
        size: String,
        price: Option<String>,
    ) -> PyResult<&'py PyAny> {
        let client = self.client.clone();
        future_into_py(py, async move {
            let mut order_json = serde_json::json!({
                "market": market,
                "side": side,
                "type": order_type,
                "size": size,
            });
            
            if let Some(p) = price {
                order_json["price"] = serde_json::json!(p);
            }
            
            let result = client.submit_order_json(order_json).await
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))?;
            
            let json = serde_json::to_string(&result)
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))?;
            
            Ok(json)
        })
    }
}

/// Python wrapper for SimpleWebSocketClient
#[pyclass]
pub struct PySimpleWebSocketClient {
    client: Arc<crate::websocket::SimpleWebSocketClient>,
    runtime: Arc<tokio::runtime::Runtime>,
}

#[pymethods]
impl PySimpleWebSocketClient {
    #[new]
    fn new(config: &PyParadexConfig) -> Self {
        let client = crate::websocket::SimpleWebSocketClient::new(config.config.clone());
        let runtime = tokio::runtime::Runtime::new().unwrap();
        
        Self {
            client: Arc::new(client),
            runtime: Arc::new(runtime),
        }
    }
    
    fn on_orderbook(&self, callback: PyObject) {
        let client = self.client.clone();
        self.runtime.block_on(async move {
            client.set_orderbook_callback(move |data| {
                Python::with_gil(|py| {
                    if let Ok(json_str) = serde_json::to_string(&data) {
                        let _ = callback.call1(py, (json_str,));
                    }
                });
            }).await;
        });
    }
    
    fn on_trades(&self, callback: PyObject) {
        let client = self.client.clone();
        self.runtime.block_on(async move {
            client.set_trades_callback(move |data| {
                Python::with_gil(|py| {
                    if let Ok(json_str) = serde_json::to_string(&data) {
                        let _ = callback.call1(py, (json_str,));
                    }
                });
            }).await;
        });
    }
    
    fn connect<'py>(&self, py: Python<'py>, channels: Vec<String>) -> PyResult<&'py PyAny> {
        let client = self.client.clone();
        future_into_py(py, async move {
            client.connect_and_subscribe(channels).await
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))
        })
    }
}

/// Python wrapper for WebSocketClient
#[pyclass]
pub struct PyWebSocketClient {
    ws_client: crate::websocket::WebSocketClient,
}

#[pymethods]
impl PyWebSocketClient {
    #[new]
    fn new(config: &PyParadexConfig) -> Self {
        Self {
            ws_client: crate::websocket::WebSocketClient::new(config.config.clone()),
        }
    }

    fn subscribe_orderbook<'py>(&self, py: Python<'py>, instrument_id: String) -> PyResult<&'py PyAny> {
        let mut client = self.ws_client.clone();
        future_into_py(py, async move {
            client.subscribe_orderbook(&instrument_id).await
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))
        })
    }

    fn subscribe_trades<'py>(&self, py: Python<'py>, instrument_id: String) -> PyResult<&'py PyAny> {
        let mut client = self.ws_client.clone();
        future_into_py(py, async move {
            client.subscribe_trades(&instrument_id).await
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))
        })
    }

    fn unsubscribe_all<'py>(&self, py: Python<'py>) -> PyResult<&'py PyAny> {
        let mut client = self.ws_client.clone();
        future_into_py(py, async move {
            client.unsubscribe_all().await
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))
        })
    }

    fn on_orderbook(&mut self, callback: PyObject) -> PyResult<()> {
        self.ws_client.on_orderbook(move |data| {
            Python::with_gil(|py| {
                if let Ok(json_str) = serde_json::to_string(&data) {
                    let _ = callback.call1(py, (json_str,));
                }
            });
            Ok(())
        }).map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))
    }

    fn on_trades(&mut self, callback: PyObject) -> PyResult<()> {
        self.ws_client.on_trades(move |data| {
            Python::with_gil(|py| {
                if let Ok(json_str) = serde_json::to_string(&data) {
                    let _ = callback.call1(py, (json_str,));
                }
            });
            Ok(())
        }).map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))
    }

    fn on_fills(&mut self, callback: PyObject) -> PyResult<()> {
        self.ws_client.on_fills(move |data| {
            Python::with_gil(|py| {
                if let Ok(json_str) = serde_json::to_string(&data) {
                    let _ = callback.call1(py, (json_str,));
                }
            });
            Ok(())
        }).map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))
    }

    fn on_orders(&mut self, callback: PyObject) -> PyResult<()> {
        self.ws_client.on_orders(move |data| {
            Python::with_gil(|py| {
                if let Ok(json_str) = serde_json::to_string(&data) {
                    let _ = callback.call1(py, (json_str,));
                }
            });
            Ok(())
        }).map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))
    }

    fn on_account(&mut self, callback: PyObject) -> PyResult<()> {
        self.ws_client.on_account(move |data| {
            Python::with_gil(|py| {
                if let Ok(json_str) = serde_json::to_string(&data) {
                    let _ = callback.call1(py, (json_str,));
                }
            });
            Ok(())
        }).map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))
    }
}

/// Python wrapper for STARK signer
#[pyclass]
pub struct PyStarker {
    starker: crate::signing::signer::Starker,
}

#[pymethods]
impl PyStarker {
    #[new]
    fn new(config: &PyParadexConfig) -> PyResult<Self> {
        let starker = crate::signing::signer::Starker::new(&config.config)
            .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))?;
        Ok(Self { starker })
    }

    fn get_account_address(&self) -> String {
        self.starker.get_account_address()
    }

    fn get_public_key(&self) -> String {
        self.starker.get_public_key()
    }

    fn sign_order(&self, params_dict: &PyDict) -> PyResult<String> {
        // Extract order params from Python dict
        let order_params = OrderSignatureParams {
            maker: params_dict.get_item("maker")?
                .map(|v| v.extract::<String>())
                .transpose()?
                .unwrap_or_default(),
            taker: params_dict.get_item("taker")?
                .map(|v| v.extract::<String>())
                .transpose()?
                .unwrap_or_default(),
            base_asset: params_dict.get_item("base_asset")?
                .map(|v| v.extract::<String>())
                .transpose()?
                .unwrap_or_default(),
            quote_asset: params_dict.get_item("quote_asset")?
                .map(|v| v.extract::<String>())
                .transpose()?
                .unwrap_or_default(),
            base_quantity: params_dict.get_item("base_quantity")?
                .map(|v| v.extract::<String>())
                .transpose()?
                .unwrap_or_default(),
            quote_quantity: params_dict.get_item("quote_quantity")?
                .map(|v| v.extract::<String>())
                .transpose()?
                .unwrap_or_default(),
            order_id: params_dict.get_item("order_id")?
                .map(|v| v.extract::<String>())
                .transpose()?
                .unwrap_or_default(),
            nonce: params_dict.get_item("nonce")?
                .map(|v| v.extract::<String>())
                .transpose()?
                .unwrap_or_default(),
            expiration: params_dict.get_item("expiration")?
                .map(|v| v.extract::<String>())
                .transpose()?
                .unwrap_or_default(),
            is_post_only: params_dict.get_item("is_post_only")?
                .map(|v| v.extract::<String>())
                .transpose()?
                .unwrap_or_else(|| "false".to_string()),
        };

        let sig_params = SignatureParams {
            order: order_params,
            verifying_contract_address: params_dict.get_item("verifying_contract_address")?
                .map(|v| v.extract::<String>())
                .transpose()?
                .unwrap_or_else(|| "0x0".to_string()),
            chain_id: params_dict.get_item("chain_id")?
                .map(|v| v.extract::<String>())
                .transpose()?
                .unwrap_or_else(|| "SN_SEPOLIA".to_string()),
        };

        let signature = self.starker.sign_order(&sig_params)
            .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{:?}", e)))?;

        Ok(format!("{{\"r\":\"{:#x}\",\"s\":\"{:#x}\"}}", signature.r, signature.s))
    }
}


#[pyclass]
pub struct PyParadexWebSocket {
    ws: Arc<tokio::sync::Mutex<Option<crate::websocket::jsonrpc_client::ParadexWebSocket>>>,
    runtime: Arc<tokio::runtime::Runtime>,
}

#[pymethods]
impl PyParadexWebSocket {
    #[new]
    fn new() -> PyResult<Self> {
        let runtime = tokio::runtime::Runtime::new()
            .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))?;

        Ok(Self {
            ws: Arc::new(tokio::sync::Mutex::new(None)),
            runtime: Arc::new(runtime),
        })
    }

    fn connect(&self, url: String) -> PyResult<()> {
        let ws = self.ws.clone();
        self.runtime.block_on(async move {
            let client = crate::websocket::jsonrpc_client::ParadexWebSocket::connect(&url)
                .await
                .map_err(|e| pyo3::exceptions::PyConnectionError::new_err(e.to_string()))?;
            *ws.lock().await = Some(client);
            Ok(())
        })
    }

    fn authenticate(&self, jwt_token: String) -> PyResult<()> {
        let ws = self.ws.clone();
        self.runtime.block_on(async move {
            let ws_guard = ws.lock().await;
            if let Some(client) = ws_guard.as_ref() {
                client.authenticate(&jwt_token)
                    .await
                    .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))?;
                Ok(())
            } else {
                Err(pyo3::exceptions::PyRuntimeError::new_err("Not connected"))
            }
        })
    }

    fn subscribe(&self, channel: String) -> PyResult<()> {
        let ws = self.ws.clone();
        self.runtime.block_on(async move {
            let ws_guard = ws.lock().await;
            if let Some(client) = ws_guard.as_ref() {
                client.subscribe(&channel)
                    .await
                    .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))?;
                Ok(())
            } else {
                Err(pyo3::exceptions::PyRuntimeError::new_err("Not connected"))
            }
        })
    }

    fn recv(&self) -> PyResult<Option<String>> {
        let ws = self.ws.clone();
        self.runtime.block_on(async move {
            let ws_guard = ws.lock().await;
            if let Some(client) = ws_guard.as_ref() {
                let msg = client.recv()
                    .await
                    .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))?;
                Ok(msg.map(|v| v.to_string()))
            } else {
                Err(pyo3::exceptions::PyRuntimeError::new_err("Not connected"))
            }
        })
    }

    fn close(&self) -> PyResult<()> {
        let ws = self.ws.clone();
        self.runtime.block_on(async move {
            let ws_guard = ws.lock().await;
            if let Some(client) = ws_guard.as_ref() {
                client.close()
                    .await
                    .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))?;
            }
            Ok(())
        })
    }
}
