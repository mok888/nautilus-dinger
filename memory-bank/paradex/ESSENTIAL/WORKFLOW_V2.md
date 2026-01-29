# WORKFLOW V2 - IMPROVED IMPLEMENTATION GUIDE

**Version:** 2.0 (Dependency-Aware, Critical Path Optimized)  
**Total Time:** 85.5 hours (was 68h)  
**Total Credits:** 1,400-1,700 (was 1,100-1,400)  
**Approach:** Plan → Foundation → Parallel → Validate → Integrate

---

## 🚀 PREREQUISITES

### Install Nautilus Trader
```bash
# Install Nautilus Trader via pip
pip install nautilus_trader

# Verify installation
python -c "import nautilus_trader; print(f'Nautilus Trader {nautilus_trader.__version__} installed')"
```

---

## 🎯 CRITICAL PATH OVERVIEW

```
Phase 0: Preparation (6h)
  ↓
Phase 0.5: Mock Infrastructure (3h)
  ↓
Phase 1: Python Foundation (12.5h)
  ├─ CRITICAL PATH: Reconciliation (3h) ⭐ BLOCKING
  ├─ CRITICAL PATH: Method Signatures (1h) ⭐ BLOCKING
  └─ PARALLEL: Other methods (8.5h)
  ↓
Phase 1.5: Integration Sandbox (4h)
  ↓
Phase 2: Rust Core (38h)
  ├─ CRITICAL: PyO3 bindings (3h) ⭐ BLOCKING
  ├─ CRITICAL: State management (2h) ⭐ BLOCKING
  └─ PARALLEL: Other components (33h)
  ↓
Phase 2.1: Performance Baseline (3h)
  ↓
Phase 3: Full Testing (17h)
  ↓
Phase 4: Documentation Review (2h)
```

---

## 📋 PHASE 0: PREPARATION (6 hours)

### Part A: Dependency Analysis (2h) ⭐ NEW

**Purpose:** Understand task dependencies before coding

**Tasks:**
1. **Map Component Dependencies (45 min)**
   ```bash
   # Create dependency graph
   vim memory-bank/tracking/dependency-graph.md
   ```
   
   Document:
   - Python methods that depend on Rust components
   - Rust components that depend on each other
   - Blocking vs parallelizable tasks

2. **Identify Critical Path (30 min)**
   - Reconciliation (blocks everything)
   - PyO3 bindings (blocks Python-Rust integration)
   - State management (blocks event emission)

3. **Risk Assessment (45 min)**
   - STARK signing complexity (HIGH RISK)
   - WebSocket reconnection logic (MEDIUM RISK)
   - Fill deduplication (MEDIUM RISK)
   - Performance targets (LOW RISK)

**Deliverable:** `tracking/dependency-graph.md`

**Validation:**
```bash
# Check all dependencies documented
cat tracking/dependency-graph.md | grep "BLOCKS:"
# Expected: 5-7 blocking dependencies identified
```

---

### Part B: Exploration & Learning (4h) ⭐ NEW

**Purpose:** Discover Paradex API quirks before implementation

**Tasks:**
1. **Test Real API (1.5h)**
   ```python
   # Create exploration script
   import requests
   import asyncio
   import websockets
   
   # Test HTTP endpoints
   response = requests.get("https://api.testnet.paradex.trade/v1/markets")
   print(response.json())
   
   # Test WebSocket
   async def test_ws():
       async with websockets.connect("wss://ws.testnet.paradex.trade/v1") as ws:
           # Subscribe to trades
           await ws.send('{"method":"subscribe","params":["trades.BTC-USD-PERP"]}')
           msg = await ws.recv()
           print(msg)
   
   asyncio.run(test_ws())
   ```

2. **Test STARK Signing (1h)**
   ```python
   # Experiment with starknet-crypto
   from starknet_crypto import sign
   # Document exact signature format required
   ```

3. **Document API Quirks (1h)**
   - Timestamp format (ms vs ns)
   - WebSocket message format
   - Order status values
   - Error response format

4. **Create Minimal POC (0.5h)**
   ```python
   # Proof of concept: Submit one order end-to-end
   # Save as: exploration/minimal_poc.py
   ```

**Deliverable:** `exploration/notes.md`, `exploration/minimal_poc.py`

**Validation:**
```bash
python exploration/minimal_poc.py
# Expected: Successfully submit and receive order confirmation
```

---

## 📋 PHASE 0.5: MOCK INFRASTRUCTURE (3 hours) ⭐ NEW

**Purpose:** Enable offline development and deterministic testing

