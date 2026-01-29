// crates/adapters/paradex/src/state/models.rs

use crate::common::types::{Fill, Order, Position};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// State for tracking orders
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OrderState {
    pub orders: HashMap<String, Order>,
}

/// State for tracking fills
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FillState {
    pub fills: HashMap<String, Fill>,
}

/// State for tracking positions
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PositionState {
    pub positions: HashMap<String, Position>,
}

/// State for tracking subscriptions
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SubscriptionState {
    pub subscriptions: Vec<String>,
}

/// Centralized state for Paradex adapter
#[derive(Debug, Clone)]
pub struct AdapterState {
    pub orders: OrderState,
    pub fills: FillState,
    pub positions: PositionState,
    pub subscriptions: SubscriptionState,
}

impl AdapterState {
    pub fn new() -> Self {
        Self {
            orders: OrderState {
                orders: HashMap::new(),
            },
            fills: FillState {
                fills: HashMap::new(),
            },
            positions: PositionState {
                positions: HashMap::new(),
            },
            subscriptions: SubscriptionState {
                subscriptions: Vec::new(),
            },
        }
    }
}
