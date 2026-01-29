# RUST CORE - PARADEX ADAPTER

## OVERVIEW
PyO3-bound Rust core providing auth, HTTP client, WebSocket, STARK signing, and state management for Paradex DEX integration.

## STRUCTURE

```
src/
├── auth/                 # JWT token generation
├── http/                 # ParadexHttpClient (reqwest + JWT)
├── websocket/           # JSON-RPC client, handlers, simple client
├── signing/             # StarkSigner (starknet-crypto)
├── state/               # ConnectionState, Reconciliation (DashMap)
├── python/              # PyO3 bindings (17 classes)
├── common/              # Shared types
├── concurrency.rs       # Concurrent primitives
├── config.rs            # PyParadexConfig
└── error.rs             # ParadexError enum + Result<T>
```

## WHERE TO LOOK

| Module | Key Files | Purpose |
|--------|-----------|---------|
| **Auth** | `auth/jwt.rs` | JWT generation + expiration (1hr TTL) |
| **HTTP** | `http/client.rs` | ParadexHttpClient with JWT auth header injection |
| **WebSocket** | `websocket/client.rs`, `simple_client.rs` | Full JSON-RPC client + simplified version |
| **Signing** | `signing/signer.rs` | STARK signatures with starknet-crypto |
| **State** | `state/state.rs`, `reconciliation.rs` | DashMap order/fill tracking + deduplication |
| **Python** | `python/mod.rs` | PyO3 bindings for all public types |
| **Error** | `error.rs` | ParadexError enum + Result<T> alias |

## CONVENTIONS

**Error Handling:** `Result<T>` alias for all functions, thiserror enums, `From<E>` impls for reqwest/tungstenite/serde_json errors.

**Async Runtime:** tokio (full features), pyo3-asyncio with tokio-runtime for Python bridging.

**Concurrency:** DashMap for state (not RwLock), parking_lot::Mutex, Arc for shared ownership.

**Crypto:** starknet-crypto for STARK signatures, sha2/sha3 for hashing, hex encoding.

**Python Integration:** PyO3 (abi3-py312), `#[pyclass]`/`#[pymethods]`, pyo3-asyncio for async bridging.

**HTTP/WS:** reqwest (json feature), tokio-tungstenite (native-tls), JSON-RPC v2 protocol.

**Serialization:** serde derives, serde_json, chrono for timestamps.

## ANTI-PATTERNS (THIS MODULE)

### FORBIDDEN
- ❌ RwLock for state → use DashMap
- ❌ hyper directly → use reqwest
- ❌ bare `std::result::Result<T, E>` → use `Result<T>` alias
- ❌ expose reqwest types to Python → wrap in PyHttpClient
- ❌ skip JWT header injection → auth/ handles this
- ❌ std::sync::Mutex → use parking_lot::Mutex

### REQUIRED
- ✅ `From<E>` impls for ParadexError (reqwest, tungstenite, serde_json)
- ✅ DashMap for concurrent state
- ✅ chrono for timestamps
- ✅ pyo3-asyncio for Python async exposure
- ✅ Validate STARK keys (64 hex chars, no "0x" prefix)
- ✅ JSON-RPC v2 protocol for WebSocket
- ✅ JWT expiration handling (1hr TTL)

## INTEGRATION POINTS

- **Python layer**: All PyO3-wrapped structs via `paradex_adapter` module
- **StarkNet crypto**: starknet-crypto for all STARK operations
- **Async bridge**: pyo3-asyncio connects tokio to Python asyncio

---

**Last Updated:** 2026-01-29 14:30 UTC
