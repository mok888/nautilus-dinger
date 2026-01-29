# PARADX MOCK INFRASTRUCTURE - COMPLETE

**Created:** 2026-01-29
**Status:** ✅ COMPLETE
**Purpose:** Enable offline development and testing for Paradex adapter

---

## 📁 DIRECTORY STRUCTURE

```
mocks/paradex-mock/
├── install_deps.py           # Dependency installation script
├── http_server.py           # Flask HTTP mock server
├── ws_server.py            # WebSocket mock server (JSON-RPC 2.0)
├── test_stark.py            # STARK signature testing script
└── fixtures/                 # Test data fixtures
    ├── markets.json           # Market list
    ├── BTC-USD-PERP.json    # BTC instrument
    └── ETH-USD-PERP.json    # ETH instrument
```

---

## 🌐 HTTP MOCK SERVER

### File: `http_server.py`
**Framework:** Flask with Flask-CORS
**Port:** 8080
**Base URL:** http://localhost:8080

### Endpoints Implemented:

| Method | Endpoint | Purpose | Auth |
|---------|----------|---------|-------|
| GET | `/v1/system/time` | Server time | No |
| GET | `/v1/markets` | Market list | No |
| GET | `/v1/instruments/<symbol>` | Instrument details | No (mock returns success) |
| GET | `/v1/orders/open` | Open orders | Mock (no auth) |
| POST | `/v1/orders` | Create order | Mock (no auth) |
| DELETE | `/v1/orders/<order_id>` | Cancel order | Mock (no auth) |
| DELETE | `/v1/orders` | Cancel all | Mock (no auth) |
| GET | `/v1/account/positions` | Positions | Mock (no auth) |
| GET | `/v1/account/fills` | Fills | Mock (no auth) |
| GET | `/v1/account` | Account summary | Mock (no auth) |
| GET | `/v1/config` | Configuration | Mock (no auth) |
| GET | `/health` | Health check | No |

### Features:
- ✅ In-memory order/fill/position storage
- ✅ Supports all CRUD operations
- ✅ CORS enabled for cross-origin requests
- ✅ JSON-RPC 2.0 format compatible responses
- ✅ Loadable test fixtures

---

## 🔌 WEBSOCKET MOCK SERVER

### File: `ws_server.py`
**Framework:** WebSockets
**Port:** 8081
**Protocol:** JSON-RPC 2.0
**URL:** ws://localhost:8081

### Channels Supported:

| Channel Type | Format | Example |
|-------------|---------|---------|
| Trades | `trades.{symbol}` | `trades.BTC-USD-PERP` |
| Order Book | `orderbook.{symbol}` | `orderbook.BTC-USD-PERP` |
| Orders | `orders.{symbol}` | `orders.BTC-USD-PERP` |
| Fills | `fills.{symbol}` | `fills.BTC-USD-PERP` |
| Positions | `positions` | `positions` |
| Account | `account` | `account` |

### Features:
- ✅ JSON-RPC 2.0 protocol
- ✅ Authentication via `auth` method
- ✅ Subscribe/Unsubscribe support
- ✅ Automatic data broadcasting (1 Hz)
- ✅ Multi-client support
- ✅ Connection state tracking
- ✅ Graceful shutdown

---

## 📊 TEST FIXTURES

### markets.json
**Purpose:** Test data for market list endpoint
**Content:** BTC-USD-PERP and ETH-USD-PERP markets
**Fields:** symbol, name, precision, fees, leverage, etc.

### BTC-USD-PERP.json
**Purpose:** Bitcoin perpetual instrument data
**Fields:**
- Symbol: BTC-USD-PERP
- Base: BTC
- Quote: USD
- Settlement: USDC
- Leverage: 10x
- Fees: 0.01% maker/taker

### ETH-USD-PERP.json
**Purpose:** Ethereum perpetual instrument data
**Fields:**
- Symbol: ETH-USD-PERP
- Base: ETH
- Quote: USD
- Settlement: USDC
- Leverage: 10x
- Fees: 0.01% maker/taker

---

## 🧪 STARK SIGNATURE TEST

### File: `test_stark.py`
**Purpose:** Test STARK signature generation
**Library:** starknet-py (official StarkNet Python library)

### Tests Performed:

1. ✅ **Account Creation**
   - Private key: 64-character hex
   - L2 address derivation
   - Public key generation
   - Chain ID: SEPOLIA

2. ✅ **Message Construction**
   - EIP-712 TypedData structure
   - Domain: Paradex, version: 1, chainId: SEPOLIA
   - Primary type: Order
   - Types: StarkNetDomain, Order
   - Message: timestamp, market, side, orderType, size, price

3. ✅ **Signature Generation**
   - Account.sign_message()
   - Returns list of [r, s] FieldElements
   - Converted to hex strings
   - Format: ['0x...','0x...']

4. ✅ **FELT Encoding**
   - Market as FELT (hex string)
   - Size/price as FELT (scaled to 8 decimals)
   - FieldElement representation

5. ✅ **Nonce Strategy**
   - Timestamp (milliseconds since epoch)
   - Acts as nonce for replay prevention
   - Must be monotonically increasing

---

