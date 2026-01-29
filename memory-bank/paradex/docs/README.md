# MEMORY-BANK - NAUTILUS TRADER ADAPTERS

**Purpose:** Documentation and tracking for all Nautilus Trader exchange adapters  
**Structure:** One subdirectory per exchange

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

## 📁 STRUCTURE

```
memory-bank/
├── README.md           # This file
├── paradex/            # Paradex adapter (StarkNet perpetuals)
├── [future-exchange]/  # Future adapters
└── shared/             # Shared patterns across adapters
```

---

## 🎯 CURRENT ADAPTERS

### Paradex (StarkNet Perpetuals)
**Status:** In development (20% complete)  
**Location:** `paradex/`  
**Documentation:** `paradex/ESSENTIAL/START_HERE.md`

```bash
cd paradex
cat ESSENTIAL/START_HERE.md
```

---

## 🚀 ADDING NEW ADAPTERS

### Template Structure:
```
memory-bank/[exchange-name]/
├── ESSENTIAL/              # Core documentation
│   ├── START_HERE.md
│   ├── WORKFLOW.md
│   ├── PATTERNS.md
│   ├── BUGS.md
│   └── CONFIG.md
├── reference/              # Code templates
│   ├── python/
│   └── rust/
├── tracking/               # Progress tracking
│   ├── progress.md
│   ├── bug-fixes-record.md
│   ├── improvements-log.md
│   ├── validation-results.md
│   └── learning-log.md
└── archive/                # Historical docs
```

### Steps to Add New Adapter:
```bash
# 1. Copy paradex template
cp -r paradex/ [exchange-name]/

# 2. Update exchange-specific details
cd [exchange-name]
vim ESSENTIAL/START_HERE.md
vim ESSENTIAL/CONFIG.md

# 3. Update this README
vim ../README.md
```

---

## 📚 SHARED RESOURCES

### Common Patterns (Future):
```
memory-bank/shared/
├── reconciliation-patterns.md
├── websocket-patterns.md
├── rest-client-patterns.md
└── testing-patterns.md
```

**Note:** Will be created as patterns emerge across multiple adapters

---

## 🎯 QUICK ACCESS

### Paradex Adapter:
```bash
cd memory-bank/paradex/ESSENTIAL
cat START_HERE.md
```

### Future Adapters:
```bash
# Binance (example)
cd memory-bank/binance/ESSENTIAL
cat START_HERE.md

# Bybit (example)
cd memory-bank/bybit/ESSENTIAL
cat START_HERE.md
```

---

## 📊 ADAPTER STATUS

| Exchange | Status | Completion | Location |
|----------|--------|------------|----------|
| Paradex | In Development | 20% | `paradex/` |
| [Future] | Not Started | 0% | - |

---

**Last Updated:** 2026-01-28  
**Active Adapters:** 1 (Paradex)
