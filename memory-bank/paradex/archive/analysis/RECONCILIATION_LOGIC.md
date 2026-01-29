# RECONCILIATION LOGIC - CRITICAL REQUIREMENT

**Date:** 2026-01-27  
**Priority:** CRITICAL  
**Status:** Must be implemented in Phase 1

---

## 🚨 WHY RECONCILIATION IS CRITICAL

### The Problem:
- WebSocket connections can drop
- Messages can be missed
- State can desync between client and exchange
- Orders/fills can be lost during reconnection

### The Solution:
**REST-Authoritative Reconciliation**
- REST API is the source of truth
- WebSocket provides hints only
- Reconcile state on EVERY connect/reconnect
- Periodic reconciliation (every 5 minutes)

---

## 📋 RECONCILIATION REQUIREMENTS

### 1. On Connect (MANDATORY)
```python
async def _connect(self) -> None:
    # 1. Initialize instruments
    await self._instrument_provider.initialize()
    
    # 2. MANDATORY: Reconcile state from REST
    await self._reconcile_state()
    
    # 3. Start periodic reconciliation
    self._reconcile_task = asyncio.create_task(self._run_reconciliation_loop())
    
    # 4. Connect WebSocket
    await self._ws_client.connect(...)
```

### 2. Reconcile State Method
```python
async def _reconcile_state(self) -> None:
    """
    Reconcile orders, fills, and positions from REST API.
    
    This is the authoritative source of truth.
    WebSocket is for real-time hints only.
    """
    self._log.info("Reconciling state from REST API...")
    
    # Query REST for current state
    orders = await self._http_client.get_open_orders()
    fills = await self._http_client.get_recent_fills()
    positions = await self._http_client.get_positions()
    
    # Generate order status reports
    for order in orders:
        report = self._parse_order_status_report(order)
        self.generate_order_status_report(report)
    
    # Generate fill reports (with deduplication)
    for fill in fills:
        trade_id = TradeId(fill.trade_id)
        if trade_id not in self._emitted_fills:
            report = self._parse_fill_report(fill)
            self.generate_fill_report(report)
            self._emitted_fills.add(trade_id)
    
    # Generate position reports
    for position in positions:
        report = self._parse_position_report(position)
        self.generate_position_status_report(report)
    
    self._log.info(f"Reconciliation complete: {len(orders)} orders, {len(fills)} fills, {len(positions)} positions")
```

### 3. Periodic Reconciliation Loop
```python
async def _run_reconciliation_loop(self) -> None:
    """
    Periodic reconciliation to catch any missed updates.
    
    Default: Every 5 minutes
    Configurable via: reconcile_interval_secs
    """
    while True:
        try:
            await asyncio.sleep(self._config.reconcile_interval_secs)
            await self._reconcile_state()
        except asyncio.CancelledError:
            self._log.info("Reconciliation loop cancelled")
            break
        except Exception as e:
            self._log.error(f"Error in reconciliation loop: {e}")
```

### 4. Fill Deduplication
```python
class ParadexExecutionClient(LiveExecutionClient):
    def __init__(self, ...):
        super().__init__(...)
        
        # Track emitted fills to prevent duplicates
        self._emitted_fills: set[TradeId] = set()
    
    def _handle_fill(self, fill_data):
        """Handle fill from WebSocket or REST."""
        trade_id = TradeId(fill_data.trade_id)
        
        # Check if already emitted
        if trade_id in self._emitted_fills:
            self._log.debug(f"Skipping duplicate fill: {trade_id}")
            return
        
        # Generate fill report
        report = self._parse_fill_report(fill_data)
        self.generate_fill_report(report)
        
        # Track as emitted
        self._emitted_fills.add(trade_id)
```

---

## ✅ IMPLEMENTATION CHECKLIST

### Required Components:

