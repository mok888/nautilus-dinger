// crates/adapters/paradex/src/error.rs

use thiserror::Error;

pub type Result<T> = std::result::Result<T, ParadexError>;

#[derive(Error, Debug)]
pub enum ParadexError {
    #[error("HTTP error: {0}")]
    Http(String),

    #[error("WebSocket error: {0}")]
    WebSocket(String),

    #[error("Authentication error: {0}")]
    Auth(String),

    #[error("STARK signature error: {0}")]
    Signature(String),

    #[error("Parsing error: {0}")]
    Parse(String),

    #[error("Configuration error: {0}")]
    Config(String),
}
