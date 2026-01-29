# PARADEX NAUTILUS ADAPTER - DOCUMENTATION INDEX

**Last Updated:** 2026-01-27  
**Status:** Study Complete - Ready to Implement  
**Compliance:** ❌ NOT COMPLIANT (20% complete)

---

## 📚 DOCUMENTATION FILES

### 0. **MASTER_AGENT_PROMPT.md** ⭐⭐⭐ START HERE FIRST
**Purpose:** Complete agent instructions and project rules  
**Contents:**
- Critical rules (NEVER violate)
- DO's and DON'Ts
- Required skills
- Workflow (step-by-step)
- Code fetching strategy (use GitHub, don't reinvent)
- Progress tracking
- Success checklist
- **UPDATED:** Full refactoring requirements

**READ THIS FIRST BEFORE ANY CODING - Contains all rules and instructions.**

---

### 0.5. **REFACTORING_UPDATE_SUMMARY.md** ⭐⭐ NEW APPROACH
**Purpose:** Full refactoring integration summary  
**Contents:**
- What changed (implementation-only → full refactoring)
- Updated estimates (68h, 1,100-1,400 credits)
- Quality improvements (0% → 90% test coverage)
- ROI analysis (+20h investment, lower long-term cost)
- Phase-by-phase quality gates
- Documents updated

**READ THIS SECOND - Understand the new quality-focused approach.**

---

### 1. **STUDY_COMPLETE_SUMMARY.md** ⭐ PROJECT OVERVIEW
**Purpose:** Executive summary of study findings  
**Contents:**
- What was studied (OKX adapter, Nautilus docs, Paradex API)
- Critical findings (non-compliance issues)
- Key patterns learned
- Paradex-specific adaptations
- Immediate next steps

**Read this first to understand the situation.**

---

### 2. **QUICK_START_WITH_VALIDATION.md** ⭐⭐ IMPLEMENTATION GUIDE
**Purpose:** Step-by-step implementation with auto-validation at EVERY step  
**Contents:**
- 9 phases with validation checkpoints after EACH step
- Exact code to copy-paste
- Validation commands and expected outputs
- Pass/Fail tracking with metrics
- Time estimates: 8-10 hours
- **NEW:** Integrated agent-auto-validation.md framework

**Use this to fix the code with early bug detection and quality assurance.**

---

### 2b. **QUICK_START_CHECKLIST.md** (Original - No Validation)
**Purpose:** Basic checklist without validation  
**Note:** Use QUICK_START_WITH_VALIDATION.md instead for better results

---

### 3. **VALIDATION_INTEGRATION_SUMMARY.md** 🆕
**Purpose:** Explains validation integration enhancement  
**Contents:**
- What validation was added
- Validation checkpoints per phase
- Metrics tracked
- Benefits of validation-first approach
- How to use the framework

**Read this to understand the validation enhancement.**

---

### 4. **PROJECT_ORGANIZATION.md** 🆕 MANDATORY
**Purpose:** Define file organization and documentation standards  
**Contents:**
- Directory structure (tests/, memory-bank/, production code)
- Test file locations (validation/, unit/, integration/)
- Documentation requirements (bug fixes, improvements, validation results)
- Workflow for bugs, improvements, and validations
- Agent instructions for proper organization

**READ THIS BEFORE MAKING ANY CHANGES - Defines where files go and how to document.**

---

### 5. **COMPLIANCE_AUDIT.md**
**Purpose:** Detailed gap analysis  
**Contents:**
- Missing methods (30 in data client, 2 in execution client)
- Wrong method signatures
- Incomplete Rust structure
- Missing tests
- Estimated work remaining: 18-26 hours

**Reference this to understand what's missing.**

---

### 4. **IMPLEMENTATION_ACTION_PLAN.md**
**Purpose:** Phase-by-phase implementation guide  
**Contents:**
- Phase 1: Fix Python method signatures
- Phase 2: Add missing data client methods (30 methods)
- Phase 3: Fix execution client (2 methods)
- Phase 4: Paradex-specific adaptations
- Complete code templates for all methods

**Use this for detailed implementation guidance.**

---

### 5. **NAUTILUS_PATTERNS_REFERENCE.md**
**Purpose:** Copy-paste patterns from OKX adapter  
**Contents:**
- 10 essential patterns with code examples
- Method signatures
- PyO3 conversion
- Error handling
- Event generation
- WebSocket message handling

**Use this as a quick reference while coding.**

---

## 🎯 RECOMMENDED READING ORDER

### For Understanding the Problem:
1. **MASTER_AGENT_PROMPT.md** ⭐⭐⭐ - Read FIRST (all rules and workflow)
2. **STUDY_COMPLETE_SUMMARY.md** - Get the big picture
3. **COMPLIANCE_AUDIT.md** - See detailed gaps
4. **NAUTILUS_PATTERNS_REFERENCE.md** - Learn the patterns

### For Implementation:
1. **MASTER_AGENT_PROMPT.md** ⭐⭐⭐ - Follow workflow exactly
2. **QUICK_START_WITH_VALIDATION.md** - Step-by-step with validation
3. **IMPLEMENTATION_ACTION_PLAN.md** - Reference for details
4. **NAUTILUS_PATTERNS_REFERENCE.md** - Copy-paste patterns
5. **agent-auto-validation.md** - Validation framework reference

---

## 📊 PROJECT STATUS

### Current State
- **Python Data Client:** 8/38 methods (21% complete)
- **Python Execution Client:** 10/12 methods (83% complete)
- **Rust Core:** 0% implemented (stubs only)
- **Tests:** 0 tests exist
- **Compliance:** ❌ NOT COMPLIANT

### What Works
- ✅ Basic structure (directory layout)
- ✅ Configuration classes
- ✅ InstrumentProvider (3/3 methods)
- ✅ Idempotent reconciliation pattern
- ✅ Fill deduplication logic

### What's Broken
- ❌ Wrong method signatures (accept raw types instead of commands)
- ❌ Missing 30 data client methods
- ❌ Missing 2 execution client methods
- ❌ No Rust HTTP client
- ❌ No Rust WebSocket client
- ❌ No STARK signing
- ❌ No tests

---

## 🚀 QUICK START

### If you want to understand the problem:
```bash
cd /home/mok/projects/nautilus-dinger/memory-bank
cat MASTER_AGENT_PROMPT.md  # Read this FIRST
cat STUDY_COMPLETE_SUMMARY.md
```

### If you want to start coding:
```bash
cd /home/mok/projects/nautilus-dinger/memory-bank

# 1. Read the master prompt (MANDATORY)
cat MASTER_AGENT_PROMPT.md

# 2. Check current status
cat progress.md
cat bug-fixes-record.md

# 3. Follow implementation guide
cat QUICK_START_WITH_VALIDATION.md
```

### If you want detailed reference:
```bash
cd /home/mok/projects/nautilus-dinger/memory-bank
cat NAUTILUS_PATTERNS_REFERENCE.md
# Copy patterns as needed
```

---

## 📋 IMPLEMENTATION PHASES

### Phase 1: Python Fixes (8 hours) ⏳ NEXT
- Fix method signatures
- Add missing methods
- Add imports
- Basic validation

### Phase 2: Rust Core (12-16 hours) ⏳ TODO
- HTTP client (~500 LOC)
- WebSocket client (~400 LOC)
- STARK signing (~200 LOC)
- PyO3 bindings (~300 LOC)

### Phase 3: Testing (4-6 hours) ⏳ TODO
- Rust unit tests
- Rust integration tests
- Python integration tests
- Mock servers

### Phase 4: Documentation (2-3 hours) ⏳ TODO
- README updates
- API documentation
- Usage examples

**Total Estimated Time:** 26-33 hours

---

## 🔑 KEY INSIGHTS

### Critical Pattern #1: Method Signatures
**WRONG:**
```python
async def _subscribe_trade_ticks(self, instrument_id: InstrumentId) -> None:
```

**CORRECT:**
```python
async def _subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
```

### Critical Pattern #2: PyO3 Conversion
Always convert Nautilus types to PyO3 types:
```python
pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
pyo3_quantity = nautilus_pyo3.Quantity.from_str(str(order.quantity))
pyo3_price = nautilus_pyo3.Price.from_str(str(order.price))
```

### Critical Pattern #3: Unsupported Features
Log warnings, don't crash:
```python
async def _subscribe_quote_ticks(self, command: SubscribeQuoteTicks) -> None:
    self._log.warning("Quote ticks not supported by Paradex")

async def _unsubscribe_quote_ticks(self, command: UnsubscribeQuoteTicks) -> None:
    pass  # No-op
```

---

## 📞 EXTERNAL REFERENCES

### Official Nautilus Documentation
- **Adapter Guide:** https://nautilustrader.io/docs/latest/developer_guide/adapters/
- **OKX Adapter:** https://github.com/nautechsystems/nautilus_trader/tree/develop/nautilus_trader/adapters/okx

### Paradex Documentation
- **Main Docs:** https://docs.paradex.trade/
- **WebSocket API:** https://docs.paradex.trade/ws/general-information/introduction
- **REST API:** https://docs.paradex.trade/api/

### Reference Adapters (Study These)
- **OKX:** Gold standard - most complete
- **BitMEX:** Good WebSocket patterns
- **Bybit:** Good error handling

---

## ✅ SUCCESS CRITERIA

### Python Layer Complete When:
- [ ] All 38 data client methods implemented
- [ ] All 12 execution client methods implemented
- [ ] All method signatures accept `command` objects
- [ ] All imports present
- [ ] Python syntax validates
- [ ] Basic tests pass

### Rust Layer Complete When:
- [ ] HTTP client with JWT auth
- [ ] WebSocket client with JSON-RPC
- [ ] STARK signing module
- [ ] PyO3 bindings expose all functionality
- [ ] Rust tests pass

### Production Ready When:
- [ ] All Python methods implemented
- [ ] All Rust modules implemented
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Testnet validation successful

---

## 🎯 IMMEDIATE NEXT ACTION

```bash
cd /home/mok/projects/nautilus-dinger/memory-bank
cat QUICK_START_CHECKLIST.md
# Start with Phase 1: Backup & Setup
```

---

**DOCUMENTATION COMPLETE**  
**READY TO IMPLEMENT**  
**FOLLOW QUICK_START_CHECKLIST.md**


---

## 🚨 CRITICAL ADDITIONS

### RECONCILIATION_LOGIC.md (NEW - CRITICAL)
**Purpose:** Explain reconciliation requirements (MANDATORY)  
**Priority:** CRITICAL - Must implement in Phase 1

**Contents:**
- Why reconciliation is critical
- REST-authoritative pattern
- Implementation requirements (3 methods + fill tracking)
- Fill deduplication strategy
- Code examples from OKX
- Common mistakes to avoid
- Validation tests

**Why Critical:**
- Prevents state desync on reconnection
- Ensures no lost orders/fills
- Required by Nautilus best practices
- Production safety requirement

**Implementation:**
- Task 6 in Phase 1
- ~50-100 LOC
- 1-2 hours
- Must be done before Rust layer

**READ THIS:** Reconciliation is NOT optional - it's a critical safety requirement.

---

### KEY_IMPROVEMENTS.md (NEW - COMPARISON)
**Purpose:** Show before/after improvements from prototype to production

**Contents:**
- 6 key improvements with benchmarks
- Before vs After code examples
- Performance gains (100x faster state access)
- Reliability improvements
- Production readiness metrics

**Why Important:**
- Understand what was wrong
- See what's needed
- Justify the work
- Learn from mistakes

**Highlights:**
- State Management: 100x faster ⚡
- Reconciliation: Prevents races ✅
- Event Emission: Nautilus compliant ✅
- Subscription Tracking: Retry + backoff ✅
- Connection State: 7-state machine ✅
- Tests: Production ready ✅

---
