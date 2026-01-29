# Race Conditions: REST vs WebSocket

## ✅ YES - This is a REAL Race Condition!

## The Problem

When using **both REST and WebSocket** simultaneously, you get race conditions:

```
T=0ms:   WebSocket: "Order filled at $89,300"
T=50ms:  Update local state: filled = true
T=100ms: REST poll: "Order still open" (stale cache)
T=150ms: Update local state: filled = false  ← WRONG!
```

**Result:** Your state is corrupted. You think order is open, but it's actually filled!

## Real-World Example

### Scenario: Place Order + Monitor Status

```python
# Place order via REST
order_id = await rest.place_order(...)  # T=0ms

# WebSocket receives update
@ws.on_order_update
def on_update(data):
    if data.id == order_id:
        state.orders[order_id] = data  # T=50ms: "FILLED"

# Meanwhile, REST poll happens
orders = await rest.get_orders()  # T=100ms: returns cached "OPEN"
state.orders[order_id] = orders[order_id]  # T=150ms: overwrites with stale data

# Now your state says "OPEN" but order is actually "FILLED"!
```

## Types of REST vs WebSocket Race Conditions

### 1. **Stale Data Overwrite**
```
WebSocket (T=10ms):  Position = 0.01 BTC
REST (T=357ms):      Position = 0 BTC (stale)
Final state:         Position = 0 BTC ← WRONG!
```

### 2. **Order Status Confusion**
```
WebSocket: Order FILLED
REST:      Order OPEN (cached)
Result:    Try to cancel already-filled order → ERROR
```

### 3. **Double Execution**
```
WebSocket: Order filled
Strategy:  Place new order
REST:      Says old order still open
Strategy:  Place ANOTHER order → DOUBLE POSITION!
```

### 4. **Balance Mismatch**
```
WebSocket: Balance = $99,000 (after trade)
REST:      Balance = $100,000 (before trade)
Result:    Think you have more money than you do
```

## Why This Happens

### REST Characteristics
- **Latency:** 357ms
- **Caching:** API may cache responses
- **Polling:** You control when to fetch
- **Snapshot:** Point-in-time data

### WebSocket Characteristics
- **Latency:** 10-50ms
- **Real-time:** Instant push updates
- **Event-driven:** Server controls when to send
- **Stream:** Continuous updates

### The Race
```
T=0ms:    Event happens on exchange
T=10ms:   WebSocket pushes update → You receive it
T=357ms:  REST returns data (from T=0ms) → Stale!
```

## Solutions

### ❌ BAD: Use Both Independently
```python
# WebSocket updates
@ws.on_order
def on_order(data):
    state.orders[data.id] = data

# REST updates (RACE CONDITION!)
orders = await rest.get_orders()
for order in orders:
    state.orders[order.id] = order  # Overwrites WebSocket data!
```

### ✅ GOOD: WebSocket as Source of Truth
```python
# WebSocket is primary
@ws.on_order
def on_order(data):
    state.orders[data.id] = data
    state.last_ws_update = time.now()

# REST only for reconciliation
async def reconcile():
    if time.now() - state.last_ws_update > 60:  # No WS for 60s
        orders = await rest.get_orders()
        state.orders = orders  # Only if WS is dead
```

### ✅ BETTER: Sequence Numbers
```python
@ws.on_order
def on_order(data):
    if data.seq_no > state.orders[data.id].seq_no:
        state.orders[data.id] = data  # Only if newer

async def rest_update():
    orders = await rest.get_orders()
    for order in orders:
        if order.seq_no > state.orders[order.id].seq_no:
            state.orders[order.id] = order  # Only if newer
```

### ✅ BEST: Timestamps + Priority
```python
class StateManager:
    def update_order(self, order, source):
        current = self.orders.get(order.id)
        
        # WebSocket always wins if recent
        if source == "websocket":
            self.orders[order.id] = order
            self.last_ws_time[order.id] = time.now()
        
        # REST only if no recent WebSocket update
        elif source == "rest":
            last_ws = self.last_ws_time.get(order.id, 0)
            if time.now() - last_ws > 5:  # 5 second grace period
                self.orders[order.id] = order
```

## Paradex Adapter Current Status

### What We Tested
✅ **REST concurrent requests** - No race conditions
✅ **Multiple REST clients** - No race conditions

### What We DIDN'T Test
❌ **REST + WebSocket together** - WILL have race conditions!
❌ **State synchronization** - Not implemented
❌ **Sequence number handling** - Not implemented

## The Real Race Condition Test

```python
async def test_rest_ws_race():
    # Start WebSocket
    ws = WebSocketClient()
    await ws.connect()
    
    # Place order via REST
    order_id = await rest.place_order(...)
    
    # Race condition window
    await asyncio.sleep(0.1)  # WebSocket gets update
    
    # Poll REST (stale data)
    rest_orders = await rest.get_orders()
    
    # Check for mismatch
    ws_status = ws.orders[order_id].status
    rest_status = rest_orders[order_id].status
    
    if ws_status != rest_status:
        print("❌ RACE CONDITION DETECTED!")
        print(f"WebSocket: {ws_status}")
        print(f"REST: {rest_status}")
```

## Recommendation for Paradex Adapter

### Current (REST Only)
✅ **No race conditions** - Only one data source
✅ **Safe** - Can't have REST vs WS conflicts
⚠️ **Slow** - 357ms latency

### Adding WebSocket (Future)
⚠️ **MUST implement:**
1. **Source priority** - WebSocket > REST
2. **Timestamp tracking** - Know which data is newer
3. **Grace periods** - Don't overwrite recent WS data
4. **Reconciliation logic** - Periodic verification

### Implementation Pattern
```rust
pub struct StateManager {
    orders: DashMap<String, Order>,
    last_ws_update: DashMap<String, Instant>,
}

impl StateManager {
    pub fn update_from_websocket(&self, order: Order) {
        self.orders.insert(order.id.clone(), order);
        self.last_ws_update.insert(order.id, Instant::now());
    }
    
    pub fn update_from_rest(&self, order: Order) {
        // Only update if no recent WebSocket data
        if let Some(last_ws) = self.last_ws_update.get(&order.id) {
            if last_ws.elapsed() < Duration::from_secs(5) {
                return;  // Skip stale REST data
            }
        }
        self.orders.insert(order.id, order);
    }
}
```

## Summary

### What We Tested
✅ REST concurrent requests (no race conditions)
✅ REST vs REST (no race conditions)

### What We Missed
❌ **REST vs WebSocket race conditions** - This is the REAL issue!

### The Truth
- **REST-only:** Safe, no race conditions ✅
- **WebSocket-only:** Safe, no race conditions ✅
- **REST + WebSocket:** RACE CONDITIONS! ⚠️

### Solution
When adding WebSocket:
1. Make WebSocket the source of truth
2. Use REST only for commands and reconciliation
3. Implement timestamp/sequence number checking
4. Add grace periods to prevent stale overwrites

**Current Status:** Safe (REST-only), but need careful design when adding WebSocket!