**Tasks:**
1. **Create Mock Package (1h)**
   ```bash
   mkdir -p tests/mocks/paradex_mock
   ```
   
   ```python
   # tests/mocks/paradex_mock/http_server.py
   from flask import Flask, jsonify
   
   app = Flask(__name__)
   
   @app.route('/v1/markets')
   def get_markets():
       return jsonify([
           {"market": "BTC-USD-PERP", "status": "active"},
           {"market": "ETH-USD-PERP", "status": "active"},
       ])
   
   @app.route('/v1/orders', methods=['POST'])
   def submit_order():
       return jsonify({
           "id": "mock-order-123",
           "status": "PENDING",
       })
   ```

2. **Mock WebSocket Server (1h)**
   ```python
   # tests/mocks/paradex_mock/ws_server.py
   import asyncio
   import websockets
   import json
   
   async def handler(websocket):
       async for message in websocket:
           data = json.loads(message)
           if data["method"] == "subscribe":
               # Send mock trade
               await websocket.send(json.dumps({
                   "channel": "trades",
                   "data": {"price": "50000", "size": "0.1"}
               }))
   ```

3. **Record Real Responses (0.5h)**
   ```bash
   # Capture real API responses as fixtures
   curl https://api.testnet.paradex.trade/v1/markets > tests/fixtures/markets.json
   ```

4. **Integration (0.5h)**
   ```python
   # tests/conftest.py
   import pytest
   from tests.mocks.paradex_mock import start_mock_server
   
   @pytest.fixture
   def mock_paradex():
       server = start_mock_server()
       yield server
       server.stop()
   ```

**Deliverable:** `tests/mocks/paradex_mock/`

**Validation:**
```bash
# Start mock server
python tests/mocks/paradex_mock/http_server.py &
curl http://localhost:5000/v1/markets
# Expected: Mock market data returned
```

---

## 📋 PHASE 1: PYTHON LAYER (12.5 hours, REORGANIZED)

### 🔴 CRITICAL PATH (Must Complete First)

#### Step 0: Reconciliation Foundation (3h) ⭐ MOVED EARLIER, BLOCKING

**Why First:** Everything depends on solid reconciliation

**Tasks:**
1. **Implement Reconciliation Skeleton (1h)**
   ```python
   async def _reconcile_state(self) -> None:
       """Reconcile state from REST API (REST is authoritative)."""
       self._log.info("Starting reconciliation...")
       
       # 1. Fetch open orders
       open_orders = await self._http_client.get_open_orders()
       for order_data in open_orders:
           report = self._parse_order_status_report(order_data)
           self._send_order_status_report(report)
       
       # 2. Fetch fills (deduplicated)
       fills = await self._http_client.get_fills(
           start_time=self._last_reconcile_time
       )
       for fill_data in fills:
           trade_id = TradeId(fill_data["trade_id"])
           if trade_id not in self._emitted_fills:
               report = self._parse_fill_report(fill_data)
               self._send_fill_report(report)
               self._emitted_fills.add(trade_id)
       
       # 3. Fetch positions
       positions = await self._http_client.get_positions()
       for position_data in positions:
           report = self._parse_position_report(position_data)
           self._send_position_status_report(report)
       
       self._last_reconcile_time = self._clock.timestamp_ns()
   ```

2. **Add Fill Deduplication (0.5h)**
   ```python
   def __init__(self, ...):
       self._emitted_fills: set[TradeId] = set()
   ```

3. **Write Reconciliation Tests FIRST (1h, TDD)**
   ```python
   # tests/unit/test_reconciliation.py
   @pytest.mark.asyncio
   async def test_reconciliation_deduplicates_fills():
       """Test that duplicate fills are not emitted."""
       client = create_test_client()
       
       # Mock REST returns same fill twice
       mock_fills = [
           {"trade_id": "fill-123", "size": "0.1"},
           {"trade_id": "fill-123", "size": "0.1"},  # Duplicate
       ]
       
       await client._reconcile_state()
       
       # Should only emit once
       assert len(client._emitted_fills) == 1
   ```

4. **Validate with Mock (0.5h)**
   ```bash
   pytest tests/unit/test_reconciliation.py -v
   # Expected: All reconciliation tests pass
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
print('✅ Reconciliation foundation complete')
"
```

---

#### Step 1: Fix Method Signatures (1h) ⭐ BLOCKING

**Why Critical:** Framework won't call methods with wrong signatures

**Tasks:**
Fix 6 methods:
```python
# BEFORE (WRONG):
async def _subscribe_trade_ticks(self, instrument_id: InstrumentId) -> None:

# AFTER (CORRECT):
async def _subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
    instrument_id = command.instrument_id
```

**Incremental Validation:**
```bash
# After EACH method fix:
python -m py_compile nautilus_trader/adapters/paradex/data.py
python tests/validation/validate_signatures.py --method _subscribe_trade_ticks
```

---

### 🟢 PARALLEL TRACK (Can Run Alongside Critical Path)

