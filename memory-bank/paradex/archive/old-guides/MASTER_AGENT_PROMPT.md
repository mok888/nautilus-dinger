# PARADEX NAUTILUS ADAPTER - MASTER AGENT PROMPT

**Project:** Paradex Nautilus Adapter Implementation  
**Location:** /home/mok/projects/nautilus-dinger/  
**Status:** In Development (20% complete)  
**Compliance:** ❌ NOT COMPLIANT - Requires fixes

---

## 🎯 PROJECT OBJECTIVE

Build a **production-grade Nautilus Trader adapter** for Paradex (StarkNet-based perpetual futures exchange) that is **100% compliant** with official Nautilus specifications.

**Success Criteria:**
- ✅ All 38 LiveMarketDataClient methods implemented
- ✅ All 12 LiveExecutionClient methods implemented
- ✅ All method signatures match official specification
- ✅ Rust core with HTTP, WebSocket, STARK signing
- ✅ Comprehensive tests (unit + integration)
- ✅ Full documentation

---

## 🚨 CRITICAL RULES (NEVER VIOLATE)

### Rule 1: READ BEFORE CODING
**MANDATORY:** Before writing ANY code, read these documents in order:

1. **memory-bank/PROJECT_ORGANIZATION.md** - File organization standards
2. **memory-bank/bug-fixes-record.md** - Known bugs and fixes
3. **memory-bank/progress.md** - Current project status
4. **memory-bank/COMPLIANCE_AUDIT.md** - What's missing
5. **memory-bank/QUICK_START_WITH_VALIDATION.md** - Implementation guide

**Why:** Avoid duplicating work, understand current state, know what needs fixing.

### Rule 2: USE EXISTING CODE (DON'T REINVENT)
**MANDATORY:** Always check official Nautilus repo FIRST before writing code.

**Process:**
1. **Search GitHub first:** Use web_fetch to get code from official repo
2. **Copy patterns:** Use OKX adapter as gold standard reference
3. **Adapt, don't create:** Modify existing patterns for Paradex
4. **Glue coding:** Connect existing components, don't rewrite

**Official Reference:**
- **OKX Adapter:** https://github.com/nautechsystems/nautilus_trader/tree/develop/nautilus_trader/adapters/okx
- **BitMEX Adapter:** https://github.com/nautechsystems/nautilus_trader/tree/develop/nautilus_trader/adapters/bitmex
- **Bybit Adapter:** https://github.com/nautechsystems/nautilus_trader/tree/develop/nautilus_trader/adapters/bybit

**Example:**
```bash
# WRONG: Writing from scratch
def _subscribe_trade_ticks(self, command):
    # ... writing 50 lines of new code

# RIGHT: Copy from OKX, adapt for Paradex
# 1. Fetch OKX implementation
# 2. Copy the pattern
# 3. Change only Paradex-specific parts (API calls)
```

### Rule 3: VALIDATE AFTER EVERY CHANGE
**MANDATORY:** Run validation after EVERY phase, EVERY file, EVERY change.

**Validation Commands:**
```bash
# Syntax check
python -m py_compile [file].py

# Import test
python -c "from nautilus_trader.adapters.paradex import *"

# Method count
python tests/validation/count_methods.py

# Compliance check
python tests/validation/validate_compliance.py
```

**If validation FAILS:**
1. STOP immediately
2. Document in bug-fixes-record.md
3. Fix the issue
4. Re-validate
5. THEN continue

### Rule 4: DOCUMENT EVERYTHING
**MANDATORY:** Update documentation after EVERY change.

**Required Updates:**
- **Bug fix?** → Update `bug-fixes-record.md`
- **Improvement?** → Update `improvements-log.md`
- **Validation run?** → Update `validation-results.md`
- **Phase complete?** → Update `progress.md`
- **Git commit?** → Reference entry number

### Rule 5: FOLLOW OFFICIAL PATTERNS EXACTLY
**MANDATORY:** Match official Nautilus patterns with ZERO deviation.

**Method Signatures:**
```python
# WRONG:
async def _subscribe_trade_ticks(self, instrument_id: InstrumentId) -> None:

# RIGHT (from official spec):
async def _subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
```

**Reference:** `memory-bank/NAUTILUS_PATTERNS_REFERENCE.md`

### Rule 6: IMPLEMENT RECONCILIATION LOGIC (CRITICAL)
**MANDATORY:** Execution client MUST reconcile state on connect.

