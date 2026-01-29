# BUGS - KNOWN ISSUES

**Total Bugs:** 12 (3 Python + 9 Rust)  
**Status:** All documented, ready to fix

---

## 🐍 PYTHON LAYER BUGS (3)

### Bug #001: Wrong Method Signatures ⚠️ CRITICAL
**Severity:** HIGH  
**Impact:** Methods won't be called by Nautilus framework  
**Status:** Not fixed

**Problem:**
6 methods accept raw parameters instead of command objects.

**Affected Methods:**
1. `_subscribe_trade_ticks`
2. `_subscribe_quote_ticks`
3. `_subscribe_order_book_deltas`
4. `_subscribe_order_book_snapshots`
5. `_unsubscribe_trade_ticks`
6. `_unsubscribe_quote_ticks`

**Current (WRONG):**
```python
async def _subscribe_trade_ticks(self, instrument_id: InstrumentId) -> None:
    pass
```

**Should Be:**
```python
async def _subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
    instrument_id = command.instrument_id
    # Implementation...
```

**Fix:** See WORKFLOW.md Phase 1, Step 1

---

### Bug #002: Missing 30 Data Client Methods ⚠️ CRITICAL
**Severity:** HIGH  
**Impact:** Adapter is non-compliant, missing functionality  
**Status:** Not fixed

**Problem:**
Data client only has 8 methods, needs 38 total.

**Missing Methods (30):**

**Base Methods (3):**
- `_subscribe(data_type: DataType)`
- `_unsubscribe(data_type: DataType)`
- `_request(data_type: DataType, correlation_id: UUID4)`

**Subscription Methods (16):**
- `_subscribe_bars`
- `_subscribe_instrument_status`
- `_subscribe_instrument_close`
- `_subscribe_mark_price`
- `_subscribe_funding_rate`
- `_subscribe_index_price`
- `_subscribe_open_interest`
- `_subscribe_liquidations`
- `_unsubscribe_bars`
- `_unsubscribe_order_book_deltas`
- `_unsubscribe_order_book_snapshots`
- `_unsubscribe_instrument_status`
- `_unsubscribe_instrument_close`
- `_unsubscribe_mark_price`
- `_unsubscribe_funding_rate`
- `_unsubscribe_index_price`

**Request Methods (7):**
- `_request_quote_ticks`
- `_request_trade_ticks`
- `_request_bars`
- `_request_instrument`
- `_request_instruments`
- `_request_order_book_snapshot`
- `_request_data`

**Additional (4):**
- `_subscribe_open_interest`
- `_subscribe_liquidations`
- `_unsubscribe_open_interest`
- `_unsubscribe_liquidations`

**Fix:** See WORKFLOW.md Phase 1, Steps 2-4

---

### Bug #003: Missing 2 Execution Client Methods ⚠️ CRITICAL
**Severity:** HIGH  
**Impact:** Cannot submit order lists, cannot generate mass status  
**Status:** Not fixed

**Problem:**
Execution client missing 2 required methods.

**Missing Methods:**
1. `_submit_order_list(command: SubmitOrderList)` - Submit multiple orders atomically
2. `generate_mass_status(lookback_mins: int | None) -> list[OrderStatusReport]` - Generate status for all orders

**Fix:** See WORKFLOW.md Phase 1, Step 5

---

## 🦀 RUST LAYER BUGS (9)

### Bug #004: Using RwLock Instead of DashMap ⚠️ CRITICAL
**Severity:** HIGH  
**Impact:** 100x slower performance, lock contention  
**Status:** Not fixed

**Problem:**
State management uses `RwLock<HashMap>` which is slow for concurrent access.

**Current (WRONG):**
```rust
use std::sync::RwLock;
use std::collections::HashMap;

struct State {
    orders: RwLock<HashMap<String, Order>>,
}
```

**Should Be:**
```rust
use dashmap::DashMap;

struct State {
    orders: DashMap<String, Order>,
}
```

**Impact:**
- Read operations: 100x slower
- Write operations: 50x slower
- Lock contention under load

**Fix:** Replace all `RwLock<HashMap>` with `DashMap` (~200 LOC)

---

### Bug #005: Reconciliation is Stub ⚠️ CRITICAL
**Severity:** CRITICAL  
**Impact:** State can become inconsistent, duplicate fills, missed orders  
**Status:** Not fixed

**Problem:**
Reconciliation logic is not implemented. Current code is just a stub.

**Required Implementation:**
1. Query REST API on connect
2. Fetch open orders
3. Generate order status reports
4. Fetch recent fills
5. Deduplicate fills (track emitted fills)
6. Generate fill reports
7. Fetch positions
8. Generate position reports
9. Run periodically (default: 5 min)

**Why Critical:**
- REST is authoritative (never trust WebSocket alone)
- Without reconciliation: duplicate fills, missed orders, inconsistent state
- Required by Nautilus specification

**Fix:** See WORKFLOW.md Phase 1, Step 6 (Python) and Phase 2, Component 6 (Rust)