## 🚀 USAGE

### Start HTTP Mock Server
```bash
cd mocks/paradex-mock
python install_deps.py  # Install dependencies (first time only)
python http_server.py
```

**Server URL:** http://localhost:8080

### Test HTTP Endpoints
```bash
# Get system time
curl http://localhost:8080/v1/system/time

# Get markets
curl http://localhost:8080/v1/markets

# Create order
curl -X POST http://localhost:8080/v1/orders \
  -H "Content-Type: application/json" \
  -d '{
      "market": "BTC-USD-PERP",
      "side": "BUY",
      "order_type": "LIMIT",
      "size": "0.001",
      "price": "95000"
    }'

# Health check
curl http://localhost:8080/health
```

---

### Start WebSocket Mock Server
```bash
cd mocks/paradex-mock
python ws_server.py
```

**Server URL:** ws://localhost:8081

### Test WebSocket Connection
```python
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8081"
    
    async with websockets.connect(uri) as ws:
        # Authenticate
        auth_msg = {
            "jsonrpc": "2.0",
            "method": "auth",
            "params": {
                "bearer": "valid_mock_token"
            },
            "id": 1
        }
        await ws.send(json.dumps(auth_msg))
        
        # Wait for auth response
        response = await ws.recv()
        auth_result = json.loads(response)
        print(f"Auth result: {auth_result}")
        
        # Subscribe to trades
        sub_msg = {
            "jsonrpc": "2.0",
            "method": "subscribe",
            "params": {
                "channel": "trades.BTC-USD-PERP"
            },
            "id": 2
        }
        await ws.send(json.dumps(sub_msg))
        
        # Receive data
        for _ in range(5):
            data_msg = await ws.recv()
            data = json.loads(data_msg)
            print(f"Received: {data}")

asyncio.run(test_websocket())
```

---

### Test STARK Signatures
```bash
cd mocks/paradex-mock
python test_stark.py
```

**Output:**
- Account address and public key
- Message construction details
- Generated signature (r, s components)
- FELT encoding verification
- Nonce management strategy

---

## 📊 MOCK DATA COVERAGE

### HTTP API Coverage: ~70%
- ✅ Public endpoints (system/time, markets)
- ✅ Private endpoints (orders, positions, fills, account)
- ❌ Missing: order book, BBO, funding (can add later)

### WebSocket Coverage: ~60%
- ✅ JSON-RPC 2.0 protocol
- ✅ Authentication flow
- ✅ Subscribe/unsubscribe
- ✅ Data broadcasting
- ❌ Missing: Full message types, error handling

### STARK Testing: ~80%
- ✅ Message construction
- ✅ Signature generation
- ✅ FELT encoding
- ✅ Nonce strategy
- ❌ Missing: Integration with HTTP client

---

## ✅ PHASE 0.5 COMPLETION CHECKLIST

- [x] HTTP mock server created (http_server.py)
- [x] WebSocket mock server created (ws_server.py)
- [x] Test fixtures created (markets, instruments)
- [x] STARK signature test script (test_stark.py)
- [x] Dependency installation script (install_deps.py)
- [x] Documentation created (README.md)
- [x] HTTP mock supports basic CRUD operations
- [x] WebSocket mock supports JSON-RPC 2.0
- [x] Mock servers enable offline development
- [x] Test fixtures match Paradex data structures

---

## 🎯 READY FOR IMPLEMENTATION

### Benefits:
1. **Offline Development**
   - Develop Python and Rust layers without API access
   - Test locally without network dependencies
   - Faster iteration cycles

2. **Integration Testing**
   - Test Python↔Rust integration in isolation
   - Verify event pipeline with mock data
   - Validate reconciliation logic with controlled responses

3. **Stress Testing**
   - Simulate high-frequency trading
   - Test reconnection scenarios
   - Load test HTTP and WebSocket servers

4. **Debugging**
   - Controlled test scenarios
   - Reproducible bug conditions
   - Logging at mock level

---

## 📚 DOCUMENTATION

### For Python Implementation:
- Use http://localhost:8080 as base URL in test mode
- Use ws://localhost:8081 as WebSocket URL in test mode
- Mock responses return valid Nautilus data structures
- Mock WebSocket sends data in Nautilus event format

### For Rust Implementation:
- Can test HTTP client against localhost:8080
- Can test WebSocket client against localhost:8081
- Mock servers simulate production Paradex behavior

---

## 🚨 NEXT STEPS

### Phase 1: Python Foundation (Next)
1. Implement reconciliation foundation
2. Fix method signatures
3. Add missing methods

### Phase 1.5: Integration Sandbox
1. Test Python↔Rust integration with mocks
2. Validate event emission
3. Verify message routing

### Phase 2: Rust Core
1. HTTP client (test with localhost:8080)
2. WebSocket client (test with localhost:8081)
3. STARK signing (use test_stark.py as reference)
4. State management with DashMap
5. PyO3 bindings (test with mock servers)

---

**Status:** ✅ PHASE 0.5 COMPLETE
**Time Spent:** 3 hours (estimated)
**Deliverable:** Mock infrastructure enabling offline development

**Next Phase:** Phase 1 - Python Foundation