**Why Critical:**
- REST is authoritative (WebSocket is hints only)
- Prevents state desync on reconnection
- Ensures idempotent operations
- Required by Nautilus specification

**Pattern (from OKX):**
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

async def _reconcile_state(self) -> None:
    """Reconcile orders, fills, positions from REST API."""
    # Query REST for current state
    orders = await self._http_client.get_open_orders()
    fills = await self._http_client.get_recent_fills()
    positions = await self._http_client.get_positions()
    
    # Generate reports for Nautilus
    for order in orders:
        report = self._parse_order_status_report(order)
        self.generate_order_status_report(report)
    
    # Track emitted fills to prevent duplicates
    for fill in fills:
        if fill.trade_id not in self._emitted_fills:
            self.generate_fill_report(fill)
            self._emitted_fills.add(fill.trade_id)

async def _run_reconciliation_loop(self) -> None:
    """Periodic reconciliation (every 5 minutes)."""
    while True:
        await asyncio.sleep(self._config.reconcile_interval_secs)
        await self._reconcile_state()
```

**Key Points:**
- ✅ Reconcile on EVERY connect/reconnect
- ✅ Query REST API (authoritative source)
- ✅ Generate reports for Nautilus engine
- ✅ Track emitted fills (prevent duplicates)
- ✅ Periodic reconciliation (default: 5 minutes)
- ❌ NEVER trust WebSocket alone
- ❌ NEVER skip reconciliation

**Reference:** `memory-bank/2_PYTHON_ADAPTER_IMPLEMENTATION.md` (Pattern #1)

---

## ✅ DO's (REQUIRED PRACTICES)

### DO: Use Official Reference Code
- ✅ Fetch code from GitHub using web_fetch
- ✅ Copy OKX adapter patterns
- ✅ Adapt for Paradex API specifics
- ✅ Reference official documentation

### DO: Follow File Organization
- ✅ Tests in `/tests/` directory
- ✅ Documentation in `/memory-bank/`
- ✅ Production code in `/nautilus_trader/adapters/paradex/`
- ✅ Validation scripts in `/tests/validation/`

### DO: Validate Continuously
- ✅ After every phase
- ✅ After every file
- ✅ Before committing
- ✅ Document results

### DO: Document Changes
- ✅ Bug fixes in bug-fixes-record.md
- ✅ Improvements in improvements-log.md
- ✅ Validation in validation-results.md
- ✅ Progress in progress.md

### DO: Use Glue Coding
- ✅ Connect existing components
- ✅ Adapt existing patterns
- ✅ Reuse proven code
- ✅ Minimize custom code

---

## ❌ DON'Ts (FORBIDDEN PRACTICES)

### DON'T: Write Code from Scratch
- ❌ Creating new patterns when official ones exist
- ❌ Reinventing existing functionality
- ❌ Ignoring reference implementations
- ❌ Writing without checking GitHub first

### DON'T: Skip Documentation
- ❌ "It's too small to document"
- ❌ "I'll document later"
- ❌ Leaving bugs undocumented
- ❌ Skipping validation results

### DON'T: Mix File Types
- ❌ Tests in production directories
- ❌ Documentation in code directories
- ❌ Validation scripts scattered
- ❌ Unorganized structure

### DON'T: Skip Validation
- ❌ "I'll test later"
- ❌ "This is too simple to test"
- ❌ Proceeding with failed validation
- ❌ Accumulating technical debt

### DON'T: Deviate from Spec
- ❌ Custom method signatures
- ❌ Different parameter types
- ❌ Skipping required methods
- ❌ "My way is better"

---

## 🛠️ REQUIRED SKILLS

### Technical Skills:
1. **Python 3.10+** - Async/await, type hints, Pydantic
2. **Rust** - Tokio, PyO3, serde, async programming
3. **Git** - Version control, branching, commits
4. **Testing** - pytest, unit tests, integration tests
5. **API Integration** - REST, WebSocket, JSON-RPC

### Domain Knowledge:
1. **Nautilus Trader** - Architecture, patterns, conventions
2. **Paradex API** - Endpoints, authentication, data structures
3. **StarkNet** - STARK signatures, account abstraction
4. **Trading Systems** - Orders, fills, positions, reconciliation

### Soft Skills:
1. **Reading Comprehension** - Understand existing code
2. **Pattern Recognition** - Identify reusable patterns
3. **Attention to Detail** - Match specifications exactly
4. **Documentation** - Clear, complete, consistent

---

## 📋 WORKFLOW (FOLLOW EXACTLY)

### Step 1: PREPARATION (Before ANY coding)

```bash
# 1. Read project status
cat memory-bank/progress.md

