# MEMORY-BANK REORGANIZATION PLAN

## CURRENT STATE: 32 MD files + 10 code files = TOO MUCH

## PROPOSED STRUCTURE:

```
memory-bank/
├── ESSENTIAL/                    # Only what's needed for implementation
│   ├── START_HERE.md            # Consolidated quick start
│   ├── WORKFLOW.md              # Step-by-step implementation
│   ├── PATTERNS.md              # Code patterns to copy
│   ├── BUGS.md                  # Known issues
│   └── CONFIG.md                # Configuration guide
│
├── reference/                    # Reference code templates
│   ├── python/
│   │   ├── data.py
│   │   ├── execution.py
│   │   ├── providers.py
│   │   ├── factories.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   └── __init__.py
│   └── rust/
│       ├── lib.rs
│       ├── config.rs
│       └── error.rs
│
├── tracking/                     # Progress tracking
│   ├── progress.md
│   ├── bug-fixes-record.md
│   ├── improvements-log.md
│   └── validation-results.md
│
└── archive/                      # Historical/redundant docs
    ├── summaries/
    ├── old-guides/
    └── analysis/
```

## CONSOLIDATION PLAN:

### Create 5 Essential Docs (from 32):

**1. START_HERE.md** (consolidate from):
- INDEX.md
- README.md
- START_HERE_QUICK_GUIDE.md
- AGENTS.md

**2. WORKFLOW.md** (consolidate from):
- MASTER_AGENT_PROMPT.md
- QUICK_START_WITH_VALIDATION.md
- 3_IMPLEMENTATION_ROADMAP.md
- QUICK_START_CHECKLIST.md

**3. PATTERNS.md** (consolidate from):
- NAUTILUS_PATTERNS_REFERENCE.md
- 1_RUST_CORE_IMPLEMENTATION.md
- 2_PYTHON_ADAPTER_IMPLEMENTATION.md
- MASTER_ALL_IN_ONE_COMPLETE.md

**4. BUGS.md** (consolidate from):
- COMPLIANCE_AUDIT.md
- CRITICAL_MISSING_COMPONENTS.md
- KEY_IMPROVEMENTS.md
- RECONCILIATION_LOGIC.md

**5. CONFIG.md** (consolidate from):
- TESTNET_CONFIG.md
- CREDIT_ESTIMATE.md
- PROJECT_ORGANIZATION.md

### Archive (not needed for execution):
- All *_SUMMARY.md files (7 files)
- agent-auto-validation.md
- Full-Production-Validation.md
- IMPLEMENTATION_ACTION_PLAN.md
- VALIDATION_INTEGRATION_SUMMARY.md
- UPDATE_COMPLETE.md
- REFACTORING_UPDATE_SUMMARY.md

## RESULT:
- **Before:** 32 MD files (overwhelming)
- **After:** 5 essential docs + organized reference code
- **Reduction:** 84% fewer files to navigate
