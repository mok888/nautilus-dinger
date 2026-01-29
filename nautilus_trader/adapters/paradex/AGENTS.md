# PROJECT KNOWLEDGE BASE

**Generated:** 2026-01-29 14:30 UTC
**Commit:** N/A
**Branch:** master

## OVERVIEW
Python adapter layer bridging Nautilus Trader framework to Rust Paradex core via PyO3 bindings.

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| **Execution** | `execution.py` | ParadexExecutionClient - 11 Nautilus methods |
| **Market Data** | `data.py` | ParadexDataClient - 8 Nautilus methods |
| **Instruments** | `providers.py` | ParadexInstrumentProvider - 3 methods |
| **Type Conversion** | `factories.py` | Parse instruments, orders, fills, positions |
| **Config** | `config.py` | ParadexExecClientConfig, ParadexDataClientConfig |
| **Rust Bridge** | `_rust.py` | Lazy-load .so extension from `crates/adapters/paradex/target/release/` |

## CODE MAP

### Nautilus Adapter Classes

```python
# ParadexExecutionClient (11 methods)
class ParadexExecutionClient(LiveExecutionClient):
    # submit_order, cancel_order, cancel_all_orders, modify_order
    # query_order, generate_order_id, reset, _connect, _disconnect

# ParadexDataClient (8 methods)
class ParadexDataClient(LiveDataClient):
    # subscribe_quote_ticks, subscribe_trade_ticks, subscribe_order_book_deltas
    # subscribe_order_book_snapshots, unsubscribe_*, _connect, _disconnect

# ParadexInstrumentProvider (3 methods)
class ParadexInstrumentProvider(InstrumentProvider):
    # load_all, load, find
```

### Type Factories (factories.py)

```python
parse_instrument()          # Paradex market → CryptoPerpetual
parse_order_status_report() # Paradex order → OrderStatusReport
parse_fill_report()         # Paradex fill → FillReport
parse_position_status_report()  # Paradex position → PositionStatusReport
```

## CONVENTIONS

- **Nautilus patterns**: Implement exactly 11/8/3 required methods
- **Type hints everywhere**: All functions must have full type annotations
- **Async/await**: All I/O operations use asyncio
- **Rust-first**: Delegate heavy operations to Rust via _rust.py, Python orchestrates
- **Timestamp conversion**: Paradex ms → Nautilus ns (millis_to_nanos)
- **Pydantic config**: All configuration uses Pydantic models for validation
- **Factory functions**: Pure functions (no side effects), pass clock for ts_init timestamps

## ANTI-PATTERNS

### FORBIDDEN

- ❌ DO NOT skip type hints (Nautilus requires them)
- ❌ DO NOT use synchronous I/O (all must be async)
- ❌ DO NOT implement fewer than required methods
- ❌ DO NOT bypass factories.py for type conversion
- ❌ DO NOT cache Rust module globally (lazy-load in _rust.py)

### REQUIRED

- ✅ MUST use Nautilus base classes (LiveExecutionClient, LiveDataClient, InstrumentProvider)
- ✅ MUST implement all 11/8/3 required methods (execution/data/provider)
- ✅ MUST use factories.py for Paradex → Nautilus conversions
- ✅ MUST import from _rust.py (lazy-loaded) for Rust calls
- ✅ MUST use millis_to_nanos for timestamps
