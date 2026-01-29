# WORKFLOW - IMPLEMENTATION GUIDE

**Purpose:** Step-by-step implementation with validation and refactoring

---

## 🎯 OVERVIEW

**Total Time:** 68 hours  
**Total Credits:** 1,100-1,400  
**Approach:** Implementation → Refactoring → Testing → Validation

---

## 📋 PHASE 0: SETUP (5 minutes)

### Install Nautilus Trader
```bash
# Install Nautilus Trader via pip
pip install nautilus_trader

# Verify installation
python -c "import nautilus_trader; print(f'Nautilus Trader {nautilus_trader.__version__} installed')"
```

---

## 📋 PHASE 1: PYTHON LAYER (12.5 hours, 200-250 credits)

### Prerequisites
```bash
# 1. Backup existing files
cd /home/mok/projects/nautilus-dinger
cp nautilus_trader/adapters/paradex/data.py nautilus_trader/adapters/paradex/data.py.backup
cp nautilus_trader/adapters/paradex/execution.py nautilus_trader/adapters/paradex/execution.py.backup

# 2. Fetch OKX reference code
# Visit: https://github.com/nautechsystems/nautilus_trader/tree/develop/nautilus_trader/adapters/okx
# Download: data.py, execution.py
```

### Step 1: Fix Method Signatures (1h)
**Bug #001: 6 methods have wrong signatures**

```python
# WRONG (current):
async def _subscribe_trade_ticks(self, instrument_id: InstrumentId) -> None:

# CORRECT (should be):
async def _subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
    instrument_id = command.instrument_id
```

**Fix these 6 methods:**
1. `_subscribe_trade_ticks`
2. `_subscribe_quote_ticks`
3. `_subscribe_order_book_deltas`
4. `_subscribe_order_book_snapshots`
5. `_unsubscribe_trade_ticks`
6. `_unsubscribe_quote_ticks`

**Validation:**
```bash
python -m py_compile nautilus_trader/adapters/paradex/data.py
# Expected: No errors
```

### Step 2: Add Base Methods (0.5h)
**Bug #002 (partial): Missing 3 base methods**

```python
async def _subscribe(self, data_type: DataType) -> None:
    """Subscribe to generic data type."""
    self._log.warning(f"Generic subscription not supported: {data_type}")

async def _unsubscribe(self, data_type: DataType) -> None:
    """Unsubscribe from generic data type."""
    self._log.warning(f"Generic unsubscription not supported: {data_type}")

async def _request(self, data_type: DataType, correlation_id: UUID4) -> None:
    """Request generic data type."""
    self._log.warning(f"Generic request not supported: {data_type}")
```

**Validation:**
```bash
python -c "from nautilus_trader.adapters.paradex.data import ParadexDataClient; print('OK')"
```

### Step 3: Add Subscription Methods (2h)
**Bug #002 (continued): Missing 16 subscription methods**

Add these methods (copy pattern from OKX):
1. `_subscribe_bars`
2. `_subscribe_instrument_status`
3. `_subscribe_instrument_close`
4. `_subscribe_mark_price`
5. `_subscribe_funding_rate`
6. `_subscribe_index_price`
7. `_subscribe_open_interest`
8. `_subscribe_liquidations`
9. `_unsubscribe_bars`
10. `_unsubscribe_order_book_deltas`
11. `_unsubscribe_order_book_snapshots`
12. `_unsubscribe_instrument_status`
13. `_unsubscribe_instrument_close`
14. `_unsubscribe_mark_price`
15. `_unsubscribe_funding_rate`
16. `_unsubscribe_index_price`

**Pattern:**
```python
async def _subscribe_bars(self, command: SubscribeBars) -> None:
    """Subscribe to bar updates."""
    pyo3_bar_type = nautilus_pyo3.BarType.from_str(command.bar_type.value)
    await self._ws_client.subscribe_bars(pyo3_bar_type)
    self._log.info(f"Subscribed to bars: {command.bar_type}")
```

**Validation:**
```bash
python -c "
from nautilus_trader.adapters.paradex.data import ParadexDataClient
import inspect
methods = [m for m in dir(ParadexDataClient) if m.startswith('_subscribe') or m.startswith('_unsubscribe')]
print(f'Found {len(methods)} subscription methods')
"
# Expected: 22+ methods
```

### Step 4: Add Request Methods (1h)
**Bug #002 (continued): Missing 7 request methods**

Add these methods:
1. `_request_quote_ticks`
2. `_request_trade_ticks`
3. `_request_bars`
4. `_request_instrument`
5. `_request_instruments`
6. `_request_order_book_snapshot`
7. `_request_data`

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
```

**Validation:**
```bash
python -c "
from nautilus_trader.adapters.paradex.data import ParadexDataClient
import inspect
methods = [m for m in dir(ParadexDataClient) if m.startswith('_request')]
print(f'Found {len(methods)} request methods')
"
# Expected: 8+ methods
```

### Step 5: Fix Execution Client (1h)
**Bug #003: Missing 2 execution methods**

Add to `execution.py`:

```python
async def _submit_order_list(self, command: SubmitOrderList) -> None:
    """Submit a list of orders atomically."""
    self._log.info(f"Submitting order list: {len(command.order_list.orders)} orders")
    
    for order in command.order_list.orders:
        await self._submit_order(SubmitOrder(
            trader_id=command.trader_id,
            strategy_id=command.strategy_id,
            order=order,
            command_id=command.id,
            ts_init=command.ts_init,
        ))

