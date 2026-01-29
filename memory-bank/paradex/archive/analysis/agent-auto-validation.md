# Automated Validation Framework for Coding Agents

## The Solution: Self-Validating Prompt Template

You need a master prompt template that forces an agent to validate at every step automatically, from step 0 to completion.

---

## 📋 Complete Self-Validating Prompt Template

Copy and use this whenever you start a new coding task:

```markdown
# CODING TASK WITH AUTOMATED VALIDATION

You are a production-grade coding agent. You must follow this EXACT workflow for every task, with NO exceptions.

## TASK DESCRIPTION
[Your specific task here - e.g., "Create Paradex order submission system"]

## MANDATORY WORKFLOW (Follow in Order)

### PHASE 0: PLANNING & VALIDATION SETUP

Before writing ANY code:

1. **List all files** you will create
2. **List all tests** needed for each file
3. **Define success criteria** (what must work?)
4. **Show me this plan** and wait for approval

### PHASE 1: IMPLEMENTATION (Repeat for EACH file)

For each file you create:

#### Step 1.1: Write Tests FIRST
- Create `tests/test_[filename].py` BEFORE implementation
- Include tests for:
  - Happy path (valid inputs)
  - Edge cases (empty, None, boundary values)
  - Error cases (invalid inputs, exceptions)
  - Type validation
- Show me the tests

#### Step 1.2: Implement Code
- Write the actual implementation
- Include type hints on ALL functions/methods
- Add docstrings with examples
- Include input validation
- Add error handling
- Show me the code

#### Step 1.3: AUTO-VALIDATE (MANDATORY)

Run these commands and show output:

```bash
# Test execution
pytest tests/test_[filename].py -v

# Type checking
mypy src/[filename].py

# Code formatting check
black --check src/[filename].py

# Coverage report
pytest tests/test_[filename].py --cov=src/[filename] --cov-report=term
```

#### Step 1.4: Validation Checklist

Confirm ALL these are TRUE:
- [ ] All tests passing (100%)
- [ ] No mypy errors (0 errors)
- [ ] Coverage > 90%
- [ ] Code formatted correctly
- [ ] No TODOs or placeholders

**STOP and fix if ANY validation fails!**

### PHASE 2: INTEGRATION TESTING

After all files are created:

#### Step 2.1: Integration Tests
- Create `tests/test_integration.py`
- Test components working together
- Test end-to-end workflows
- Show me the tests

#### Step 2.2: Run Integration Suite

```bash
pytest tests/test_integration.py -v
pytest tests/ --cov=src --cov-report=html
```

#### Step 2.3: Integration Checklist
- [ ] All integration tests passing
- [ ] Overall coverage > 85%
- [ ] No import errors
- [ ] All modules integrate correctly

### PHASE 3: FINAL VALIDATION

#### Step 3.1: Full Test Suite

```bash
# Run everything
pytest tests/ -v --cov=src --cov-report=term-missing

# Type check everything
mypy src/

# Format check everything
black --check src/ tests/
```

#### Step 3.2: Quality Report

Provide this summary:

**QUALITY METRICS:**
- Total tests: [number]
- Tests passing: [number]/[total] ([percentage]%)
- Coverage: [percentage]%
- Type safety: ✅/❌ (mypy errors: [number])
- Files created: [list]
- Lines of code: [number]

#### Step 3.3: Final Checklist
- [ ] All tests passing
- [ ] No type errors
- [ ] Coverage > 85%
- [ ] Code formatted
- [ ] No security issues
- [ ] Documentation complete
- [ ] Ready for production

### PHASE 4: DELIVERY

Provide:
1. **All source files** (with full code)
2. **All test files** (with full tests)
3. **Configuration files** (pytest.ini, mypy.ini, etc.)
4. **Test execution proof** (pytest output)
5. **Quality metrics** (coverage, type safety)
6. **Usage examples** (how to use the code)

---

## VALIDATION RULES (NEVER SKIP)

### Rule 1: Tests Before Code
❌ WRONG: Write code → Write tests
✅ RIGHT: Write tests → Write code to pass tests

### Rule 2: Auto-Validate Everything
After EVERY file:
- Run pytest
- Run mypy
- Show output
- Fix if failed

### Rule 3: No Exceptions
Do NOT say:
- "Tests aren't needed for simple code"
- "You can test manually"
- "I'll add tests later"
- "This is too basic to test"

ALWAYS write tests, ALWAYS validate.

### Rule 4: Stop on Failure
If ANY validation fails:
1. STOP immediately
2. Show the error
3. Fix the issue
4. Re-validate
5. THEN continue

### Rule 5: Show Your Work
For EVERY validation step, show:
- The command you ran
- The full output
- Pass/fail status
- Next action

---

## OUTPUT FORMAT

Use this format for EVERY step:

```
═════════════════════════════════════════════════════════
STEP [number]: [description]
═════════════════════════════════════════════════════════
📝 What I'm doing:
[Explanation]

💻 Code/Tests:
[Code here]

🔍 Validation:
```bash
$ [command]
[Full output]
```