- [ ] `self._emitted_fills: set[TradeId]` - Track emitted fills
- [ ] `self._reconcile_task: asyncio.Task | None` - Reconciliation task handle
- [ ] `async def _reconcile_state(self) -> None` - Main reconciliation method
- [ ] `async def _run_reconciliation_loop(self) -> None` - Periodic loop
- [ ] Call `await self._reconcile_state()` in `_connect()`
- [ ] Start reconciliation loop in `_connect()`
- [ ] Cancel reconciliation task in `_disconnect()`
- [ ] Deduplicate fills in all fill handlers

### Configuration:

```python
# config.py
class ParadexExecClientConfig(LiveExecClientConfig):
    reconcile_interval_secs: float = 300.0  # 5 minutes default
```

---

## 🎯 PATTERNS FROM OKX ADAPTER

### OKX Implementation (Reference):
```python
# From OKX execution.py
async def _connect(self) -> None:
    await self._instrument_provider.initialize()
    await self._cache_instruments()
    await self._update_account_state()
    await self._await_account_registered()
    
    # Connect WebSocket
    await self._ws_client.connect(...)
    
    # Note: OKX doesn't show explicit reconciliation in public code
    # but the pattern is the same: query REST on connect
```

### Paradex Should Implement:
```python
async def _connect(self) -> None:
    # 1. Initialize
    await self._instrument_provider.initialize()
    
    # 2. RECONCILE (MANDATORY)
    await self._reconcile_state()
    self._reconcile_task = asyncio.create_task(self._run_reconciliation_loop())
    
    # 3. Connect WebSocket
    await self._ws_client.connect(...)
    
    # 4. Subscribe to channels
    await self._ws_client.subscribe_orders()
    await self._ws_client.subscribe_fills()
```

---

## 🚨 COMMON MISTAKES

### ❌ DON'T:
- Skip reconciliation on connect
- Trust WebSocket as source of truth
- Forget fill deduplication
- Ignore periodic reconciliation
- Clear `_emitted_fills` on reconnect

### ✅ DO:
- Reconcile on EVERY connect
- Query REST as authoritative source
- Track all emitted fills
- Run periodic reconciliation
- Keep `_emitted_fills` across reconnects

---

## 📊 VALIDATION

### How to Test Reconciliation:

1. **Connect Test:**
   ```python
   # Should reconcile on connect
   client = ParadexExecutionClient(...)
   await client.connect()
   # Verify: _reconcile_state() was called
   # Verify: _reconcile_task is running
   ```

2. **Deduplication Test:**
   ```python
   # Should not emit duplicate fills
   fill_data = {...}
   client._handle_fill(fill_data)  # First time - should emit
   client._handle_fill(fill_data)  # Second time - should skip
   # Verify: Only one fill report generated
   ```

3. **Periodic Test:**
   ```python
   # Should reconcile periodically
   await asyncio.sleep(reconcile_interval_secs + 1)
   # Verify: _reconcile_state() called again
   ```

---

## 📚 REFERENCES

### Documentation:
- **memory-bank/2_PYTHON_ADAPTER_IMPLEMENTATION.md** - Pattern #1
- **memory-bank/execution.py** - Lines 202-220 (reference implementation)
- **memory-bank/AGENTS.md** - Line 116 (REST is authoritative)

### Key Concepts:
- **REST-Authoritative:** REST API is source of truth
- **Idempotent:** Safe to call multiple times
- **Deduplication:** Prevent duplicate fills
- **Periodic:** Regular reconciliation (5 min default)

---

## 🎯 IMPLEMENTATION PRIORITY

**Phase:** 1 (Python Layer)  
**Task:** 6 (After fixing methods)  
**Priority:** CRITICAL  
**Time:** 1-2 hours  
**LOC:** ~50-100

**Must be implemented before:**
- Rust layer
- Production deployment
- Live trading

**Why:** Without reconciliation, state can desync and orders/fills can be lost.

---

**RECONCILIATION IS NOT OPTIONAL**  
**IT IS A CRITICAL REQUIREMENT**  
**IMPLEMENT IN PHASE 1**