def generate_mass_status(
    self,
    lookback_mins: int | None = None,
) -> list[OrderStatusReport]:
    """Generate mass order status reports."""
    reports = []
    for order_id, order_state in self._order_states.items():
        report = OrderStatusReport(
            account_id=self.account_id,
            instrument_id=order_state.instrument_id,
            client_order_id=order_id,
            order_status=order_state.status,
            # ... other fields
        )
        reports.append(report)
    return reports
```

**Validation:**
```bash
python -c "
from nautilus_trader.adapters.paradex.execution import ParadexExecutionClient
assert hasattr(ParadexExecutionClient, '_submit_order_list')
assert hasattr(ParadexExecutionClient, 'generate_mass_status')
print('OK')
"
```

### Step 6: Implement Reconciliation (2h) ⭐ CRITICAL
**Bug #005: Reconciliation is stub**

```python
async def _reconcile_state(self) -> None:
    """Reconcile state from REST API (REST is authoritative)."""
    self._log.info("Starting state reconciliation...")
    
    # 1. Fetch open orders from REST
    open_orders = await self._http_client.get_open_orders()
    
    # 2. Generate order status reports
    for order_data in open_orders:
        report = self._parse_order_status_report(order_data)
        self._send_order_status_report(report)
    
    # 3. Fetch recent fills
    fills = await self._http_client.get_fills(
        start_time=self._last_reconcile_time
    )
    
    # 4. Generate fill reports (deduplicated)
    for fill_data in fills:
        trade_id = TradeId(fill_data["trade_id"])
        if trade_id not in self._emitted_fills:
            report = self._parse_fill_report(fill_data)
            self._send_fill_report(report)
            self._emitted_fills.add(trade_id)
    
    # 5. Fetch positions
    positions = await self._http_client.get_positions()
    
    # 6. Generate position reports
    for position_data in positions:
        report = self._parse_position_report(position_data)
        self._send_position_status_report(report)
    
    self._last_reconcile_time = self._clock.timestamp_ns()
    self._log.info("State reconciliation complete")

async def _run_reconciliation_loop(self) -> None:
    """Run periodic reconciliation."""
    while self._is_connected:
        await asyncio.sleep(self._config.reconcile_interval_secs)
        try:
            await self._reconcile_state()
        except Exception as e:
            self._log.error(f"Reconciliation failed: {e}")
```

**Validation:**
```bash
python -c "
from nautilus_trader.adapters.paradex.execution import ParadexExecutionClient
import inspect
source = inspect.getsource(ParadexExecutionClient._reconcile_state)
assert 'get_open_orders' in source
assert 'get_fills' in source
assert '_emitted_fills' in source
print('Reconciliation implemented correctly')
"
```

### Step 7: Refactor & Cleanup (1.5h)

**Extract helper methods:**
```python
def _to_pyo3_instrument_id(self, instrument_id: InstrumentId) -> nautilus_pyo3.InstrumentId:
    """Convert Nautilus InstrumentId to PyO3 type."""
    return nautilus_pyo3.InstrumentId.from_str(instrument_id.value)

def _to_pyo3_bar_type(self, bar_type: BarType) -> nautilus_pyo3.BarType:
    """Convert Nautilus BarType to PyO3 type."""
    return nautilus_pyo3.BarType.from_str(bar_type.value)
```

**Remove duplicates, improve names, add docstrings**

**Validation:**
```bash
pylint nautilus_trader/adapters/paradex/data.py --disable=C0111,R0913
pylint nautilus_trader/adapters/paradex/execution.py --disable=C0111,R0913
# Expected: Score > 7.0
```

### Step 8: Unit Tests (1.5h)

Create `tests/unit/adapters/paradex/test_data_client.py`:
```python
import pytest
from unittest.mock import Mock, AsyncMock
from nautilus_trader.adapters.paradex.data import ParadexDataClient

@pytest.fixture
def data_client():
    # Create minimal client for testing
    pass

def test_subscribe_trade_ticks_signature():
    """Test correct method signature."""
    pass

def test_subscribe_calls_ws_client():
    """Test WebSocket client is called."""
    pass

# Add 15-20 more tests...
```

**Validation:**
```bash
pytest tests/unit/adapters/paradex/ -v --cov=nautilus_trader/adapters/paradex
# Expected: >85% coverage
```

### Step 9: Integration Tests (1h)

Create `tests/integration/adapters/paradex/test_integration.py`:
```python
@pytest.mark.asyncio
async def test_connection_lifecycle():
    """Test connect/disconnect flow."""
    pass

