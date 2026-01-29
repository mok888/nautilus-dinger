# WORKFLOW V3 - DEPENDENCY-AWARE IMPLEMENTATION

**Version:** 3.0 (Critical Path Optimized)  
**Total Time:** 85.5 hours  
**Total Credits:** 1,400-1,700  
**Approach:** Analyze → Foundation → Critical Path → Parallel → Validate

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
Phase 0: Preparation (6h) ⭐ NEW
  ├─ Dependency Analysis (2h) - Map task dependencies
  └─ Exploration & Learning (4h) - Understand Paradex quirks
  ↓
Phase 0.5: Mock Infrastructure (3h) ⭐ NEW
  └─ Create comprehensive mocks for offline development
  ↓
Phase 1: Python Foundation (12.5h) - REORGANIZED
  ├─ CRITICAL PATH: Reconciliation Foundation (3h) ⭐ BLOCKING
  ├─ CRITICAL PATH: Method Signatures (1h) ⭐ BLOCKING
  ├─ PARALLEL: Base Methods (0.5h)
  ├─ PARALLEL: Subscription Methods (2h)
  ├─ PARALLEL: Request Methods (1h)
  ├─ DEPENDENT: Execution Client (1h)
  └─ DEPENDENT: Refactor/Tests (4h)
  ↓
Phase 1.5: Integration Sandbox (4h) ⭐ NEW
  └─ Test Python↔Rust integration in isolation
  ↓
Phase 2: Rust Core (38h) - WITH INCREMENTAL VALIDATION
  ├─ CRITICAL: PyO3 bindings (3h) ⭐ BLOCKING
  ├─ CRITICAL: State management (2h) ⭐ BLOCKING
  └─ PARALLEL: Other components (33h)
  ↓
Phase 2.1: Performance Baseline (3h) ⭐ NEW
  └─ Validate 100x improvement claim
  ↓
Phase 3: Full System Testing (17h) - EXPANDED
  ├─ Unit/Integration tests (14h)
  └─ Chaos Testing (3h) ⭐ NEW
  ↓
Phase 4: Documentation Review (2h) - SIMPLIFIED
  └─ Review docs, create examples
```

---

## 📋 PHASE 0: PREPARATION (6 hours)

### Phase 0.1: Dependency Analysis (2h, 30-40 credits)

**Goal:** Map task dependencies and identify critical path

```bash
# Create dependency analysis
touch tracking/dependency-graph.md
```

**Tasks:**
1. **Map Python→Rust dependencies** (30 min)
   - Which Python methods need Rust components?
   - Which Rust components are foundational?

2. **Identify critical path** (45 min)
   - Reconciliation logic (blocks everything)
   - PyO3 bindings (blocks Python integration)
   - State management (blocks concurrent operations)

3. **Find parallelizable tasks** (30 min)
   - Subscription methods (independent)
   - Request methods (independent)
   - HTTP vs WebSocket clients (independent)

4. **Risk assessment** (15 min)
   - STARK signing complexity
   - WebSocket stability
   - Performance bottlenecks

**Deliverable:** `tracking/dependency-graph.md`

### Phase 0.2: Exploration & Learning (4h, 60-80 credits)

**Goal:** Understand Paradex API quirks before implementation

**Tasks:**
1. **API exploration** (2h)
   ```bash
   # Test real Paradex endpoints
   curl -X GET "https://api.testnet.paradex.trade/v1/system/time"
   
   # Record responses
   mkdir exploration/api-responses/
   ```

2. **WebSocket testing** (1h)
   ```bash
   # Test WebSocket connection
   wscat -c wss://ws.testnet.paradex.trade/v1
   
   # Document JSON-RPC protocol quirks
   ```

3. **STARK signature testing** (1h)
   ```python
   # Test signature generation
   from starknet_py.hash.selector import get_selector_from_name
   # Document nonce requirements, message format
   ```

**Deliverable:** `exploration/exploration-notes.md`

---

## 📋 PHASE 0.5: MOCK INFRASTRUCTURE (3 hours, 40-60 credits)

**Goal:** Create comprehensive mocks for offline development

```bash
mkdir -p mocks/paradex-mock/
cd mocks/paradex-mock/
```

**Tasks:**
1. **HTTP mock server** (1.5h)
   ```python
   # mocks/paradex-mock/http_server.py
   from flask import Flask, jsonify
   
   app = Flask(__name__)
   
   @app.route('/v1/system/time')
   def system_time():
       return jsonify({"server_time": 1640995200})
   ```

2. **WebSocket mock server** (1h)
   ```python
   # mocks/paradex-mock/ws_server.py
   import asyncio
   import websockets
   import json
   ```

3. **Test fixtures** (0.5h)
   ```bash
   # Record real API responses as fixtures
   mkdir mocks/fixtures/
   # Save responses for replay
   ```

**Deliverable:** `mocks/paradex-mock/` directory

---

## 📋 PHASE 1: PYTHON FOUNDATION (12.5 hours) - REORGANIZED

### CRITICAL PATH (Must complete first):

#### Step 0: Reconciliation Foundation (3h, 50-70 credits) ⭐ BLOCKING
**Why first:** Everything depends on reconciliation working correctly

```python
# Implement reconciliation skeleton FIRST
async def _reconcile_state(self) -> None:
    """Reconcile internal state with exchange state."""
    # 1. Fetch positions from REST
    # 2. Fetch orders from REST  
    # 3. Compare with internal state
    # 4. Emit correction events
    # 5. Update internal state
