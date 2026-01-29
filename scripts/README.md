# Scripts Directory

Organized utility scripts for the Nautilus Dinger project.

## Trading Scripts (`trading/`)

Production trading scripts and order management:

- `live_trader.py` - Main live trading bot with position management
- `place_order.py` - Simple order placement utility
- `place_order_final.py` - Advanced order placement with validation
- `check_account.py` - Check account balance and status
- `check_account_value.py` - Calculate total account value
- `check_portfolio.py` - View portfolio positions
- `close_positions.py` - Close all open positions

## Monitoring Scripts (`monitoring/`)

Live monitoring and data visualization:

- `monitoring_dashboard.py` - Real-time trading dashboard
- `live_btc_price.py` - Live BTC price feed
- `live_btc_enhanced.py` - Enhanced BTC price display
- `live_top5_stream.py` - Top 5 markets stream
- `websocket_live_price.py` - WebSocket price feed
- `websocket_paradex_py.py` - Paradex WebSocket client
- `ws_top5_markets.py` - WebSocket top markets

## Utility Scripts (`utils/`)

Testing, examples, and development utilities:

- `rust_20_trades.py` - Performance test (20 trades via Rust)
- `simple_trading_loop.py` - Simple trading loop example
- `nautilus_full_loop.py` - Full Nautilus integration example
- `nautilus_paradex_strategy.py` - Strategy implementation example
- `paradex_data_client.py` - Data client example
- `robustness_100.py` - Robustness testing (100 trades)

## Usage

All scripts should be run from the project root:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run a trading script
python scripts/trading/live_trader.py

# Run a monitoring script
python scripts/monitoring/monitoring_dashboard.py
```