@pytest.mark.asyncio
async def test_reconciliation_on_connect():
    """Test reconciliation runs on connect."""
    pass
```

**Validation:**
```bash
pytest tests/integration/adapters/paradex/ -v
# Expected: All pass
```

### Step 10: Final Validation (0.5h)

```bash
# Full test suite
pytest tests/ -v --cov=nautilus_trader/adapters/paradex --cov-report=html

# Method count check
python -c "
from nautilus_trader.adapters.paradex.data import ParadexDataClient
from nautilus_trader.adapters.paradex.execution import ParadexExecutionClient
data_methods = len([m for m in dir(ParadexDataClient) if not m.startswith('__')])
exec_methods = len([m for m in dir(ParadexExecutionClient) if not m.startswith('__')])
print(f'Data methods: {data_methods} (need 38+)')
print(f'Execution methods: {exec_methods} (need 12+)')
"
```

### ✅ Phase 1 Complete When:
- [ ] All 38 data methods implemented
- [ ] All 12 execution methods implemented
- [ ] Reconciliation working
- [ ] Code refactored
- [ ] Tests passing (85%+ coverage)
- [ ] No syntax errors

---

## 📋 PHASE 2: RUST CORE (38 hours, 650-800 credits)

### Overview
Implement missing Rust components (~2,400 LOC)

### Components to Implement:

**1. HTTP Client (4h, ~500 LOC)**
- JWT authentication
- Request/response handling
- Error handling
- Rate limiting

**2. WebSocket Client (4h, ~400 LOC)**
- JSON-RPC protocol
- Connection management
- Message routing
- Reconnection logic

**3. STARK Signing (3h, ~200 LOC)**
- StarkNet signature generation
- Order signing
- Subkey management

**4. PyO3 Bindings (3h, ~300 LOC)**
- Expose Rust to Python
- Type conversions
- Error handling

**5. State Management (2h, ~200 LOC)**
- Replace RwLock with DashMap
- Thread-safe access
- Performance optimization

**6. Reconciliation Logic (3h, ~150 LOC)**
- REST query on connect
- Event generation
- State synchronization

**7. Subscription Tracking (2h, ~100 LOC)**
- Track active subscriptions
- Handle resubscription
- Cleanup on disconnect

**8. Connection State Machine (1.5h, ~80 LOC)**
- 7 states: Disconnected/Connecting/Connected/Authenticating/Authenticated/Reconnecting/Degraded
- State transitions
- Event emission

**9. Race Prevention (2h, ~100 LOC)**
- Sequence number tracking
- Order deduplication
- REST vs WebSocket priority

**10. Event Emission (3h, ~200 LOC)**
- Use proper Nautilus event types
- OrderAccepted, OrderFilled, etc.
- Correct field mapping

**11. Message Routing (2h, ~150 LOC)**
- Parse incoming messages
- Route to handlers
- Error handling

**12. Refactor & Cleanup (3h)**
- Code review
- Performance optimization
- Documentation

**13. Integration Tests (3h, ~300 LOC)**
- Test HTTP client
- Test WebSocket client
- Test state management
- Test reconciliation

**14. Validation (2.5h)**
- Performance benchmarks
- Memory leak checks
- Thread safety verification

### ✅ Phase 2 Complete When:
- [ ] All Rust components implemented
- [ ] PyO3 bindings working
- [ ] Integration tests passing
- [ ] Performance benchmarks met
- [ ] No race conditions
- [ ] Code refactored

---

## 📋 PHASE 3: TESTING (14 hours, 180-250 credits)

### Tasks:
1. Comprehensive unit tests (2h)
2. Integration tests (2h)
3. Rust integration tests (2h)
4. End-to-end testing (2h)
5. Bug fixes (3h)
6. Performance optimization (2h)
7. Final validation (1h)

### ✅ Phase 3 Complete When:
- [ ] 90%+ test coverage
- [ ] All tests passing
- [ ] Performance optimized
- [ ] No known bugs
- [ ] Production validation passed

---

## 📋 PHASE 4: DOCUMENTATION (3.5 hours, 40-60 credits)

### Tasks:
1. Update documentation (1h)
2. Create usage examples (1h)
3. Code review (1h)
4. Final validation (0.5h)

### ✅ Phase 4 Complete When:
- [ ] Documentation complete
- [ ] Examples working
- [ ] Code reviewed
- [ ] Production ready

---

## 📊 PROGRESS TRACKING

Update after each phase:
```bash
# Update progress
vim tracking/progress.md

# Log bugs fixed
vim tracking/bug-fixes-record.md

# Log improvements
vim tracking/improvements-log.md

# Save validation results
vim tracking/validation-results.md
```

---

## 💡 TIPS

1. **Validate frequently** - After every change
2. **Use existing code** - Copy from OKX adapter
3. **Test as you go** - Don't wait until end
4. **Document everything** - Track all changes
5. **Follow patterns** - Use proven Nautilus patterns

---

**Next: See PATTERNS.md for code examples**
