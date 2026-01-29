// crates/adapters/paradex/src/common/types.rs

use serde::{Deserialize, Serialize};

/// Order data
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Order {
    pub id: String,
    pub client_id: String,
    pub instrument_id: String,
    pub side: String,
    pub order_type: String,
    pub size: String,
    pub price: Option<String>,
    pub status: String,
    pub filled_size: String,
    pub created_at: u64,
    pub updated_at: u64,
}

/// Fill data
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Fill {
    pub id: String,
    pub trade_id: String,
    pub order_id: String,
    pub instrument_id: String,
    pub side: String,
    pub size: String,
    pub price: String,
    pub fee: String,
    pub fee_currency: String,
    pub liquidity: String,
    pub created_at: u64,
}

/// Position data
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Position {
    pub id: String,
    pub instrument_id: String,
    pub side: String,
    pub size: String,
    pub entry_price: Option<String>,
    pub unrealized_pnl: Option<String>,
    pub updated_at: u64,
}

/// Market data
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Market {
    pub symbol: String,
    pub base_currency: String,
    pub quote_currency: String,
    pub price_tick_size: String,
    pub quantity_tick_size: String,
    pub min_quantity: String,
    pub max_quantity: String,
}
