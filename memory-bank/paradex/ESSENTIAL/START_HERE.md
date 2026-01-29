# START HERE - PARADEX NAUTILUS ADAPTER

**Last Updated:** 2026-01-27  
**Status:** Ready to Implement  
**Completion:** 20% (planning done)

---

## 🎯 WHAT IS THIS?

Building a **production-grade Nautilus Trader adapter** for Paradex (StarkNet perpetual futures exchange).

**Goal:** 100% compliant with [Nautilus adapter specification](https://nautilustrader.io/docs/latest/developer_guide/adapters/)

---

## 📋 CURRENT STATUS

### Completed ✅
- Planning and documentation (20%)
- Bug analysis (12 bugs identified)
- Reference code templates created
- Testnet configuration ready

### To Do ❌
- Phase 1: Python layer fixes (12.5h)
- Phase 2: Rust core implementation (38h)
- Phase 3: Full system testing (14h)
- Phase 4: Documentation polish (3.5h)

**Total Remaining:** 68 hours, 1,100-1,400 credits

---

## 🚀 QUICK START

### 1. Install Nautilus Trader (5 min)
```bash
# Install Nautilus Trader via pip
pip install nautilus_trader

# Verify installation
python -c "import nautilus_trader; print(f'Nautilus Trader {nautilus_trader.__version__} installed')"
```

### 2. Read Documentation (30 min)
```bash
cd /home/mok/projects/nautilus-dinger/memory-bank/ESSENTIAL

# Read in order:
cat START_HERE.md            # This file - overview
cat WORKFLOW_COMPARISON.md   # Choose your workflow (V1 vs V2 vs V3)
cat WORKFLOW.md              # V1: Original (68h, simpler)
cat WORKFLOW_V2.md           # V2: Improved (85.5h, production-ready)
cat WORKFLOW_V3.md           # V3: Critical Path (85.5h, dependency-aware) ⭐ RECOMMENDED
cat PATTERNS.md              # Code patterns to copy
cat BUGS.md                  # Known issues to fix
cat CONFIG.md                # Configuration details
```

### 3. Review Reference Code (15 min)
```bash
# Python templates
ls -l reference/python/
# data.py, execution.py, providers.py, factories.py, config.py, constants.py, __init__.py

# Rust templates
ls -l reference/rust/
# lib.rs, config.rs, error.rs, Cargo.toml
```

### 4. Check Progress (5 min)
```bash
cat tracking/progress.md
cat tracking/bug-fixes-record.md
```

### 5. Begin Implementation
```bash
# Follow WORKFLOW.md Phase 1
cat ESSENTIAL/WORKFLOW.md
```

---

## 📁 PROJECT STRUCTURE

```
/home/mok/projects/nautilus-dinger/
├── memory-bank/
│   ├── ESSENTIAL/              # 5 core docs - READ THESE
│   │   ├── START_HERE.md       # This file
│   │   ├── WORKFLOW.md         # Implementation steps
│   │   ├── PATTERNS.md         # Code patterns
│   │   ├── BUGS.md             # Known issues
│   │   └── CONFIG.md           # Configuration
│   │
│   ├── reference/              # Code templates
│   │   ├── python/             # 7 Python files
│   │   └── rust/               # 4 Rust files
│   │
│   ├── tracking/               # Progress tracking
│   │   ├── progress.md
│   │   ├── bug-fixes-record.md
│   │   ├── improvements-log.md
│   │   └── validation-results.md
│   │
│   └── archive/                # Historical docs
│
├── .env.testnet                # Testnet credentials
└── .gitignore                  # Security
```

---

## 🎯 IMPLEMENTATION PHASES

### Phase 1: Python Layer (12.5h, 200-250 credits)
- Fix 6 method signatures
- Add 32 missing methods
- Implement reconciliation logic
- Refactor and test
- **Deliverable:** Working Python adapter

### Phase 2: Rust Core (38h, 650-800 credits)
- HTTP client with JWT auth
- WebSocket client with JSON-RPC
- STARK signing module
- PyO3 bindings
- State management (DashMap)
- **Deliverable:** Complete Rust layer

### Phase 3: Testing (14h, 180-250 credits)
- Unit tests (85%+ coverage)
- Integration tests
- Performance optimization
- Bug fixes
- **Deliverable:** Production-ready code

### Phase 4: Documentation (3.5h, 40-60 credits)
- Update docs
- Create examples
- Final review
- **Deliverable:** Complete package

---

## 🔑 KEY CONCEPTS

### 1. REST-Authoritative Pattern
- **Never trust WebSocket data alone**
- Always reconcile from REST API on connect
- Periodic reconciliation (default: 5 min)

### 2. Idempotent Operations
- Safe to restart/reconnect anytime
- No duplicate fills
- Track emitted events

### 3. STARK Signatures
- All orders require StarkNet signing
- Use subkey (safer than main account)
- Implemented in Rust layer

### 4. Compliance Requirements
- 38 data client methods (8 base + 30 missing)
- 12 execution client methods (10 base + 2 missing)
- Proper event emission
- Full type safety

---

## 📊 KNOWN ISSUES

### Python Layer (3 bugs):
- Bug #001: Wrong method signatures (6 methods)
- Bug #002: Missing 30 data methods
- Bug #003: Missing 2 execution methods

### Rust Layer (9 bugs):
- Bug #004: Using RwLock (should use DashMap)
- Bug #005: Reconciliation is stub
- Bug #006: Subscription tracking too simple
- Bug #007: Boolean connection state (needs state machine)
- Bug #008: No race condition prevention
- Bug #009: Wrong event types
- Bug #010: Instrument parsing returns None
- Bug #011: Message handlers are stubs
- Bug #012: No integration tests

**See BUGS.md for details**

---

## 🔧 TESTNET CONFIGURATION

### Credentials (already configured):
```bash
# Location: /home/mok/projects/nautilus-dinger/.env.testnet
PARADEX_ENVIRONMENT=testnet
PARADEX_L2_ADDRESS=0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8
PARADEX_SUBKEY_PRIVATE_KEY=0x0441c1622edc5a77891cf97cd76c4ff097211f3df4493425fb9519e06ff8cf55
```

**See CONFIG.md for full setup**

---

## 📚 REFERENCE SOURCES

### Official Documentation:
- [Nautilus Adapter Guide](https://nautilustrader.io/docs/latest/developer_guide/adapters/)
- [Paradex API Docs](https://docs.paradex.trade/)

### Reference Implementations:
- OKX adapter (primary reference)
- BitMEX adapter (secondary)
- Bybit adapter (secondary)

### Code Templates:
- `reference/python/` - Python adapter templates
- `reference/rust/` - Rust core templates

---

## ✅ NEXT STEPS

1. **Read WORKFLOW.md** - Understand the implementation process
2. **Read PATTERNS.md** - Learn code patterns to use
3. **Read BUGS.md** - Understand what needs fixing
4. **Start Phase 1** - Begin Python layer implementation

---

## 💡 TIPS

- **Use existing code:** Fetch from OKX adapter, don't reinvent
- **Validate frequently:** After every change
- **Document everything:** Track bugs, improvements, progress
- **Test as you go:** Don't wait until the end
- **Follow patterns:** Use proven Nautilus patterns

---

## 📞 HELP

### Stuck? Check:
1. WORKFLOW.md - Step-by-step guide
2. PATTERNS.md - Code examples
3. BUGS.md - Known issues and solutions
4. tracking/progress.md - Current status

### Need More Info?
- See archive/ for detailed analysis documents
- Check reference/ for code templates

---

**Ready to begin? → Read WORKFLOW.md next**
