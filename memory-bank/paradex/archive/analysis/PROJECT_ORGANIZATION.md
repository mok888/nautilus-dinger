# PROJECT ORGANIZATION & DOCUMENTATION STANDARDS

**Date:** 2026-01-27  
**Purpose:** Define file organization and documentation requirements  
**Status:** MANDATORY - Follow strictly

---

## 📁 FILE ORGANIZATION

### Directory Structure:

```
/home/mok/projects/nautilus-dinger/
├── memory-bank/                          # Documentation & tracking
│   ├── README.md
│   ├── INDEX.md
│   ├── AGENTS.md
│   ├── progress.md                       # Project progress tracking
│   ├── bug-fixes-record.md              # Bug fixes log
│   ├── improvements-log.md              # Improvements tracking
│   ├── validation-results.md            # Validation test results
│   ├── [implementation files].py        # Reference implementations
│   └── [documentation files].md         # Guides and references
│
├── tests/                                # All test files here
│   ├── validation/                      # Validation scripts
│   │   ├── validate_compliance.py
│   │   ├── count_methods.py
│   │   ├── check_imports.py
│   │   └── syntax_check.py
│   │
│   ├── unit/                            # Unit tests
│   │   ├── test_data_client.py
│   │   ├── test_execution_client.py
│   │   └── test_providers.py
│   │
│   └── integration/                     # Integration tests
│       └── adapters/
│           └── paradex/
│               ├── test_compliance.py
│               ├── test_data.py
│               └── test_execution.py
│
└── nautilus_trader/                     # Production code
    └── adapters/
        └── paradex/
            ├── __init__.py
            ├── config.py
            ├── data.py
            ├── execution.py
            ├── providers.py
            └── factories.py
```

---

## 🧪 TEST FILES LOCATION

### Rule: ALL test files go in `/tests/` directory

### Validation Scripts (`tests/validation/`):

**Purpose:** Automated validation and compliance checking

**Files:**
```
tests/validation/
├── validate_compliance.py    # Main compliance checker
├── count_methods.py          # Method counter
├── check_imports.py          # Import validator
├── syntax_check.py           # Syntax validator
└── README.md                 # Validation guide
```

**Usage:**
```bash
cd /home/mok/projects/nautilus-dinger/tests/validation
python validate_compliance.py
```

### Unit Tests (`tests/unit/`):

**Purpose:** Test individual components in isolation

**Files:**
```
tests/unit/
├── test_data_client.py       # Data client tests
├── test_execution_client.py  # Execution client tests
├── test_providers.py         # Provider tests
├── test_factories.py         # Factory tests
└── conftest.py               # Shared fixtures
```

### Integration Tests (`tests/integration/adapters/paradex/`):

**Purpose:** Test components working together

**Files:**
```
tests/integration/adapters/paradex/
├── test_compliance.py        # Compliance tests
├── test_data.py              # Data client integration
├── test_execution.py         # Execution client integration
└── conftest.py               # Shared fixtures
```

---

## 📝 DOCUMENTATION REQUIREMENTS

### Bug Fixes (`memory-bank/bug-fixes-record.md`):

**Format:**
```markdown
## Bug Fix #[NUMBER] - [DATE]

**Issue:** [Description of the bug]

**Location:** [File and line number]

**Root Cause:** [Why it happened]

**Fix Applied:**
```python
# Before:
[old code]

# After:
[new code]
```

**Validation:**
- [ ] Syntax check passed
- [ ] Tests pass
- [ ] No regressions

**Impact:** [What changed]

**Committed:** [Git commit hash]

---
```

**Example:**
```markdown
## Bug Fix #001 - 2026-01-27

**Issue:** Wrong method signature in _subscribe_trade_ticks

**Location:** data.py, line 85

**Root Cause:** Method accepted raw InstrumentId instead of command object

**Fix Applied:**
```python
# Before:
async def _subscribe_trade_ticks(self, instrument_id: InstrumentId) -> None:

# After:
async def _subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
```

**Validation:**
- [x] Syntax check passed
- [x] Import test passed
- [x] Signature matches OKX pattern

**Impact:** Now compliant with Nautilus specification

**Committed:** abc123def

---
```

### Improvements (`memory-bank/improvements-log.md`):

**Format:**
```markdown
## Improvement #[NUMBER] - [DATE]

**Type:** [Performance/Feature/Refactor/Documentation]

**Description:** [What was improved]

**Motivation:** [Why it was needed]

**Changes:**
- Change 1
- Change 2

**Before/After:**
```python
# Before:
[old code]

# After:
[new code]
```

**Metrics:**
- Performance: [if applicable]
- LOC: [lines added/removed]
- Complexity: [if applicable]

**Validation:**
- [ ] Tests updated
- [ ] Documentation updated
- [ ] No regressions

---
```

### Validation Results (`memory-bank/validation-results.md`):

**Format:**
```markdown
## Validation Run - [DATE] [TIME]

**Phase:** [Phase number and name]

**Validation Type:** [Syntax/Import/Compliance/Integration]

**Command:**
```bash
[command executed]
```

**Output:**
```
[full output]
```

**Status:** ✅ PASS / ❌ FAIL

**Metrics:**
- Methods: __/__
- Syntax errors: __
- Import errors: __
- Coverage: __%

**Issues Found:**
1. [Issue 1]
2. [Issue 2]

**Actions Taken:**
1. [Action 1]
2. [Action 2]

---
```

