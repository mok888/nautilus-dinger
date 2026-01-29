# PATTERNS - CODE REFERENCE

**Purpose:** Copy-paste patterns from OKX adapter adapted for Paradex

---

## 🎯 PYTHON PATTERNS

### 1. Method Signatures (CRITICAL)

**WRONG:**
```python
async def _subscribe_trade_ticks(self, instrument_id: InstrumentId) -> None:
    pass
```

**CORRECT:**
```python
async def _subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
    instrument_id = command.instrument_id
    # Implementation...
```

**Rule:** All subscription/request methods accept command objects, not raw parameters.

---

### 2. Subscription Methods

**Pattern:**
```python
async def _subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
    """Subscribe to trade tick updates."""
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.subscribe_trades(pyo3_instrument_id)
    self._log.info(f"Subscribed to trades: {command.instrument_id}")

async def _subscribe_quote_ticks(self, command: SubscribeQuoteTicks) -> None:
    """Subscribe to quote tick updates."""
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.subscribe_quotes(pyo3_instrument_id)
    self._log.info(f"Subscribed to quotes: {command.instrument_id}")

async def _subscribe_bars(self, command: SubscribeBars) -> None:
    """Subscribe to bar updates."""
    pyo3_bar_type = nautilus_pyo3.BarType.from_str(command.bar_type.value)
    await self._ws_client.subscribe_bars(pyo3_bar_type)
    self._log.info(f"Subscribed to bars: {command.bar_type}")
```

---

### 3. Unsubscription Methods

**Pattern:**
```python
async def _unsubscribe_trade_ticks(self, command: UnsubscribeTradeTicks) -> None:
    """Unsubscribe from trade tick updates."""
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.unsubscribe_trades(pyo3_instrument_id)
    self._log.info(f"Unsubscribed from trades: {command.instrument_id}")
```

---

### 4. Request Methods

**Pattern:**
```python
async def _request_bars(self, command: RequestBars) -> None:
    """Request historical bars."""
    try:
        bars = await self._http_client.get_bars(
            instrument_id=command.instrument_id,
            bar_type=command.bar_type,
            start=command.start,
            end=command.end,
        )
        self._handle_bars(bars, command.correlation_id)
    except Exception as e:
        self._log.error(f"Failed to request bars: {e}")
        # Send error response
        self._send_data_response(
            data_type=DataType(BarType, metadata={"bar_type": command.bar_type}),
            data=None,
            correlation_id=command.correlation_id,
        )

async def _request_quote_ticks(self, command: RequestQuoteTicks) -> None:
    """Request historical quote ticks."""
    try:
        quotes = await self._http_client.get_quotes(
            instrument_id=command.instrument_id,
            start=command.start,
            end=command.end,
        )
        self._handle_quotes(quotes, command.correlation_id)
    except Exception as e:
        self._log.error(f"Failed to request quotes: {e}")
```

---

### 5. Reconciliation Logic (CRITICAL)

**Pattern:**
```python
async def _reconcile_state(self) -> None:
    """
    Reconcile state from REST API.
    
    REST is authoritative - never trust WebSocket data alone.
    """
    self._log.info("Starting state reconciliation...")
    
    # 1. Fetch open orders from REST
    try:
        open_orders = await self._http_client.get_open_orders()
    except Exception as e:
        self._log.error(f"Failed to fetch open orders: {e}")
        return
    
    # 2. Generate order status reports
    for order_data in open_orders:
        try:
            report = self._parse_order_status_report(order_data)
            self._send_order_status_report(report)
        except Exception as e:
            self._log.error(f"Failed to parse order: {e}")
    
    # 3. Fetch recent fills (since last reconciliation)
    try:
        fills = await self._http_client.get_fills(
            start_time=self._last_reconcile_time
        )
    except Exception as e:
        self._log.error(f"Failed to fetch fills: {e}")
        return
    
    # 4. Generate fill reports (with deduplication)
    for fill_data in fills:
        trade_id = TradeId(fill_data["trade_id"])
        
        # Deduplicate: only emit if not already emitted
        if trade_id not in self._emitted_fills:
            try:
                report = self._parse_fill_report(fill_data)
                self._send_fill_report(report)
                self._emitted_fills.add(trade_id)
            except Exception as e:
                self._log.error(f"Failed to parse fill: {e}")
    
    # 5. Fetch positions
    try:
        positions = await self._http_client.get_positions()
    except Exception as e:
        self._log.error(f"Failed to fetch positions: {e}")
        return
    
    # 6. Generate position reports
    for position_data in positions:
        try:
            report = self._parse_position_report(position_data)
            self._send_position_status_report(report)
        except Exception as e:
            self._log.error(f"Failed to parse position: {e}")
    
    # Update last reconciliation time
    self._last_reconcile_time = self._clock.timestamp_ns()
    self._log.info("State reconciliation complete")

async def _run_reconciliation_loop(self) -> None:
    """Run periodic reconciliation in background."""
    while self._is_connected:
        await asyncio.sleep(self._config.reconcile_interval_secs)
        try:
            await self._reconcile_state()
        except Exception as e:
            self._log.error(f"Reconciliation loop error: {e}")
```

