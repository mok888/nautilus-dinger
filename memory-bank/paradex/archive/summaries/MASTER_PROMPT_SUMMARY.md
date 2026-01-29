# MASTER AGENT PROMPT CREATED - FINAL SUMMARY

**Date:** 2026-01-27  
**Update:** Created comprehensive master agent prompt  
**Status:** ✅ COMPLETE

---

## 🎯 WHAT WAS CREATED

### MASTER_AGENT_PROMPT.md (New Document)

**Purpose:** Single source of truth for all agent instructions

**Key Sections:**

1. **Critical Rules (NEVER VIOLATE)**
   - Read before coding
   - Use existing code (don't reinvent)
   - Validate after every change
   - Document everything
   - Follow official patterns exactly

2. **DO's (Required Practices)**
   - Use official reference code
   - Follow file organization
   - Validate continuously
   - Document changes
   - Use glue coding

3. **DON'Ts (Forbidden Practices)**
   - Write code from scratch
   - Skip documentation
   - Mix file types
   - Skip validation
   - Deviate from spec

4. **Required Skills**
   - Technical: Python, Rust, Git, Testing, APIs
   - Domain: Nautilus, Paradex, StarkNet, Trading
   - Soft: Reading, Pattern recognition, Detail, Documentation

5. **Workflow (Follow Exactly)**
   - Step 1: Preparation (read docs)
   - Step 2: Fetch reference code
   - Step 3: Implement with validation
   - Step 4: Document
   - Step 5: Validate & iterate

6. **Code Fetching Strategy**
   - Always fetch from GitHub first
   - Copy OKX adapter patterns
   - Adapt for Paradex specifics
   - Use glue coding approach

7. **Progress Tracking**
   - Current status
   - Next actions
   - Completion metrics

8. **Success Checklist**
   - Python layer criteria
   - Rust layer criteria
   - Project completion criteria

---

## 🚨 CRITICAL EMPHASIS

### Rule #1: READ BEFORE CODING

**MANDATORY Reading (in order):**
1. PROJECT_ORGANIZATION.md (5 min)
2. progress.md (2 min)
3. bug-fixes-record.md (3 min)
4. COMPLIANCE_AUDIT.md (10 min)
5. STUDY_COMPLETE_SUMMARY.md (10 min)

**Why:** Understand current state, avoid duplication, know what needs fixing.

### Rule #2: USE EXISTING CODE

**Process:**
1. Search GitHub FIRST
2. Fetch OKX adapter code
3. Copy the pattern
4. Adapt for Paradex
5. Validate

**Example:**
```bash
# WRONG: Writing from scratch
# Writing 50 lines of new code...

# RIGHT: Fetch and adapt
# 1. web_fetch OKX implementation
# 2. Copy pattern
# 3. Change only Paradex-specific parts
```

**Emphasis:**
- ✅ **Glue coding** - Connect existing components
- ✅ **Pattern reuse** - Copy proven patterns
- ✅ **Minimal custom code** - Only what's necessary
- ❌ **Reinventing wheel** - Never do this

### Rule #3: VALIDATE CONTINUOUSLY

**After EVERY:**
- Phase
- File
- Change
- Commit

**Commands:**
```bash
python -m py_compile [file].py
python tests/validation/validate_compliance.py
```

**If FAIL:**
1. STOP
2. Document bug
3. Fix
4. Re-validate
5. Continue

### Rule #4: DOCUMENT EVERYTHING

**Update After EVERY Change:**
- Bug fix → bug-fixes-record.md
- Improvement → improvements-log.md
- Validation → validation-results.md
- Progress → progress.md

**No Exceptions:**
- Not "too small"
- Not "later"
- Not "obvious"
- Document NOW

---

## 📋 WORKFLOW SUMMARY

### Before Coding:
```bash
# 1. Read master prompt
cat MASTER_AGENT_PROMPT.md

# 2. Check status
cat progress.md
cat bug-fixes-record.md

# 3. Understand gaps
cat COMPLIANCE_AUDIT.md
```

### During Coding:
```bash
# 1. Fetch reference
# Use web_fetch to get OKX code

# 2. Implement
# Copy pattern, adapt for Paradex

# 3. Validate
python -m py_compile [file].py

# 4. Document
vim bug-fixes-record.md
```

### After Coding:
```bash
# 1. Final validation
python tests/validation/validate_compliance.py

# 2. Update docs
vim progress.md

# 3. Commit
git commit -m "Fix #001: Description"
```

---

## 🎯 KEY PRINCIPLES

### 1. Read First, Code Later
- Understand before implementing
- Know what exists
- Avoid duplication

### 2. Copy, Don't Create
- Use official patterns
- Fetch from GitHub
- Adapt, don't reinvent

### 3. Validate Always
- After every change
- Before proceeding
- Document results

### 4. Document Everything
- Bugs
- Improvements
- Validations
- Progress

### 5. Follow Spec Exactly
- Zero deviation
- Match signatures
- Complete implementation

---

## 📊 CURRENT STATUS

### Project:
- **Completion:** 20%
- **Phase:** Planning
- **Compliance:** ❌ NOT COMPLIANT

### Known Issues:
- **Bug #001:** Wrong signatures (6 methods)
- **Bug #002:** Missing methods (30 methods)
- **Bug #003:** Missing execution methods (2 methods)

### Next Actions:
1. Read MASTER_AGENT_PROMPT.md
2. Read all required docs
3. Fetch OKX adapter code
4. Start Phase 1 fixes
5. Validate continuously

---

## 🚀 HOW TO USE

### For New Agents:
```bash
# Start here
cd /home/mok/projects/nautilus-dinger/memory-bank
cat MASTER_AGENT_PROMPT.md

# Read everything in "Required Reading" section
# Follow workflow exactly
# Use code fetching strategy
```

### For Resuming Work:
```bash
# 1. Check status
cat progress.md
cat bug-fixes-record.md

# 2. Review master prompt
cat MASTER_AGENT_PROMPT.md

# 3. Continue from last checkpoint
cat QUICK_START_WITH_VALIDATION.md
```

### For Reference:
```bash
# Rules and workflow
cat MASTER_AGENT_PROMPT.md

# Code patterns
cat NAUTILUS_PATTERNS_REFERENCE.md

# Implementation guide
cat QUICK_START_WITH_VALIDATION.md
```

---

## ✅ BENEFITS

### For Agents:
- Clear instructions
- No ambiguity
- Step-by-step workflow
- Success criteria defined

### For Project:
- Consistent approach
- Quality assurance
- Complete documentation
- Faster development

### For Code:
- Proven patterns
- Minimal custom code
- High quality
- Fully compliant

---

## 📚 UPDATED DOCUMENTS

### New:
- **MASTER_AGENT_PROMPT.md** - Complete agent instructions

### Updated:
- **INDEX.md** - Added master prompt as #0 (read first)
- **Reading order** - Prioritizes master prompt
- **Quick start** - Includes master prompt

---

## 🎯 FINAL INSTRUCTIONS

### For Any Agent Starting Work:

1. **READ FIRST:**
   ```bash
   cat memory-bank/MASTER_AGENT_PROMPT.md
   ```

2. **FOLLOW RULES:**
   - Read before coding
   - Use existing code
   - Validate continuously
   - Document everything

3. **USE WORKFLOW:**
   - Preparation → Fetch → Implement → Document → Validate

4. **FETCH CODE:**
   - Always check GitHub first
   - Copy OKX patterns
   - Adapt for Paradex

5. **VALIDATE ALWAYS:**
   - After every change
   - Document results
   - Fix immediately if fail

---

**MASTER PROMPT CREATED**  
**ALL RULES DEFINED**  
**WORKFLOW ESTABLISHED**  
**READY FOR IMPLEMENTATION**

**START HERE:** `cat memory-bank/MASTER_AGENT_PROMPT.md`
