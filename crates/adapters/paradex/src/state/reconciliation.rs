// crates/adapters/paradex/src/state/reconciliation.rs

use crate::error::Result;
use crate::http::HttpClient;
use crate::state::models::{AdapterState, OrderState, FillState, PositionState};
use crate::common::{Order, Fill, Position};
use serde_json::Value;
use tracing::{debug, info, warn};

/// Reconciliation manager for Paradex adapter
pub struct ReconciliationManager {
    client: HttpClient,
    state: AdapterState,
}

impl ReconciliationManager {
    /// Create new reconciliation manager
    pub fn new(client: HttpClient, state: AdapterState) -> Self {
        Self { client, state }
    }

    /// Perform full reconciliation with REST API
    pub async fn reconcile(&mut self) -> Result<()> {
        info!("Starting reconciliation...");
        
        // Reconcile orders
        let rest_orders = self.client.get_open_orders().await.map_err(|e| {
            error!("Failed to fetch orders: {}", e)
        })?;
        info!("Fetched {} orders from REST", rest_orders.len());
        
        for order in &rest_orders {
            self.state.orders.orders.insert(order.id.clone(), order);
            debug!("Reconciled order: {}", order.id);
        }

        // Reconcile fills
        let rest_fills = self.client.get_fills(0).await.map_err(|e| {
            error!("Failed to fetch fills: {}", e)
        })?;
        info!("Fetched {} fills from REST", rest_fills.len());
        
        for fill in &rest_fills {
            self.state.fills.fills.insert(fill.id.clone(), fill);
            debug!("Reconciled fill: {}", fill.id);
        }

        // Reconcile positions
        let rest_positions = self.client.get_positions().await.map_err(|e| {
            error!("Failed to fetch positions: {}", e)
        })?;
        info!("Fetched {} positions from REST", rest_positions.len());
        
        for position in &rest_positions {
            self.state.positions.positions.insert(position.id.clone(), position);
            debug!("Reconciled position: {}", position.id);
        }

        info!("Reconciliation completed");
        Ok(())
    }

    /// Get reconciliation state snapshot
    pub fn snapshot(&self) -> Result<AdapterState> {
        Ok(AdapterState {
            orders: OrderState {
                orders: self.state.orders.orders.clone().into_iter().collect(),
            },
            fills: FillState {
                fills: self.state.fills.fills.clone().into_iter().collect(),
            },
            positions: PositionState {
                positions: self.state.positions.positions.clone().into_iter().collect(),
            },
            subscriptions: self.state.subscriptions.clone(),
        })
    }

    /// Restore from snapshot
    pub fn restore(&mut self, snapshot: AdapterState) {
        self.state.orders.orders = snapshot.orders.orders;
        self.state.fills.fills = snapshot.fills;
        self.state.positions.positions = snapshot.positions;
        self.state.subscriptions = snapshot.subscriptions;
    }
}
