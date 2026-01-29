# Draft: Validation Plan for nautilus-dinger

## User Requirements (Confirmed)

### Validation Scope
- **Python files**: 57 total (.py files)
  - 33 root Python files (test scripts, trading scripts, utilities)
  - 7 files in nautilus_trader/adapters/paradex/ (adapter code)
  - 8 files in crates/adapters/paradex/tests/ (Python test files)
  - 9 files in memory-bank/ (mocks and reference implementations)

- **Rust files**: 31 total (.rs files)
  - 25 files in crates/adapters/paradex/src/ (main implementation)
  - 4 files in crates/adapters/paradex/tests/ (Rust test files)
  - 3 files in memory-bank/paradex/reference/rust/ (reference implementation)

### Exclusions
- .venv directory
- target directory

### Validation Strategy Decisions

**1. Python Validation Depth:**
- Check if ruff/mypy/black available in .venv
- Fall back to `python -m py_compile` if not
- Do NOT install new tools

**2. Test Execution:**
- Rust tests: YES, run `cargo test` for both crates
- Python tests: NO, skip running (too complex with dependencies)

**3. Error Handling:**
- Comprehensive mode: Continue validating all files
- Report all errors at the end

**4. Cargo.toml Files:**
- Validate independently as separate crates:
  - `crates/adapters/paradex/Cargo.toml` (main crate)
  - `memory-bank/paradex/reference/rust/Cargo.toml` (reference impl)

**5. Output Format:**
- Summary + detailed logs
- Report counts: total, passed, failed, warnings

### Available Tools
- Rust: cargo 1.93.0, rustc 1.93.0, clippy 0.1.93
- Python: Python 3.12 (in .venv)
- No ruff, mypy, or black installed

### Work Structure
- Wave 1: Rust validation (parallel for different crates)
- Wave 2: Python validation (parallel for different directories)
- Wave 3: Summary and reporting
