# INSTRUCTIONS FOR CODING AGENT

## 📝 RECORDING SUCCESSFUL PATTERNS

### CRITICAL: Log After EVERY Task

After completing ANY task (method implementation, bug fix, test, etc.), immediately record what worked in the learning log.

---

## 🎯 STEP-BY-STEP INSTRUCTIONS

### 1. Complete a Task
```bash
# Example: Implement _reconcile_state() method
vim nautilus_trader/adapters/paradex/execution.py
# ... implement method ...
pytest tests/unit/test_reconciliation.py -v
# ✅ Tests pass
```

### 2. Immediately Open Learning Log
```bash
vim memory-bank/tracking/learning-log.md
```

### 3. Add Entry Using Template
```markdown
### 2026-01-28 - Phase 1 - Reconciliation Implementation

**What Worked:** Implemented reconciliation with fill deduplication
**Why It Worked:** Used set to track emitted fills, prevents duplicates
**Reusable Pattern:** Always deduplicate events using unique ID in a set
**Code:**
```python
self._emitted_fills: set[TradeId] = set()

async def _reconcile_state(self):
    fills = await self._http_client.get_fills()
    for fill_data in fills:
        trade_id = TradeId(fill_data["trade_id"])
        if trade_id not in self._emitted_fills:
            self._send_fill_report(fill_data)
            self._emitted_fills.add(trade_id)
```
**Time Saved:** Prevented HIGH severity duplicate fill bug
**Reference:** execution.py:245-255, commit abc123

**Key Insight:** REST is authoritative, WebSocket can send duplicates
```

### 4. Save and Continue
```bash
:wq
# Continue with next task
```

---

## 📋 WHAT TO LOG

### ✅ Always Log These:

**1. Successful Implementations**
- What: Method/feature implemented
- Why: Approach taken
- Pattern: How to reuse
- Code: Working snippet

**2. Bug Fixes**
- What: Bug fixed
- Why: Root cause
- Pattern: How to prevent
- Code: Fix applied

**3. Performance Wins**
- What: Optimization applied
- Why: Performance improved
- Pattern: When to use
- Code: Optimized code
- Metrics: Before/after numbers

**4. API Discoveries**
- What: API behavior discovered
- Why: Differs from documentation
- Pattern: How to handle
- Code: Workaround

**5. Testing Insights**
- What: Test approach that worked
- Why: Caught bugs effectively
- Pattern: Testing strategy
- Code: Test example

**6. Debugging Breakthroughs**
- What: How bug was found
- Why: Root cause
- Pattern: Diagnostic technique
- Code: Fix

---

## 🚫 ALSO LOG ANTI-PATTERNS

### When Something Goes Wrong:

```markdown
### 2026-01-28 - ANTI-PATTERN: Validated at End Only

**What Happened:** Implemented 10 methods, validated at end
**Result:** Found 5 bugs, spent 3h isolating which method caused which bug
**Lesson:** Validate after EACH method, not at end
**Fix:** Incremental validation - run tests after each method
**Time Lost:** 3h
**Prevention:** 
```bash
# After EACH method:
python -m py_compile file.py
pytest tests/unit/test_specific_method.py -v
```
```

---

## ⏰ WHEN TO LOG

### Timing is Critical:

**✅ BEST: Immediately after task completion**
- Details are fresh
- Code is in front of you
- Takes 2-3 minutes

**⚠️ ACCEPTABLE: End of work session**
- Review completed tasks
- Log each one
- Takes 10-15 minutes

**❌ TOO LATE: Next day or later**
- You'll forget details
- Code context is lost
- Takes 30+ minutes to reconstruct

---

## 📊 TRACK METRICS

### Update These Regularly:

```markdown
## Time Savings Tracker
| Date | Improvement | Time Saved | Cumulative |
|------|-------------|------------|------------|
| 01-28 | Dependency analysis | 5h | 5h |
| 01-28 | Mock infrastructure | 10h | 15h |
| 01-28 | Incremental validation | 8h | 23h |

## Bug Prevention Tracker
| Date | Practice | Bugs Prevented | Severity |
|------|----------|----------------|----------|
| 01-28 | Reconciliation-first | 3 | HIGH |
| 01-28 | Mock testing | 2 | LOW |
```

---

## 🔄 DAILY WORKFLOW

### Morning Routine:
```bash
# 1. Review yesterday's learnings
tail -30 memory-bank/tracking/learning-log.md

# 2. Check for patterns to apply today
grep "Reusable Pattern:" memory-bank/tracking/learning-log.md | tail -5
```