# 2. Check known bugs
cat memory-bank/bug-fixes-record.md

# 3. Review compliance gaps
cat memory-bank/COMPLIANCE_AUDIT.md

# 4. Read implementation guide
cat memory-bank/QUICK_START_WITH_VALIDATION.md

# 5. Check file organization
cat memory-bank/PROJECT_ORGANIZATION.md
```

**Checklist:**
- [ ] Read all 5 documents above
- [ ] Understand current status
- [ ] Know what needs fixing
- [ ] Understand file organization
- [ ] Ready to proceed

### Step 2: FETCH REFERENCE CODE

```bash
# Use web_fetch to get official implementation
# Example: Get OKX data client
```

**Process:**
1. Identify what you need to implement
2. Find equivalent in OKX adapter
3. Fetch the code from GitHub
4. Study the pattern
5. Adapt for Paradex

**Example:**
```python
# Need to implement _subscribe_trade_ticks?
# 1. Fetch OKX implementation
# 2. Copy the pattern:
async def _subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.subscribe_trades(pyo3_instrument_id)

# 3. Adapt for Paradex (only change API-specific parts)
```

### Step 3: IMPLEMENT (With validation)

```bash
# For each phase in QUICK_START_WITH_VALIDATION.md:

# 1. Implement the change
# 2. Run validation
python -m py_compile [file].py

# 3. Check results
python tests/validation/validate_compliance.py

# 4. Document
# - Update bug-fixes-record.md if fixing bug
# - Update improvements-log.md if adding feature
# - Update validation-results.md with results

# 5. If PASS, proceed to next phase
# 6. If FAIL, fix immediately and re-validate
```

### Step 4: DOCUMENT

```bash
# After EVERY change:

# 1. Update appropriate log
vim memory-bank/bug-fixes-record.md      # If bug fix
vim memory-bank/improvements-log.md      # If improvement
vim memory-bank/validation-results.md    # Validation results

# 2. Update progress
vim memory-bank/progress.md

# 3. Commit with reference
git add .
git commit -m "Fix #001: Wrong method signatures in data.py"
```

### Step 5: VALIDATE & ITERATE

```bash
# Run full validation suite
cd tests/validation
python validate_compliance.py

# If issues found:
# 1. Document in bug-fixes-record.md
# 2. Fix immediately
# 3. Re-validate
# 4. Update documentation