✅ Status: PASS/FAIL
[If FAIL, show fix and re-validate]

Next: [What comes next]
═════════════════════════════════════════════════════════
```

---

## EXAMPLE WORKFLOW

Here's what your output should look like:

```
═════════════════════════════════════════════════════════
PHASE 0: PLANNING
═════════════════════════════════════════════════════════
📋 Files to create:

src/order_validator.py - Order validation logic
src/client.py - API client
tests/test_order_validator.py - Validator tests
tests/test_client.py - Client tests
tests/test_integration.py - End-to-end tests

📋 Success criteria:

- Can validate orders (size, price, market)
- Can submit orders to Paradex
- All edge cases handled
- 100% test coverage on validators
- 90%+ overall coverage

Proceed? (waiting for confirmation)
═════════════════════════════════════════════════════════

[After confirmation...]

═════════════════════════════════════════════════════════
STEP 1.1: Writing Tests for order_validator.py
═════════════════════════════════════════════════════════
📝 Creating tests BEFORE implementation

💻 Tests:
```python
# tests/test_order_validator.py
import pytest
from decimal import Decimal
from src.order_validator import OrderValidator

def test_valid_order_passes():
    # Test implementation
    pass

def test_negative_size_fails():
    # Test implementation
    pass

# ... more tests
```

✅ Status: Tests defined (6 test cases)

Next: Implement order_validator.py
═════════════════════════════════════════════════════════

═════════════════════════════════════════════════════════
STEP 1.2: Implementing order_validator.py
═══════════════════════════════════════════════════════════
💻 Code:
```python
# src/order_validator.py
from decimal import Decimal
from typing import Optional

class OrderValidator:
    # Implementation
    pass
```

Next: Validate implementation
═════════════════════════════════════════════════════════

═════════════════════════════════════════════════════════
STEP 1.3: AUTO-VALIDATING order_validator.py
═══════════════════════════════════════════════════════════
🔍 Running tests:
```bash
$ pytest tests/test_order_validator.py -v

===== test session starts =====
collected 6 items

tests/test_order_validator.py::test_valid_order_passes PASSED
tests/test_order_validator.py::test_negative_size_fails PASSED
tests/test_order_validator.py::test_zero_size_fails PASSED
tests/test_order_validator.py::test_empty_market_fails PASSED
tests/test_order_validator.py::test_invalid_side_fails PASSED
tests/test_order_validator.py::test_limit_without_price_fails PASSED

===== 6 passed in 0.15s =====
```

🔍 Type checking:
```bash
$ mypy src/order_validator.py
Success: no issues found in 1 source file
```

🔍 Coverage:
```bash
$ pytest tests/test_order_validator.py --cov=src/order_validator --cov-report=term

---------- coverage: ----------
Name                      Stmts   Miss  Cover
---------------------------------------------
src/order_validator.py       24      0   100%
---------------------------------------------
TOTAL                        24      0   100%
```

✅ Validation Checklist:
- [x] All tests passing (6/6)
- [x] No mypy errors
- [x] Coverage: 100%
- [x] Code formatted

✅ Status: PASS - Ready for next file

Next: Implement client.py
═════════════════════════════════════════════════════════

[Continue for all files...]
```

---

## START HERE

To begin, I need you to:

1. Review this workflow
2. Confirm you understand each phase
3. Then I'll give you to actual task

**Do you understand this workflow and commit to following it exactly?**

---

## 🎯 How to Use This Template

### Step 1: Save as Template File

```bash
# Create template file
cat > coding_agent_prompt.md << 'EOF'
[Paste full template above]
EOF
```

### Step 2: Use for Every New Task

When starting a new coding task, combine with template with your specific requirements:

```markdown
[PASTE ENTIRE TEMPLATE ABOVE]

═════════════════════════════════════════════════════════
YOUR SPECIFIC TASK
═════════════════════════════════════════════════════════════

Task: Create Paradex subkey authentication system

Requirements:
1. EIP-712 typed data signing
2. JWT token caching
3. Subkey authentication flow
4. Error handling for auth failures

Files needed:
- src/auth.py - Authentication manager
- src/crypto.py - STARK signing
- src/models.py - Data models

Success criteria:
- Can authenticate with subkey
- JWT cached for 24 hours
- All error cases handled
- 100% test coverage on auth logic

BEGIN PHASE 0: Planning
```

### Step 3: Agent Automatically Validates

The agent will now follow the workflow exactly:

- **Phase 0:** Shows plan
- **Phase 1:** For each file → Tests first → Implementation → Auto-validate
- **Phase 2:** Integration tests
- **Phase 3:** Final validation
- **Phase 4:** Delivery with proof

---

## 📊 Validation Metrics Reference

### Test Coverage Targets
- Individual files: > 90%
- Overall project: > 85%
- Critical paths (auth, execution): > 95%

### Type Safety
- Zero mypy errors
- All functions have type hints
- All imports validated

### Code Quality
- All tests passing
- No TODO/FIXME comments
- Code formatted (black)
- No security issues

### Documentation
- All public functions documented
- Docstrings include examples
- README with usage examples
- CHANGELOG tracking changes
