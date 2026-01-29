# Account Value & Balance Check

## ✅ COMPLETE

Successfully retrieved full account information including value, balances, and margin.

## Script: `check_account.py`

### Usage
```bash
cd /home/mok/projects/nautilus-dinger
python3 check_account.py
```

### Output
```
======================================================================
ACCOUNT VALUE & BALANCE
======================================================================

[ACCOUNT INFO]
Address:     0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8
Username:    mokmok
Status:      ACTIVE
Account Type: main

[ACCOUNT VALUE]
Account Value:       $     100,370.33
Total Collateral:    $     100,370.33
Free Collateral:     $     100,370.33

[MARGIN]
Initial Margin Req:  $           0.00
Maint. Margin Req:   $           0.00
Margin Cushion:      $     100,370.33

[BALANCES]
USDC:  $        100,404.0405

[POSITIONS]
No open positions

[FEE RATES]
Maker Rate:  -0.005%
Taker Rate:   0.030%

======================================================================
✅ Account check complete
```

## Account Summary

### Current Status
- **Account Value:** $100,370.33
- **Available Balance:** $100,404.04 USDC
- **Free Collateral:** $100,370.33
- **Open Positions:** 0
- **Margin Used:** $0.00

### Account Details
- **Username:** mokmok
- **Account Type:** main (not isolated)
- **Parent Account:** eth:0x372d169f3f5912ee762c477c3d1749c1626a7023

### Fee Structure
- **Maker Rate:** -0.005% (rebate)
- **Taker Rate:** 0.030%
- **Spot Maker:** 0.010%
- **Spot Taker:** 0.050%

## Data Retrieved

1. **Account Info** - Basic account details
2. **Account Summary** - Portfolio value and margin
3. **Balances** - Token balances (USDC)
4. **Positions** - Open positions with PnL
5. **Fee Rates** - Trading fee structure

## API Endpoints Used

```python
paradex.api_client.fetch_account_info()      # Account details
paradex.api_client.fetch_account_summary()   # Value & margin
paradex.api_client.fetch_balances()          # Token balances
paradex.api_client.fetch_positions()         # Open positions
```

## Files

- `check_account.py` - Full account checker
- `check_portfolio.py` - Portfolio with fills
- `check_account_value.py` - Basic value check

## Related Scripts

- `live_btc_price.py` - Live price feed
- `check_portfolio.py` - Portfolio overview
- `nautilus_full_loop.py` - Trading demo
