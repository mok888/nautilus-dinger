# Paradex Adapter - Authentication Guide

## Current Status

**✅ WORKING: Use `paradex-py` SDK**

The `paradex-py` SDK correctly implements L2 wallet + subkey authentication without requiring a separate API key.

## Usage

### Installation

```bash
pip install paradex-py python-dotenv
```

### Configuration

Create `.env.testnet`:
```bash
PARADEX_L2_ADDRESS=0x...
PARADEX_SUBKEY_PRIVATE_KEY=0x...
```

### Implementation

```python
from paradex_py import ParadexSubkey
from paradex_py.common.order import Order, OrderSide, OrderType
from decimal import Decimal
import os
from dotenv import load_dotenv

load_dotenv(".env.testnet")

# Initialize with L2 credentials only (no API key needed)
paradex = ParadexSubkey(
    env="testnet",
    l2_private_key=os.getenv("PARADEX_SUBKEY_PRIVATE_KEY"),
    l2_address=os.getenv("PARADEX_L2_ADDRESS")
)

# Get market data
orderbook = paradex.api_client.fetch_orderbook("BTC-USD-PERP")
ask = Decimal(orderbook["asks"][0][0])

# Place order
order = Order(
    market="BTC-USD-PERP",
    order_side=OrderSide.Buy,
    order_type=OrderType.Limit,
    size=Decimal("0.001"),
    limit_price=ask * Decimal("0.9995")  # -5bps
)

result = paradex.api_client.submit_order(order)
print(f"Order placed: {result['id']}")

# Check positions
positions = paradex.api_client.fetch_positions()
for pos in positions["results"]:
    if Decimal(pos["size"]) != 0:
        print(f"{pos['market']}: {pos['size']}")

# Close position
close_order = Order(
    market="BTC-USD-PERP",
    order_side=OrderSide.Sell,
    order_type=OrderType.Market,
    size=Decimal("0.001")
)
paradex.api_client.submit_order(close_order)
```

## Why Not Rust Adapter?

The Rust adapter (`crates/adapters/paradex/`) has JWT authentication issues:
- ❌ JWT signature verification fails
- ❌ Error: `STARKNET_SIGNATURE_VERIFICATION_FAILED`
- ❌ All authenticated endpoints blocked

The `paradex-py` SDK handles JWT generation internally from the subkey, which the Rust adapter doesn't do correctly yet.

## Tested & Working

All functions tested successfully with `paradex-py`:
- ✅ Market data fetching
- ✅ Order placement (limit & market)
- ✅ Position management
- ✅ Order status checks
- ✅ Account queries
- ✅ Order cancellation

## Example Scripts

- `place_order.py` - Place BTC limit order with -5bps entry
- `close_positions.py` - Close all open positions
- `test_adapter_loop.py` - Full robustness test

## Authentication Flow

`paradex-py` SDK handles this internally:
1. Takes L2 address + subkey private key
2. Generates JWT token from subkey signature
3. Uses JWT for API authentication
4. Auto-refreshes token as needed

**No separate API key required!**

## Future: Rust Adapter Fix

To fix the Rust adapter, it needs to:
1. Generate JWT token from subkey (like `paradex-py` does)
2. Fix STARK signature verification
3. Handle token refresh automatically

Until then, use `paradex-py` SDK for production trading.
