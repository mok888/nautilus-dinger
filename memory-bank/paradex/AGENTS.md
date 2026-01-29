# PROJECT KNOWLEDGE BASE - PARADEX

**Generated:** 2026-01-29 14:30 UTC
**Commit:** N/A
**Branch:** master

## OVERVIEW
Documentation hub for Paradex Nautilus adapter implementation with organized reference materials and tracking systems.

## STRUCTURE

```
memory-bank/paradex/
├── ESSENTIAL/              # Core docs (START_HERE, WORKFLOW, PATTERNS, BUGS, CONFIG)
├── reference/              # Code templates (python/, rust/)
├── tracking/               # Progress tracking (progress.md, bug-fixes-record.md, etc.)
├── archive/                # Historical docs (summaries/, old-guides/, analysis/)
├── docs/                   # Current implementation docs
├── exploration/            # Research and notes
└── mocks/                  # Test fixtures (paradex-mock/)
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| **Getting Started** | `ESSENTIAL/START_HERE.md` | Project overview, status, quick start |
| **Implementation Guide** | `ESSENTIAL/WORKFLOW.md` | Phase-based workflow (4 phases, 68h) |
| **Code Patterns** | `ESSENTIAL/PATTERNS.md` | Reusable code patterns from OKX adapter |
| **Known Issues** | `ESSENTIAL/BUGS.md` | 12 documented bugs with solutions |
| **Configuration** | `ESSENTIAL/CONFIG.md` | Testnet setup, credentials |
| **Python Templates** | `reference/python/` | 7 template files (data.py, execution.py, etc.) |
| **Rust Templates** | `reference/rust/` | 4 template files (lib.rs, config.rs, etc.) |
| **Progress Tracking** | `tracking/progress.md` | Completion metrics, phase status |
| **Bug Fixes** | `tracking/bug-fixes-record.md` | Detailed bug tracking log |
| **Historical Analysis** | `archive/analysis/` | 15 detailed analysis documents |
| **Test Fixes** | `mocks/paradex-mock/` | HTTP/WebSocket mock servers |

## CONVENTIONS

### Documentation Style
- **Emoji prefixes**: 🚀 (quick actions), 🎯 (goals), 📁 (structure), 📊 (metrics), 🐛 (bugs)
- **Status tracking**: Use checkboxes for task lists (`- [ ]`, `- [x]`)
- **Phase organization**: Work organized into 4 phases (Python → Rust → Testing → Documentation)
- **Time estimates**: Include estimated hours and credits for each task
- **Priority indicators**: CRITICAL, HIGH, MEDIUM for bugs and issues

### Progress Tracking
- Update `tracking/progress.md` after each task completion
- Track metrics: completion %, test coverage, known bugs, technical debt
- Log bug fixes in `tracking/bug-fixes-record.md`
- Document improvements in `tracking/improvements-log.md`
- Record validation results in `tracking/validation-results.md`

### Code Reference Organization
- Templates separated by language: `reference/python/` and `reference/rust/`
- Templates are production-ready examples from OKX adapter
- Include imports, type hints, and docstrings
- Mock fixtures in `mocks/paradex-mock/fixtures/` (JSON format)

## ANTI-PATTERNS

### Documentation (FORBIDDEN)
- ❌ DO NOT reference archive files in ESSENTIAL docs
- ❌ DO NOT duplicate content across multiple files
- ❌ DO NOT skip updating tracking files after work
- ❌ DO NOT create new markdown files without archiving old ones first

### Reference Code (FORBIDDEN)
- ❌ DO NOT modify reference templates directly - copy them first
- ❌ DO NOT use stub implementations as final code
- ❌ DO NOT skip type hints or docstrings in templates
- ❌ DO NOT commit mock server credentials to git

### Required
- ✅ MUST read ESSENTIAL docs before implementation
- ✅ MUST update progress.md after each phase
- ✅ MUST use reference/ templates as starting point
- ✅ MUST validate changes against BUGS.md checklist
- ✅ MUST archive outdated guides to archive/old-guides/
- ✅ MUST use DashMap, NOT RwLock (see BUGS.md #004)

---

**Last Updated:** 2026-01-29 14:30 UTC