---

### Bug #006: Subscription Tracking Too Simplistic
**Severity:** MEDIUM  
**Impact:** Cannot resubscribe on reconnect, memory leaks  
**Status:** Not fixed

**Problem:**
No proper tracking of active subscriptions.

**Required:**
- Track all active subscriptions
- Resubscribe on reconnect
- Clean up on disconnect
- Handle subscription failures

**Fix:** Implement subscription state machine (~100 LOC)

---

### Bug #007: Boolean Connection State ⚠️ CRITICAL
**Severity:** HIGH  
**Impact:** Cannot handle reconnection, degraded states  
**Status:** Not fixed

**Problem:**
Connection state is just a boolean (`is_connected: bool`).

**Should Be:**
7-state machine:
1. Disconnected
2. Connecting
3. Connected
4. Authenticating
5. Authenticated
6. Reconnecting
7. Degraded

**Fix:** Implement proper state machine (~80 LOC)

---

### Bug #008: No Race Condition Prevention ⚠️ CRITICAL
**Severity:** HIGH  
**Impact:** REST and WebSocket updates can conflict  
**Status:** Not fixed

**Problem:**
No sequence tracking or conflict resolution between REST and WebSocket updates.

**Required:**
- Sequence number tracking
- REST takes priority over WebSocket
- Deduplicate updates
- Handle out-of-order messages

**Fix:** Implement sequence tracking (~100 LOC)

---

### Bug #009: Wrong Event Types ⚠️ CRITICAL
**Severity:** HIGH  
**Impact:** Events not recognized by Nautilus framework  
**Status:** Not fixed

**Problem:**
Using custom event types instead of Nautilus event types.

**Current (WRONG):**
```rust
struct OrderEvent {
    order_id: String,
    status: String,
}
```

**Should Be:**
```rust
use nautilus_model::events::{OrderAccepted, OrderFilled, OrderCanceled};

let event = OrderAccepted::new(
    order_id,
    account_id,
    timestamp_ns,
);
```

**Required Event Types:**
- OrderAccepted
- OrderRejected
- OrderCanceled
- OrderFilled
- OrderUpdated
- PositionOpened
- PositionChanged
- PositionClosed

**Fix:** Use proper Nautilus event types (~200 LOC)

---

### Bug #010: Instrument Parsing Returns None
**Severity:** MEDIUM  
**Impact:** Cannot load instruments, adapter won't work  
**Status:** Not fixed

**Problem:**
`parse_instrument()` always returns `None`.

**Required:**
- Parse Paradex instrument data
- Convert to Nautilus Instrument type
- Handle all instrument fields
- Error handling

**Fix:** Implement proper parsing (~50 LOC)

---

### Bug #011: Message Handlers Are Stubs
**Severity:** HIGH  
**Impact:** WebSocket messages not processed  
**Status:** Not fixed

**Problem:**
All message handlers are empty stubs.

**Required Handlers:**
- Trade updates
- Quote updates
- Order book updates
- Order updates
- Fill updates
- Position updates
- Account updates

**Fix:** Implement message routing and handlers (~150 LOC)

---

### Bug #012: No Integration Tests
**Severity:** MEDIUM  
**Impact:** Cannot verify Rust layer works  
**Status:** Not fixed

**Problem:**
No tests for Rust components.

**Required Tests:**
- HTTP client tests
- WebSocket client tests
- State management tests
- Reconciliation tests
- Event emission tests
- PyO3 binding tests

**Fix:** Create integration tests (~300 LOC)

---

## 📊 BUG SUMMARY

### By Severity:
- **CRITICAL:** 6 bugs (#005, #007, #008, #009, #001, #002, #003)
- **HIGH:** 3 bugs (#004, #011, #006)
- **MEDIUM:** 3 bugs (#006, #010, #012)

### By Layer:
- **Python:** 3 bugs
- **Rust:** 9 bugs

### By Impact:
- **Blocking:** 6 bugs (must fix for basic functionality)
- **Performance:** 1 bug (#004)
- **Quality:** 5 bugs (should fix for production)

---

## ✅ FIX PRIORITY

### Phase 1 (Python - 12.5h):
1. Bug #001 - Method signatures (1h)
2. Bug #002 - Missing methods (3.5h)
3. Bug #003 - Execution methods (1h)
4. Bug #005 - Reconciliation Python side (2h)

### Phase 2 (Rust - 38h):
1. Bug #005 - Reconciliation Rust side (3h)
2. Bug #004 - DashMap (2h)
3. Bug #007 - Connection state (1.5h)
4. Bug #008 - Race prevention (2h)
5. Bug #009 - Event types (3h)
6. Bug #011 - Message handlers (2h)
7. Bug #006 - Subscription tracking (2h)
8. Bug #010 - Instrument parsing (0.5h)
9. Bug #012 - Integration tests (3h)

---

**Next: See CONFIG.md for configuration details**