#### Step 2: Add Base Methods (0.5h)
```python
async def _subscribe(self, data_type: DataType) -> None:
    self._log.warning(f"Generic subscription not supported: {data_type}")
```

**Validation:** `python -c "from nautilus_trader.adapters.paradex.data import ParadexDataClient; print('OK')"`

---

#### Step 3: Add Subscription Methods (2h)
16 methods, validate after each group:
```bash
# After quote/trade subscriptions:
pytest tests/unit/test_data_client.py::test_subscribe_quotes -v

# After order book subscriptions:
pytest tests/unit/test_data_client.py::test_subscribe_orderbook -v

# After market data subscriptions:
pytest tests/unit/test_data_client.py::test_subscribe_bars -v
```

---

#### Step 4: Add Request Methods (1h)
7 methods, validate incrementally

---

### 🔵 DEPENDENT ON CRITICAL PATH

#### Step 5: Fix Execution Client (1h)
Depends on reconciliation being complete

#### Steps 6-10: Refactor/Tests/Validation (4.5h)
Standard workflow

---

## 📋 PHASE 1.5: INTEGRATION SANDBOX (4 hours) ⭐ NEW

**Purpose:** Test Python↔Rust integration before full system tests

**Tasks:**
1. **Isolated PyO3 Binding Tests (1h)**
   ```python
   # tests/sandbox/test_pyo3_bindings.py
   def test_python_can_call_rust_http_client():
       from nautilus_trader.adapters.paradex import ParadexHttpClient
       client = ParadexHttpClient(config)
       # Should not crash
       assert client is not None
   ```

2. **Mock-Based Integration Tests (1.5h)**
   ```python
   @pytest.mark.asyncio
   async def test_full_order_flow_with_mocks(mock_paradex):
       """Test complete order submission flow with mock server."""
       # Python → Rust → Mock HTTP → Rust → Python
       client = ParadexExecutionClient(...)
       await client.connect()
       
       order = create_test_order()
       await client.submit_order(order)
       
       # Verify order reached mock server
       assert mock_paradex.received_order(order.client_order_id)
   ```

3. **Reconciliation Dry Run (1h)**
   ```python
   async def test_reconciliation_with_mock_data():
       """Test reconciliation with realistic mock data."""
       # Load recorded API responses
       mock_orders = load_fixture("open_orders.json")
       mock_fills = load_fixture("fills.json")
       
       await client._reconcile_state()
       
       # Verify correct events emitted
       assert len(emitted_events) == expected_count
   ```

4. **Event Pipeline Test (0.5h)**
   ```python
   def test_event_emission_pipeline():
       """Verify events flow from Rust to Python correctly."""
       # Rust emits OrderAccepted → Python receives it
   ```

**Deliverable:** `tests/sandbox/`, `tracking/sandbox-results.md`

**Validation:**
```bash
pytest tests/sandbox/ -v --tb=short
# Expected: All sandbox tests pass
```

---

## 📋 PHASE 2: RUST CORE (38 hours, WITH INCREMENTAL VALIDATION)

### Component-by-Component with Immediate Validation

**Pattern for Each Component:**
1. Implement component
2. Write unit tests
3. Run tests immediately
4. Fix bugs before moving on

**Example:**
```bash
# Implement HTTP client
vim src/http/client.rs

# Write tests
vim src/http/tests.rs

# Test immediately
cargo test --package paradex --lib http::tests

# If fails, fix before continuing
```

### Components (same as before, but validated incrementally):
1. HTTP client (4h) → `cargo test http::tests`
2. WebSocket client (4h) → `cargo test websocket::tests`
3. STARK signing (3h) → `cargo test signing::tests`
4. PyO3 bindings (3h) → `pytest tests/sandbox/test_pyo3.py`
5. State management (2h) → `cargo test state::tests`
6-11. Other components...

---

## 📋 PHASE 2.1: PERFORMANCE BASELINE (3 hours) ⭐ NEW

**Purpose:** Validate "100x faster" claim and set concrete targets

**Tasks:**
1. **Benchmark DashMap vs RwLock (1h)**
   ```rust
   // benches/state_access.rs
   use criterion::{black_box, criterion_group, criterion_main, Criterion};
   
   fn bench_dashmap_read(c: &mut Criterion) {
       let map = DashMap::new();
       map.insert("key", "value");
       
       c.bench_function("dashmap_read", |b| {
           b.iter(|| map.get(black_box("key")))
       });
   }
   
   fn bench_rwlock_read(c: &mut Criterion) {
       let map = RwLock::new(HashMap::new());
       map.write().unwrap().insert("key", "value");
       
       c.bench_function("rwlock_read", |b| {
           b.iter(|| map.read().unwrap().get(black_box("key")))
       });
   }
   ```
   
   ```bash
   cargo bench
   # Expected: DashMap 50-100x faster
   ```