```

**Validation after this step:**
```bash
python tests/test_reconciliation.py --isolated
# Must pass before proceeding
```

#### Step 1: Fix Method Signatures (1h, 15-20 credits) ⭐ BLOCKING
**Why critical:** Framework won't work with wrong signatures

```python
# Fix these 6 methods:
async def _subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
async def _subscribe_quote_ticks(self, command: SubscribeQuoteTicks) -> None:
# ... etc
```

**Validation after this step:**
```bash
python -c "from nautilus_trader.adapters.paradex.data import ParadexDataClient"
# Must import without errors
```

### PARALLEL TRACK (Can run alongside critical path):

#### Step 2: Add Base Methods (0.5h, 8-12 credits)
#### Step 3: Add Subscription Methods (2h, 30-40 credits)  
#### Step 4: Add Request Methods (1h, 15-20 credits)

### DEPENDENT ON CRITICAL PATH:

#### Step 5: Fix Execution Client (1h, 15-20 credits)
#### Steps 6-10: Refactor/Tests/Validation (4h, 60-80 credits)

**Incremental Validation:**
```bash
# After each method group
python tests/validate_data_client.py --group subscriptions
python tests/validate_data_client.py --group requests
python tests/validate_execution_client.py --group orders
```

---

## 📋 PHASE 1.5: INTEGRATION SANDBOX (4 hours, 60-80 credits) ⭐ NEW

**Goal:** Test Python↔Rust integration before full system

**Tasks:**
1. **Isolated PyO3 testing** (2h)
   ```python
   # Test PyO3 bindings in isolation
   import paradex_core  # Rust module
   
   # Test basic operations
   client = paradex_core.HttpClient("testnet")
   response = client.get("/v1/system/time")
   ```

2. **Mock integration testing** (1h)
   ```python
   # Test with mock servers
   data_client = ParadexDataClient(mock_mode=True)
   await data_client.connect()
   # Should work without real API
   ```

3. **Event pipeline testing** (1h)
   ```python
   # Test event emission
   # Verify events reach message bus correctly
   ```

**Deliverable:** `tracking/sandbox-test-results.md`

---

## 📋 PHASE 2: RUST CORE (38 hours) - WITH INCREMENTAL VALIDATION

### CRITICAL PATH (Must complete first):

#### PyO3 Bindings (3h) ⭐ BLOCKING
#### State Management (2h) ⭐ BLOCKING

### PARALLEL COMPONENTS:
- HTTP Client (8h)
- WebSocket Client (12h)  
- STARK Signing (6h)
- Message Handlers (7h)

**Validation after each component:**
```bash
cargo test --package paradex --lib http::tests
cargo test --package paradex --lib websocket::tests
cargo test --package paradex --lib signing::tests
```

---

## 📋 PHASE 2.1: PERFORMANCE BASELINE (3 hours, 40-60 credits) ⭐ NEW

**Goal:** Validate performance claims and set targets

**Tasks:**
1. **Benchmark state access** (1h)
   ```rust
   // Benchmark DashMap vs RwLock
   // Target: <1ms (95th percentile)
   ```

2. **Benchmark HTTP throughput** (1h)
   ```rust
   // Target: >1000 requests/second
   ```

3. **Benchmark WebSocket handling** (1h)
   ```rust
   // Target: <5ms message parse time
   ```

**Deliverable:** `tracking/performance-benchmarks.md`

---

## 📋 PHASE 3: FULL SYSTEM TESTING (17 hours) - EXPANDED

### Phase 3.1: Standard Testing (14h)
- Unit tests (85%+ coverage)
- Integration tests
- Bug fixes

### Phase 3.2: Chaos Testing (3h, 40-60 credits) ⭐ NEW

**Goal:** Test failure scenarios

**Scenarios:**
```bash
# Test WebSocket disconnection
./tests/chaos/test_websocket_failure.py

# Test REST API timeout
./tests/chaos/test_rest_timeout.py

# Test process crash recovery
./tests/chaos/test_crash_recovery.py
```

**Deliverable:** `tracking/chaos-test-results.md`

---

## 📋 PHASE 4: DOCUMENTATION REVIEW (2 hours) - SIMPLIFIED

**Goal:** Review and polish (not write from scratch)

**Tasks:**
1. **Review all documentation** (1h)
2. **Create usage examples** (1h)

---

## 🎯 KEY IMPROVEMENTS OVER V2

1. **Dependency-aware:** Critical path identified and prioritized
2. **Reconciliation-first:** Foundation built before dependent components
3. **Incremental validation:** Catch bugs after each logical unit
4. **Mock-driven:** Offline development capability
5. **Chaos testing:** Production failure scenarios tested
6. **Performance validation:** Concrete benchmarks and targets

---

## 📊 COMPARISON WITH PREVIOUS VERSIONS

| Aspect | V1 | V2 | V3 |
|--------|----|----|----| 
| **Total Time** | 68h | 85.5h | 85.5h |
| **Upfront Planning** | 0h | 9h | 9h |
| **Critical Path** | ❌ | ⚪ | ✅ |
| **Incremental Validation** | ❌ | ❌ | ✅ |
| **Mock Infrastructure** | ❌ | ❌ | ✅ |
| **Chaos Testing** | ❌ | ❌ | ✅ |
| **Production Ready** | Maybe | Yes | Guaranteed |

---

**Ready to begin? → Start with Phase 0: Dependency Analysis**
