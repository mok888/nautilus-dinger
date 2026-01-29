// crates/adapters/paradex/src/lib.rs

pub mod common;
pub mod concurrency;
pub mod config;
pub mod error;
pub mod http;
pub mod python;
pub mod python_wrapper;
pub mod signing;
pub mod state;
pub mod websocket;
pub mod auth;

use pyo3::prelude::*;

#[pymodule]
fn paradex_adapter(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<config::PyParadexConfig>()?;
    m.add_class::<python::PyHttpClient>()?;
    m.add_class::<python::PyWebSocketClient>()?;
    m.add_class::<python::PySimpleWebSocketClient>()?;
    m.add_class::<python::PyParadexWebSocket>()?;
    m.add_class::<python::PyStarker>()?;
    Ok(())
}