---

## 🔄 WORKFLOW

### When Fixing a Bug:

1. **Identify the bug**
   ```bash
   # Run validation to find issue
   cd tests/validation
   python validate_compliance.py
   ```

2. **Document in bug-fixes-record.md**
   - Create new entry with bug number
   - Describe issue, location, root cause

3. **Fix the bug**
   - Apply fix in production code
   - Update tests if needed

4. **Validate the fix**
   ```bash
   # Run validation again
   python validate_compliance.py
   ```

5. **Update documentation**
   - Add validation results
   - Mark fix as complete
   - Commit with reference to bug number

### When Making an Improvement:

1. **Document in improvements-log.md**
   - Create new entry with improvement number
   - Describe what and why

2. **Implement the improvement**
   - Make changes
   - Update tests

3. **Validate**
   ```bash
   # Run relevant tests
   pytest tests/unit/test_[module].py
   ```

4. **Update documentation**
   - Add metrics
   - Mark as complete
   - Commit

### When Running Validation:

1. **Execute validation script**
   ```bash
   cd tests/validation
   python validate_compliance.py > ../../memory-bank/validation-results.md
   ```

2. **Review results**
   - Check pass/fail status
   - Note any issues

3. **Document in validation-results.md**
   - Append new validation run
   - Include full output
   - List actions taken

4. **Fix issues if any**
   - Follow bug fix workflow
   - Re-validate

---

## 📋 MANDATORY DOCUMENTATION CHECKLIST

### After Every Code Change:

- [ ] Bug fix documented in `bug-fixes-record.md`
- [ ] Improvement documented in `improvements-log.md`
- [ ] Validation run documented in `validation-results.md`
- [ ] Tests updated in `tests/` directory
- [ ] Progress updated in `progress.md`
- [ ] Git commit with reference number

### After Every Validation:

- [ ] Results saved to `validation-results.md`
- [ ] Issues logged in `bug-fixes-record.md`
- [ ] Actions documented
- [ ] Re-validation scheduled if needed

### After Every Phase:

- [ ] Phase completion documented in `progress.md`
- [ ] All bugs fixed and documented
- [ ] All validations passed and documented
- [ ] Ready for next phase

---

## 🎯 DOCUMENTATION STANDARDS

### File Naming:
- Use kebab-case: `bug-fixes-record.md`
- Be descriptive: `validation-results.md`
- Include dates in entries: `2026-01-27`

### Entry Numbering:
- Bugs: `#001`, `#002`, etc.
- Improvements: `#001`, `#002`, etc.
- Validations: Use date-time

### Code Blocks:
- Always use syntax highlighting
- Show before/after for changes
- Include file paths

### Status Indicators:
- ✅ PASS
- ❌ FAIL
- ⏳ IN PROGRESS
- 🔄 RE-VALIDATING

### Metrics:
- Always include numbers
- Show before/after
- Track over time

---

## 🚫 ANTI-PATTERNS

### DON'T:
- ❌ Put test files in production directories
- ❌ Skip documentation "because it's small"
- ❌ Forget to document validation results
- ❌ Leave bugs undocumented
- ❌ Mix test types in same directory

### DO:
- ✅ Keep all tests in `tests/` directory
- ✅ Document EVERY bug fix
- ✅ Document EVERY improvement
- ✅ Save EVERY validation result
- ✅ Update progress regularly

---

## 📊 TRACKING METRICS

### In bug-fixes-record.md:
- Total bugs fixed
- Bugs by category
- Average fix time
- Regression count

### In improvements-log.md:
- Total improvements
- Improvements by type
- LOC impact
- Performance gains

### In validation-results.md:
- Validation runs
- Pass/fail rate
- Issues found
- Time to fix

### In progress.md:
- Phases completed
- Current phase
- Blockers
- Next steps

---

## 🎯 AGENT INSTRUCTIONS

### When You Fix a Bug:

1. Create entry in `memory-bank/bug-fixes-record.md`
2. Include all required fields
3. Show before/after code
4. Run validation
5. Document validation results
6. Update progress

### When You Make an Improvement:

1. Create entry in `memory-bank/improvements-log.md`
2. Explain motivation
3. Show changes
4. Include metrics
5. Run tests
6. Document results

### When You Run Validation:

1. Execute from `tests/validation/`
2. Save output to `memory-bank/validation-results.md`
3. Document issues found
4. Create bug entries if needed
5. Track metrics

### Always:

- Keep tests in `tests/` directory
- Document in `memory-bank/`
- Update progress regularly
- Track all metrics
- Reference entry numbers in commits

---

## 📁 QUICK REFERENCE

**Test Files:** `/tests/`  
**Documentation:** `/memory-bank/`  
**Production Code:** `/nautilus_trader/adapters/paradex/`

**Bug Fixes:** `memory-bank/bug-fixes-record.md`  
**Improvements:** `memory-bank/improvements-log.md`  
**Validation:** `memory-bank/validation-results.md`  
**Progress:** `memory-bank/progress.md`

---

**FOLLOW THIS ORGANIZATION STRICTLY**  
**DOCUMENT EVERYTHING**  
**KEEP TESTS SEPARATE FROM PRODUCTION CODE**
