// crates/adapters/paradex/src/python_wrapper.rs
//! Wrapper around paradex-py SDK for correct EIP-712 implementation

use pyo3::prelude::*;
use pyo3::types::{PyDict, PyModule};
use crate::config::ParadexConfig;
use crate::error::Result;
use serde_json::Value;

/// Python SDK wrapper for Paradex
pub struct ParadexPyWrapper {
    py_client: PyObject,
}

impl ParadexPyWrapper {
    /// Create new wrapper using paradex-py SDK
    pub fn new(config: &ParadexConfig) -> Result<Self> {
        Python::with_gil(|py| {
            // Import paradex_py
            let paradex_py = PyModule::import(py, "paradex_py")
                .map_err(|e| crate::error::ParadexError::Python(format!("Import error: {}", e)))?;
            
            let subkey_class = paradex_py.getattr("ParadexSubkey")
                .map_err(|e| crate::error::ParadexError::Python(format!("Class error: {}", e)))?;
            
            // Create ParadexSubkey instance
            let py_client = subkey_class.call1((
                &config.environment,
                &config.subkey_private_key,
                &config.l2_address,
            ))
            .map_err(|e| crate::error::ParadexError::Python(format!("Init error: {}", e)))?;
            
            Ok(Self {
                py_client: py_client.into(),
            })
        })
    }
    
    /// Fetch markets
    pub fn fetch_markets(&self) -> Result<Value> {
        Python::with_gil(|py| {
            let api_client = self.py_client.getattr(py, "api_client")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            let result = api_client.call_method0(py, "fetch_markets")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            let json_module = PyModule::import(py, "json")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            let json_str = json_module.getattr("dumps")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?
                .call1((result,))
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?
                .extract::<String>()
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            serde_json::from_str(&json_str)
                .map_err(|e| crate::error::ParadexError::Parse(format!("{}", e)))
        })
    }
    
    /// Fetch orderbook
    pub fn fetch_orderbook(&self, market: &str) -> Result<Value> {
        Python::with_gil(|py| {
            let api_client = self.py_client.getattr(py, "api_client")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            let result = api_client.call_method1(py, "fetch_orderbook", (market,))
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            let json_module = PyModule::import(py, "json")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            let json_str = json_module.getattr("dumps")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?
                .call1((result,))
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?
                .extract::<String>()
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            serde_json::from_str(&json_str)
                .map_err(|e| crate::error::ParadexError::Parse(format!("{}", e)))
        })
    }
    
    /// Fetch positions
    pub fn fetch_positions(&self) -> Result<Value> {
        Python::with_gil(|py| {
            let api_client = self.py_client.getattr(py, "api_client")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            let result = api_client.call_method0(py, "fetch_positions")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            let json_module = PyModule::import(py, "json")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            let json_str = json_module.getattr("dumps")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?
                .call1((result,))
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?
                .extract::<String>()
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            serde_json::from_str(&json_str)
                .map_err(|e| crate::error::ParadexError::Parse(format!("{}", e)))
        })
    }
    
    /// Fetch account
    pub fn fetch_account(&self) -> Result<Value> {
        Python::with_gil(|py| {
            let api_client = self.py_client.getattr(py, "api_client")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            let result = api_client.call_method0(py, "fetch_account_info")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            let json_module = PyModule::import(py, "json")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            let json_str = json_module.getattr("dumps")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?
                .call1((result,))
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?
                .extract::<String>()
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            serde_json::from_str(&json_str)
                .map_err(|e| crate::error::ParadexError::Parse(format!("{}", e)))
        })
    }
    
    /// Fetch open orders
    pub fn fetch_orders(&self) -> Result<Value> {
        Python::with_gil(|py| {
            let api_client = self.py_client.getattr(py, "api_client")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            let result = api_client.call_method0(py, "fetch_orders")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            let json_module = PyModule::import(py, "json")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            let json_str = json_module.getattr("dumps")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?
                .call1((result,))
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?
                .extract::<String>()
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            serde_json::from_str(&json_str)
                .map_err(|e| crate::error::ParadexError::Parse(format!("{}", e)))
        })
    }
    
    /// Fetch fills
    pub fn fetch_fills(&self, start_time: u64) -> Result<Value> {
        Python::with_gil(|py| {
            let api_client = self.py_client.getattr(py, "api_client")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            let params = pyo3::types::PyDict::new(py);
            params.set_item("start_at", start_time)
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            let result = api_client.call_method1(py, "fetch_fills", (params,))
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            let json_module = PyModule::import(py, "json")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            let json_str = json_module.getattr("dumps")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?
                .call1((result,))
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?
                .extract::<String>()
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            serde_json::from_str(&json_str)
                .map_err(|e| crate::error::ParadexError::Parse(format!("{}", e)))
        })
    }
    pub fn submit_order(&self, order: Value) -> Result<Value> {
        Python::with_gil(|py| {
            let api_client = self.py_client.getattr(py, "api_client")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            // Import Order class
            let paradex_py = PyModule::import(py, "paradex_py.common.order")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            let order_class = paradex_py.getattr("Order")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            let order_side_class = paradex_py.getattr("OrderSide")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            let order_type_class = paradex_py.getattr("OrderType")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            // Create Order object
            let decimal_module = PyModule::import(py, "decimal")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            let decimal_class = decimal_module.getattr("Decimal")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            let kwargs = PyDict::new(py);
            // Map side and type to correct enum values
            let side_value = match order["side"].as_str().unwrap() {
                "BUY" => "Buy",
                "SELL" => "Sell",
                s => s,
            };
            let type_value = match order["type"].as_str().unwrap() {
                "LIMIT" => "Limit",
                "MARKET" => "Market",
                t => t,
            };
            
            kwargs.set_item("market", order["market"].as_str().unwrap())
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            kwargs.set_item("order_side", order_side_class.getattr(side_value)
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?)
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            kwargs.set_item("order_type", order_type_class.getattr(type_value)
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?)
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            kwargs.set_item("size", decimal_class.call1((order["size"].as_str().unwrap(),))
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?)
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            if let Some(price) = order.get("price") {
                kwargs.set_item("limit_price", decimal_class.call1((price.as_str().unwrap(),))
                    .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?)
                    .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            }
            
            let py_order = order_class.call((), Some(kwargs))
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            // Submit
            let result = api_client.call_method1(py, "submit_order", (py_order,))
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            let json_module = PyModule::import(py, "json")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            let json_str = json_module.getattr("dumps")
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?
                .call1((result,))
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?
                .extract::<String>()
                .map_err(|e| crate::error::ParadexError::Python(format!("{}", e)))?;
            
            serde_json::from_str(&json_str)
                .map_err(|e| crate::error::ParadexError::Parse(format!("{}", e)))
        })
    }
}
