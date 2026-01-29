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
    
    #[error("Python error: {0}")]
    Python(String),
}

impl From<reqwest::Error> for ParadexError {
    fn from(err: reqwest::Error) -> Self {
        ParadexError::Http(err.to_string())
    }
}

impl From<tokio_tungstenite::tungstenite::Error> for ParadexError {
    fn from(err: tokio_tungstenite::tungstenite::Error) -> Self {
        ParadexError::WebSocket(err.to_string())
    }
}

impl From<serde_json::Error> for ParadexError {
    fn from(err: serde_json::Error) -> Self {
        ParadexError::Parse(err.to_string())
    }
}