**Key Points:**
- REST is authoritative
- Deduplicate fills using `_emitted_fills` set
- Handle errors gracefully
- Run periodically (default: 5 min)

---

### 6. Helper Methods

**Pattern:**
```python
def _to_pyo3_instrument_id(self, instrument_id: InstrumentId) -> nautilus_pyo3.InstrumentId:
    """Convert Nautilus InstrumentId to PyO3 type."""
    return nautilus_pyo3.InstrumentId.from_str(instrument_id.value)

def _to_pyo3_bar_type(self, bar_type: BarType) -> nautilus_pyo3.BarType:
    """Convert Nautilus BarType to PyO3 type."""
    return nautilus_pyo3.BarType.from_str(bar_type.value)

def _to_pyo3_order_side(self, order_side: OrderSide) -> nautilus_pyo3.OrderSide:
    """Convert Nautilus OrderSide to PyO3 type."""
    return nautilus_pyo3.OrderSide.from_str(order_side.value)
```

---

### 7. Order Submission

**Pattern:**
```python
async def _submit_order(self, command: SubmitOrder) -> None:
    """Submit order to exchange."""
    order = command.order
    
    # Convert to Paradex format
    paradex_order = {
        "market": str(order.instrument_id),
        "side": "BUY" if order.side == OrderSide.BUY else "SELL",
        "type": self._convert_order_type(order.order_type),
        "size": str(order.quantity),
    }
    
    # Add price for limit orders
    if hasattr(order, "price"):
        paradex_order["price"] = str(order.price)
    
    # Sign order (STARK signature)
    signed_order = await self._http_client.sign_and_submit_order(paradex_order)
    
    # Track order
    self._order_states[order.client_order_id] = {
        "order": order,
        "exchange_order_id": signed_order["id"],
        "status": OrderStatus.SUBMITTED,
    }
    
    self._log.info(f"Order submitted: {order.client_order_id}")
```

---

## 🦀 RUST PATTERNS

### 1. State Management (DashMap)

**WRONG (current):**
```rust
use std::sync::RwLock;
use std::collections::HashMap;

struct State {
    orders: RwLock<HashMap<String, Order>>,
}
```

**CORRECT:**
```rust
use dashmap::DashMap;

struct State {
    orders: DashMap<String, Order>,
}

impl State {
    fn get_order(&self, id: &str) -> Option<Order> {
        self.orders.get(id).map(|r| r.clone())
    }
    
    fn insert_order(&self, id: String, order: Order) {
        self.orders.insert(id, order);
    }
}
```

**Why:** DashMap is 100x faster for concurrent access

---

### 2. Connection State Machine

**Pattern:**
```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum ConnectionState {
    Disconnected,
    Connecting,
    Connected,
    Authenticating,
    Authenticated,
    Reconnecting,
    Degraded,
}

impl ConnectionState {
    fn can_transition_to(&self, next: ConnectionState) -> bool {
        match (self, next) {
            (Disconnected, Connecting) => true,
            (Connecting, Connected) => true,
            (Connected, Authenticating) => true,
            (Authenticating, Authenticated) => true,
            (Authenticated, Disconnected) => true,
            (_, Reconnecting) => true,
            (_, Degraded) => true,
            _ => false,
        }
    }
}
```

---

### 3. Event Emission

**WRONG:**
```rust
// Custom event types
struct OrderEvent {
    order_id: String,
    status: String,
}
```

