# Account Portfolio Check via Rust Adapter

## ✅ COMPLETE

Successfully checked account portfolio using pure Rust adapter.

## Script: `check_portfolio.py`

### Usage
```bash
cd /home/mok/projects/nautilus-dinger
python3 check_portfolio.py
```

### Output Example
```
======================================================================
ACCOUNT PORTFOLIO (via Rust Adapter)
======================================================================

[ACCOUNT INFO]
Address:     0x4b23c8b4ea5dc54b...
Status:      ACTIVE

[POSITIONS]
No open positions

[OPEN ORDERS]
No open orders

[RECENT FILLS (Last 24h)]
Market               Side     Size         Price          
----------------------------------------------------------------------
BTC-USD-PERP         SELL     0.01         $89,313         
BTC-USD-PERP         SELL     0.01         $89,267         
BTC-USD-PERP         SELL     0.01         $89,267         
BTC-USD-PERP         SELL     0.01         $89,267         
BTC-USD-PERP         SELL     0.0094       $89,267         

======================================================================
✅ Portfolio check complete
```

## Data Retrieved

### 1. Account Info
- Account address
- Account status
- Via: `client.get_account()`

### 2. Positions
- Market
- Size (quantity)
- Average entry price
- Unrealized PnL
- Via: `client.get_positions()`

### 3. Open Orders
- Market
- Side (BUY/SELL)
- Size
- Limit price
- Status
- Via: `client.get_open_orders()`

### 4. Recent Fills (24h)
- Market
- Side
- Size
- Fill price
- Via: `client.get_fills(start_time)`

## Architecture

```
check_portfolio.py
      ↓
Rust Adapter (paradex_adapter.so)
      ↓
paradex-py SDK
      ↓
Paradex API
      ↓
[Account Data, Positions, Orders, Fills]
```

## Test Results

**Account:** ✅ Retrieved
**Positions:** ✅ Retrieved (0 open)
**Orders:** ✅ Retrieved (0 open)
**Fills:** ✅ Retrieved (5 recent fills)

All data successfully fetched via Rust adapter!

## Files

- `check_portfolio.py` - Portfolio checker script
- `paradex_adapter.so` - Rust adapter library

## Related Scripts

- `live_btc_price.py` - Live price feed
- `live_btc_enhanced.py` - Enhanced price display
- `test_rust_full.py` - Full adapter test
- `nautilus_full_loop.py` - Trading loop demo
