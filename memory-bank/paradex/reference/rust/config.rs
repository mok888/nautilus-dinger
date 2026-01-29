// crates/adapters/paradex/src/lib.rs
// Copyright (C) 2015-2026 Nautech Systems Pty Ltd.

//! Paradex adapter for Nautilus Trader.

pub mod common;
pub mod config;
pub mod data;
pub mod error;
pub mod execution;
pub mod http;
pub mod python;
pub mod websocket;

use pyo3::prelude::*;

#[pymodule]
fn paradex_adapter(_py: Python, m: &PyModule) -> PyResult<()> {
    python::register_python_module(m)?;
    Ok(())
}
