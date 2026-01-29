# Examples

Example scripts demonstrating Nautilus Paradex Adapter usage.

## Order Placement Examples

Located in `order_placement/`:

- `place_order_jwt.py` - Basic order placement with JWT auth
- `place_order_live.py` - Live order placement
- `place_order_with_sl_tp.py` - Orders with stop-loss and take-profit

### Usage

```bash
# Basic order placement
python examples/order_placement/place_order_jwt.py

# Live order with SL/TP
python examples/order_placement/place_order_with_sl_tp.py
```

## More Examples

See `scripts/` directory for:
- **Trading**: Production trading bots (`scripts/trading/`)
- **Monitoring**: Live dashboards (`scripts/monitoring/`)
- **Utils**: Testing utilities (`scripts/utils/`)

## Configuration

All examples require:
1. Virtual environment activated: `source .venv/bin/activate`
2. Environment variables set in `.env` or `config/.env.testnet`
3. Rust adapter built: `cd crates/adapters/paradex && maturin develop`

## API Keys

Set up API keys:
```bash
bash config/setup_api_key.sh
```

Or manually in `.env`:
```
PARADEX_API_KEY=your_key_here
PARADEX_PRIVATE_KEY=your_private_key_here
PARADEX_ACCOUNT_ADDRESS=your_address_here
```
