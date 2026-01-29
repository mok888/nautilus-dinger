# Paradex Order Placement - Subkey Authentication

**Date:** 2026-01-29  
**Status:** ✅ WORKING

## Summary

Successfully placed BTC limit order on Paradex testnet using **only L2 credentials** (no JWT token, no API key required).

## Authentication Method

Uses `paradex-py` SDK's `ParadexSubkey` class which handles:
- JWT token generation from subkey
- Order signature creation
- API authentication

**Required credentials (from `.env.testnet`):**
- `PARADEX_L2_ADDRESS` - Your wallet address
- `PARADEX_SUBKEY_PRIVATE_KEY` - Subkey for signing

## Order Details

**Executed:** 2026-01-29 09:17 UTC

```
Market: BTC-USD-PERP
Side: BUY
Type: LIMIT
Size: 0.001 BTC

BTC Ask: $89,313.10
Entry: $89,268.40 (-5bps from ask)
Stop Loss: $84,804.98 (-5% from entry)
Take Profit: $93,731.82 (+5% from entry)

Order ID: 1769678186750201703945230000
Status: ✅ PLACED
```

## Implementation

**Script:** `/home/mok/projects/nautilus-dinger/place_order.py`

### Key Code

```python
from paradex_py import ParadexSubkey
from paradex_py.common.order import Order, OrderSide, OrderType
from decimal import Decimal

# Initialize with L2 credentials only
paradex = ParadexSubkey(
    env="testnet",
    l2_private_key=SUBKEY,
    l2_address=L2_ADDRESS
)

# Get price
orderbook = paradex.api_client.fetch_orderbook("BTC-USD-PERP")
ask = Decimal(orderbook["asks"][0][0])

# Calculate entry -5bps, rounded to 0.1
entry = ask * Decimal("0.9995")
entry = (entry / Decimal("0.1")).quantize(Decimal("1")) * Decimal("0.1")

# Create and submit order
order = Order(
    market="BTC-USD-PERP",
    order_side=OrderSide.Buy,
    order_type=OrderType.Limit,
    size=Decimal("0.001"),
    limit_price=entry
)

result = paradex.api_client.submit_order(order)
```

## Dependencies

```bash
pip install paradex-py python-dotenv
```

## Usage

```bash
cd /home/mok/projects/nautilus-dinger
python3 place_order.py
```

## Key Learnings

1. **No API key needed** - Subkey handles authentication internally
2. **No JWT management** - SDK generates tokens automatically
3. **Price precision** - Must be multiple of 0.1 for BTC-USD-PERP
4. **Order parameters** - Use `limit_price` not `price`, `order_side` not `side`

## References

- [Paradex API Authentication Docs](https://docs.paradex.trade/docs/trading/api-authentication)
- [paradex-py SDK Docs](https://tradeparadex.github.io/paradex-py/)
- Subkey authentication: L2-only, no onboarding required