2. **Benchmark HTTP Client (0.5h)**
   ```bash
   # Measure requests/second
   cargo run --release --bin benchmark_http
   # Target: >1000 req/s
   ```

3. **Benchmark WebSocket (0.5h)**
   ```bash
   # Measure message parse time
   cargo run --release --bin benchmark_ws
   # Target: <5ms per message (95th percentile)
   ```

4. **Profile Memory Usage (0.5h)**
   ```bash
   valgrind --tool=massif target/release/paradex_adapter
   # Target: <500MB idle, <2GB peak
   ```

5. **Document Baselines (0.5h)**
   ```markdown
   # tracking/performance-benchmarks.md
   
   ## Baseline Results (2026-01-27)
   - DashMap read: 12ns (vs RwLock: 1,200ns) → 100x faster ✅
   - HTTP throughput: 1,500 req/s ✅
   - WebSocket parse: 3.2ms (p95) ✅
   - Memory idle: 320MB ✅
   - Memory peak: 1.8GB ✅
   ```

**Deliverable:** `tracking/performance-benchmarks.md`

---

## 📋 PHASE 3: FULL TESTING (17 hours, EXPANDED)

### Existing Tests (14h)
- Unit tests (2h)
- Integration tests (2h)
- Rust integration tests (2h)
- End-to-end testing (2h)
- Bug fixes (3h)
- Performance optimization (2h)
- Final validation (1h)

### Chaos Testing (3h) ⭐ NEW

**Purpose:** Test failure scenarios

**Tasks:**
1. **WebSocket Failure Tests (1h)**
   ```python
   @pytest.mark.asyncio
   async def test_websocket_disconnect_during_order():
       """Simulate WebSocket drop mid-order submission."""
       client = ParadexExecutionClient(...)
       await client.connect()
       
       # Submit order
       order = create_test_order()
       task = asyncio.create_task(client.submit_order(order))
       
       # Kill WebSocket mid-flight
       await asyncio.sleep(0.1)
       await client._ws_client.disconnect()
       
       # Should reconnect and reconcile
       await task
       
       # Verify order status correct after reconnect
       assert client.get_order_status(order.client_order_id) == OrderStatus.ACCEPTED
   ```

2. **REST API Failure Tests (1h)**
   ```python
   async def test_rest_timeout_with_retry():
       """Test REST timeout handling."""
       # Mock returns timeout
       # Should retry 3 times
       # Should eventually succeed or fail gracefully
   ```

3. **State Recovery Tests (1h)**
   ```python
   async def test_crash_recovery():
       """Test state recovery after process crash."""
       # Submit orders
       # Simulate crash (kill process)
       # Restart
       # Reconcile
       # Verify no data loss
   ```

**Deliverable:** `tests/chaos/`, `tracking/chaos-test-results.md`

---

## 📋 PHASE 4: DOCUMENTATION REVIEW (2 hours, SIMPLIFIED)

**Purpose:** Review and polish (not write from scratch)

**Tasks:**
1. Review all docstrings (0.5h)
2. Create usage examples (1h)
3. Final review (0.5h)

---

## 📊 REVISED ESTIMATES

### Time:
- **Phase 0:** 6h (NEW)
- **Phase 0.5:** 3h (NEW)
- **Phase 1:** 12.5h (reorganized)
- **Phase 1.5:** 4h (NEW)
- **Phase 2:** 38h (with incremental validation)
- **Phase 2.1:** 3h (NEW)
- **Phase 3:** 17h (expanded)
- **Phase 4:** 2h (simplified)
- **TOTAL:** 85.5h (was 68h)

### Credits:
- **Phase 0:** 80-100
- **Phase 0.5:** 40-50
- **Phase 1:** 200-250
- **Phase 1.5:** 60-80
- **Phase 2:** 650-800
- **Phase 2.1:** 40-60
- **Phase 3:** 280-350
- **Phase 4:** 30-40
- **TOTAL:** 1,400-1,700 (was 1,100-1,400)

### ROI:
- **Extra Investment:** +17.5h, +300 credits
- **Benefits:**
  - Fewer bugs (better planning)
  - Faster debugging (incremental validation)
  - Higher confidence (chaos testing)
  - Production-ready from day 1

---

## 💡 KEY IMPROVEMENTS

1. ✅ **Dependency-aware** - Critical path identified
2. ✅ **Reconciliation-first** - Foundation before features
3. ✅ **Incremental validation** - Catch bugs early
4. ✅ **Mock infrastructure** - Offline development
5. ✅ **Integration sandbox** - Test before full system
6. ✅ **Performance baseline** - Validate claims
7. ✅ **Chaos testing** - Production-ready

---

**Next: See WORKFLOW.md for original workflow or use this V2 for improved approach**