### After Each Task:
```bash
# 1. Complete task
# 2. Validate it works
# 3. IMMEDIATELY log it
vim memory-bank/tracking/learning-log.md
# 4. Continue to next task
```

### End of Day:
```bash
# 1. Review all entries from today
grep "2026-01-28" memory-bank/tracking/learning-log.md

# 2. Summarize top 3 wins
# 3. Update metrics
# 4. Identify patterns
```

---

## 💡 EXAMPLES OF GOOD ENTRIES

### Example 1: Technical Pattern
```markdown
### 2026-01-28 - Phase 1 - Helper Method Extraction

**What Worked:** Extracted _to_pyo3_instrument_id() helper method
**Why It Worked:** Eliminated duplicate conversion code in 6 methods
**Reusable Pattern:** Extract helper for repeated conversions
**Code:**
```python
def _to_pyo3_instrument_id(self, instrument_id: InstrumentId) -> nautilus_pyo3.InstrumentId:
    return nautilus_pyo3.InstrumentId.from_str(instrument_id.value)

# Use in all subscription methods:
async def _subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
    pyo3_id = self._to_pyo3_instrument_id(command.instrument_id)
    await self._ws_client.subscribe_trades(pyo3_id)
```
**Time Saved:** 30 min (avoided 6 duplicate implementations)
**Reference:** data.py:89-91

**Key Insight:** DRY principle - extract common patterns early
```

### Example 2: Process Improvement
```markdown
### 2026-01-28 - Phase 1 - Incremental Validation

**What Worked:** Validated each method immediately after implementation
**Why It Worked:** Caught syntax errors and import issues before moving on
**Reusable Pattern:** After each method, run:
```bash
python -m py_compile file.py
pytest tests/unit/test_specific_method.py -v
```
**Time Saved:** 8h (avoided debugging 10 methods at once)
**Reference:** WORKFLOW_V2.md Phase 1

**Key Insight:** Validate early, validate often - bugs don't compound
```

### Example 3: API Discovery
```markdown
### 2026-01-28 - Phase 0 - Paradex Timestamp Format

**What Worked:** Discovered Paradex uses milliseconds, not nanoseconds
**Why It Worked:** Tested real API before implementation
**Reusable Pattern:** Always verify timestamp format with real API
**Code:**
```python
# Nautilus uses nanoseconds, Paradex uses milliseconds
def to_paradex_timestamp(nautilus_ts_ns: int) -> int:
    return nautilus_ts_ns // 1_000_000

def to_nautilus_timestamp(paradex_ts_ms: int) -> int:
    return paradex_ts_ms * 1_000_000
```
**Time Saved:** 2h (avoided debugging timestamp mismatches)
**Reference:** exploration/notes.md

**Key Insight:** API docs are often incomplete - test everything
```

---

## 🎯 SUCCESS METRICS

### Your Learning Log is Successful When:

1. ✅ You can find solutions to similar problems quickly
2. ✅ You avoid repeating mistakes
3. ✅ You can onboard new developers faster
4. ✅ You have concrete metrics on time saved
5. ✅ You can extract reusable patterns for future projects

### Track These:
- **Entries per day:** Target 5-10
- **Time saved:** Track cumulative
- **Bugs prevented:** Track by severity
- **Patterns identified:** Track reusable patterns
- **Anti-patterns avoided:** Track mistakes prevented

---

## 📚 RELATED FILES

```bash
# Main learning log
memory-bank/tracking/learning-log.md

# Quick reference
memory-bank/tracking/learning-log-quick-ref.md

# Other tracking
memory-bank/tracking/bug-fixes-record.md
memory-bank/tracking/improvements-log.md
memory-bank/tracking/progress.md
```

---

## 🚀 START NOW

### Your First Entry:

```bash
vim memory-bank/tracking/learning-log.md
```

Add:
```markdown
### 2026-01-28 - Setup - Learning Log System

**What Worked:** Created learning log to capture successful patterns
**Why It Worked:** Systematic approach to knowledge capture
**Reusable Pattern:** Log after every task completion
**Time Saved:** Will save hours in future projects by avoiding repeated mistakes
**Reference:** learning-log.md, learning-log-quick-ref.md

**Key Insight:** Every minute spent logging saves 10 minutes in the future
```

---

## ⚡ QUICK TEMPLATE (Copy-Paste)

```markdown
### [DATE] - [PHASE] - [TASK]

**What Worked:** 
**Why It Worked:** 
**Reusable Pattern:** 
**Code:**
```[language]
[code snippet]
```
**Time Saved:** 
**Reference:** 

**Key Insight:** 
```

---

**Remember:** The best developers don't just write code - they capture and share knowledge!

**Action:** After completing your next task, log it immediately using this template.