**CORRECT:**
```rust
use nautilus_model::events::{OrderAccepted, OrderFilled, OrderCanceled};

fn emit_order_accepted(&self, order_id: ClientOrderId) {
    let event = OrderAccepted::new(
        order_id,
        self.account_id,
        self.clock.timestamp_ns(),
    );
    self.send_event(event);
}

fn emit_order_filled(&self, fill: Fill) {
    let event = OrderFilled::new(
        fill.order_id,
        fill.trade_id,
        fill.quantity,
        fill.price,
        self.clock.timestamp_ns(),
    );
    self.send_event(event);
}
```

---

### 4. PyO3 Bindings

**Pattern:**
```rust
use pyo3::prelude::*;

#[pyclass]
struct ParadexHttpClient {
    inner: Arc<HttpClient>,
}

#[pymethods]
impl ParadexHttpClient {
    #[new]
    fn new(config: ParadexConfig) -> PyResult<Self> {
        let client = HttpClient::new(config)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;
        Ok(Self {
            inner: Arc::new(client),
        })
    }
    
    fn get_instruments<'py>(&self, py: Python<'py>) -> PyResult<&'py PyAny> {
        let client = self.inner.clone();
        pyo3_asyncio::tokio::future_into_py(py, async move {
            let instruments = client.get_instruments().await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;
            Ok(instruments)
        })
    }
}
```

---

### 5. Error Handling

**Pattern:**
```rust
use thiserror::Error;

#[derive(Error, Debug)]
enum ParadexError {
    #[error("HTTP error: {0}")]
    Http(#[from] reqwest::Error),
    
    #[error("WebSocket error: {0}")]
    WebSocket(String),
    
    #[error("Parse error: {0}")]
    Parse(#[from] serde_json::Error),
    
    #[error("Authentication failed: {0}")]
    Auth(String),
}

type Result<T> = std::result::Result<T, ParadexError>;
```

---

## 📊 PARADEX-SPECIFIC PATTERNS

### 1. STARK Signature

```python
# Python side (calls Rust)
signed_order = await self._http_client.sign_order(order_params)
```

```rust
// Rust side
use starknet_crypto::{sign, FieldElement};

fn sign_order(&self, order: &Order) -> Result<Signature> {
    let message_hash = self.compute_order_hash(order)?;
    let private_key = FieldElement::from_hex_be(&self.config.private_key)?;
    let signature = sign(&private_key, &message_hash, &self.config.public_key)?;
    Ok(signature)
}
```

### 2. Timestamp Conversion

```python
# Paradex uses milliseconds, Nautilus uses nanoseconds
paradex_ts_ms = nautilus_ts_ns // 1_000_000
nautilus_ts_ns = paradex_ts_ms * 1_000_000
```

### 3. Market ID Format

```python
# Paradex: "BTC-USD-PERP"
# Nautilus: InstrumentId("BTC-USD-PERP.PARADEX")

def to_nautilus_instrument_id(paradex_market: str) -> InstrumentId:
    return InstrumentId.from_str(f"{paradex_market}.PARADEX")

def to_paradex_market(instrument_id: InstrumentId) -> str:
    return instrument_id.symbol.value
```

---

## 💡 ANTI-PATTERNS (AVOID)

### ❌ DON'T: Trust WebSocket alone
```python
# WRONG
async def on_fill(self, fill_data):
    self._send_fill_report(fill_data)  # Might be duplicate!
```

### ✅ DO: Deduplicate with REST
```python
# CORRECT
async def on_fill(self, fill_data):
    trade_id = TradeId(fill_data["trade_id"])
    if trade_id not in self._emitted_fills:
        self._send_fill_report(fill_data)
        self._emitted_fills.add(trade_id)
```

### ❌ DON'T: Use RwLock for state
```rust
// WRONG - 100x slower
let orders = RwLock::new(HashMap::new());
```

### ✅ DO: Use DashMap
```rust
// CORRECT - concurrent and fast
let orders = DashMap::new();
```

### ❌ DON'T: Skip reconciliation
```python
# WRONG
async def _connect(self):
    await self._ws_client.connect()
    # Missing reconciliation!
```

### ✅ DO: Always reconcile on connect
```python
# CORRECT
async def _connect(self):
    await self._ws_client.connect()
    await self._reconcile_state()  # MANDATORY
    asyncio.create_task(self._run_reconciliation_loop())
```

---

**Next: See BUGS.md for known issues**