# If all pass:
# 1. Update progress.md
# 2. Move to next phase
```

---

## 📚 REQUIRED READING (IN ORDER)

### Before Starting:
1. **PROJECT_ORGANIZATION.md** - File organization (5 min)
2. **progress.md** - Current status (2 min)
3. **bug-fixes-record.md** - Known bugs (3 min)
4. **COMPLIANCE_AUDIT.md** - What's missing (10 min)
5. **STUDY_COMPLETE_SUMMARY.md** - Project overview (10 min)

### During Implementation:
1. **QUICK_START_WITH_VALIDATION.md** - Step-by-step guide (reference)
2. **NAUTILUS_PATTERNS_REFERENCE.md** - Code patterns (reference)
3. **IMPLEMENTATION_ACTION_PLAN.md** - Detailed plan (reference)

### For Reference:
1. **Official Nautilus Docs** - https://nautilustrader.io/docs/latest/developer_guide/adapters/
2. **OKX Adapter Source** - https://github.com/nautechsystems/nautilus_trader/tree/develop/nautilus_trader/adapters/okx
3. **Paradex API Docs** - https://docs.paradex.trade/

---

## 🚀 IMPLEMENTATION PRIORITIES

### Phase 1: Python Layer Fixes (12.5 hours) - CRITICAL
**Priority:** CRITICAL  
**Status:** Not started

**Tasks:**
1. Fix method signatures (6 methods) - Bug #001
2. Add base methods (3 methods) - Bug #002
3. Add subscription methods (16 methods) - Bug #002
4. Add request methods (7 methods) - Bug #002
5. Fix execution client (2 methods) - Bug #003
6. **Implement reconciliation logic** - CRITICAL
   - `_reconcile_state()` method
   - `_run_reconciliation_loop()` method
   - Fill deduplication tracking (`self._emitted_fills: set[TradeId]`)
   - REST-authoritative pattern

**Refactoring & Quality (MANDATORY):**
- ✅ Code refactoring and cleanup
- ✅ Unit tests for all methods
- ✅ Validation after each section
- ✅ Code review

**Reference:** QUICK_START_WITH_VALIDATION.md

**Reconciliation Requirements:**
- ✅ Query REST on connect (MANDATORY)
- ✅ Generate order status reports
- ✅ Generate fill reports (deduplicated)
- ✅ Generate position reports
- ✅ Periodic reconciliation (5 min default)
- ✅ Track emitted fills to prevent duplicates

**Reference Code:** `memory-bank/execution.py` lines 202-220

---

### Phase 2: Rust Core (38 hours) - CRITICAL
**Priority:** HIGH  
**Status:** Not started

**Tasks:**
1. HTTP client (~500 LOC)
2. WebSocket client (~400 LOC)
3. STARK signing (~200 LOC)
4. PyO3 bindings (~300 LOC)
5. **State management with DashMap** (~200 LOC) - Bug #004
6. **Reconciliation logic** (~150 LOC) - Bug #005
7. **Subscription tracking** (~100 LOC) - Bug #006
8. **Connection state machine** (~80 LOC) - Bug #007
9. **Race condition prevention** (~100 LOC) - Bug #008
10. **Event emission** (~200 LOC) - Bug #009
11. **Message routing** (~150 LOC) - Bug #011

**Refactoring & Quality (MANDATORY):**
- ✅ Code refactoring after each component
- ✅ Integration tests
- ✅ Performance optimization
- ✅ Code review and cleanup
- ✅ Validation

**Reference:** 1_RUST_CORE_IMPLEMENTATION.md

**Critical Components (MUST IMPLEMENT):**
See `CRITICAL_MISSING_COMPONENTS.md` for detailed requirements:
- ✅ Use DashMap (not RwLock) for state
- ✅ Implement proper reconciliation
- ✅ Track connection state machine
- ✅ Prevent REST/WebSocket races
- ✅ Emit proper Nautilus events
- ✅ Parse and route messages correctly

**Total Rust LOC:** ~2,480 (increased from ~1,400)

---

### Phase 3: Full System Testing (14 hours) - HIGH
**Priority:** HIGH  
**Status:** Not started

**Tasks:**
1. Python unit tests (comprehensive)
2. Python integration tests
3. Rust integration tests
4. End-to-end testing
5. **Bug fixes from testing**
6. **Performance optimization**
7. **Final validation**

**Quality Assurance (MANDATORY):**
- ✅ Unit tests for all components
- ✅ Integration tests
- ✅ Performance benchmarks
- ✅ Load testing
- ✅ Bug fixes
- ✅ Final validation

**Reference:** agent-auto-validation.md

---

### Phase 4: Documentation & Polish (3.5 hours) - MEDIUM
**Priority:** MEDIUM  
**Status:** Partial

**Tasks:**
1. Update documentation
2. Create usage examples
3. **Code review and refactor**
4. **Final validation**

**Quality Assurance:**
- ✅ Documentation complete
- ✅ Examples working
- ✅ Code reviewed
- ✅ Production ready

---

## 🔍 CODE FETCHING STRATEGY

### When to Fetch from GitHub:

**ALWAYS fetch for:**
- Method implementations
- Class structures
- Error handling patterns
- WebSocket message handling
- HTTP client patterns
- Configuration classes

**Example Workflow:**
```bash
# Need to implement _subscribe_trade_ticks?

# 1. Fetch OKX implementation
web_fetch("https://raw.githubusercontent.com/nautechsystems/nautilus_trader/develop/nautilus_trader/adapters/okx/data.py")

# 2. Find _subscribe_trade_ticks method
# 3. Copy the pattern
# 4. Adapt for Paradex API
# 5. Validate
```

### What to Adapt (Not Copy Directly):

**Paradex-Specific:**
- API endpoints (Paradex URLs)
- Authentication (STARK signatures vs HMAC)
- WebSocket protocol (JSON-RPC vs raw JSON)
- Instrument types (only perpetuals)

**Keep from OKX:**
- Method signatures
- Parameter handling
- PyO3 conversions
- Error handling structure
- Validation patterns

---

## 📊 PROGRESS TRACKING

### Current Status:
- **Phase:** Planning/Preparation
- **Completion:** 20%
- **Bugs:** 3 known (all pending)
- **Tests:** 0 (not created)
- **Compliance:** ❌ NOT COMPLIANT

### Next Immediate Actions:
1. Read all required documents
2. Fetch OKX adapter code
3. Start Phase 1: Fix method signatures
4. Validate after each change
5. Document everything

---

## 🚨 CRITICAL REMINDERS

### Before Writing ANY Code:
- [ ] Read progress.md
- [ ] Read bug-fixes-record.md
- [ ] Check COMPLIANCE_AUDIT.md
- [ ] Fetch reference code from GitHub
- [ ] Understand the pattern

### While Writing Code:
- [ ] Copy from official repo
- [ ] Adapt, don't reinvent
- [ ] Use glue coding
- [ ] Validate continuously
- [ ] Document immediately

### After Writing Code:
- [ ] Run validation
- [ ] Update documentation
- [ ] Commit with reference
- [ ] Check progress
- [ ] Plan next step

---

## 🎓 LEARNING RESOURCES

### Official Documentation:
- **Nautilus Adapters:** https://nautilustrader.io/docs/latest/developer_guide/adapters/
- **Paradex API:** https://docs.paradex.trade/
- **StarkNet:** https://docs.starknet.io/

### Reference Implementations:
- **OKX Adapter:** Best reference for structure
- **BitMEX Adapter:** Good WebSocket patterns
- **Bybit Adapter:** Good error handling

### Project Documentation:
- **All docs in memory-bank/** - Read before coding
- **All tests in tests/** - Reference for testing
- **All code in nautilus_trader/adapters/paradex/** - Production code

---

## ✅ COMPLETION CHECKLIST

### Phase Completion:
- [ ] Phase 1: Python Fixes + Refactor + Tests (12.5h)
- [ ] Phase 2: Rust Core + Refactor + Tests (38h)
- [ ] Phase 3: Full Testing + Optimization (14h)
- [ ] Phase 4: Documentation + Review (3.5h)

### Quality Gates (MANDATORY):

**After Phase 1:**
- [ ] All 38 data client methods implemented
- [ ] All 12 execution client methods implemented
- [ ] Code refactored and cleaned
- [ ] Unit tests passing
- [ ] Validation passing
- [ ] No syntax errors
- [ ] Ready for Rust layer

**After Phase 2:**
- [ ] All Rust components implemented
- [ ] Code refactored and optimized
- [ ] Integration tests passing
- [ ] No race conditions
- [ ] Performance benchmarks met
- [ ] PyO3 bindings working
- [ ] Ready for system testing

**After Phase 3:**
- [ ] All tests passing (unit + integration)
- [ ] Performance optimized
- [ ] Bug fixes complete
- [ ] Load testing passed
- [ ] Production validation passed
- [ ] Ready for deployment

**After Phase 4:**
- [ ] Documentation complete
- [ ] Examples working
- [ ] Code reviewed
- [ ] Final validation passed
- [ ] Production ready

### Validation Results:
- [ ] Data client: __/38 methods
- [ ] Execution client: __/12 methods
- [ ] Rust components: __/11 complete
- [ ] Test coverage: __%
- [ ] Performance: __ ops/sec
- [ ] Compliance: YES/NO

### Quality Metrics:
- **Total LOC:** ~6,830 (with refactoring)
- **Test Coverage:** >85%
- **Performance:** 100x faster (DashMap)
- **Compliance:** 100%
- **Technical Debt:** Very Low
- **Production Ready:** YES

---

## 🎯 FINAL INSTRUCTIONS

### Your Mission:
Build a **production-grade, fully compliant** Paradex Nautilus adapter by:
1. **Reading** all required documentation FIRST
2. **Fetching** reference code from official repo
3. **Adapting** existing patterns (not reinventing)
4. **Validating** after every change
5. **Documenting** everything

### Your Constraints:
- ❌ NO code from scratch when official patterns exist
- ❌ NO skipping documentation
- ❌ NO proceeding with failed validation
- ❌ NO deviating from official spec
- ❌ NO mixing test and production code

### Your Tools:
- **web_fetch** - Get code from GitHub
- **Validation scripts** - Check compliance
- **Documentation** - Track everything
- **Official patterns** - Copy and adapt

### Your Success Criteria:
- ✅ 100% compliant with Nautilus spec
- ✅ All methods implemented correctly
- ✅ All tests passing
- ✅ All documentation complete
- ✅ Production-ready code

---

**READ → FETCH → ADAPT → VALIDATE → DOCUMENT → REPEAT**

**START HERE:** `cat memory-bank/QUICK_START_WITH_VALIDATION.md`
