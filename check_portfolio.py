#!/usr/bin/env python3
"""
Check account portfolio via Rust adapter
"""
import os
import sys
import asyncio
import json

sys.path.insert(0, '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages')
os.environ['PYTHONPATH'] = '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages'

from dotenv import load_dotenv
load_dotenv(".env.testnet")

import paradex_adapter


async def check_portfolio():
    print("="*70)
    print("ACCOUNT PORTFOLIO (via Rust Adapter)")
    print("="*70)
    
    # Initialize
    config = paradex_adapter.PyParadexConfig(
        "testnet",
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_SUBKEY_PRIVATE_KEY")
    )
    client = paradex_adapter.PyHttpClient(config)
    
    # Get account info
    print("\n[ACCOUNT INFO]")
    account_json = await client.get_account()
    account = json.loads(account_json)
    
    print(f"Address:     {account.get('account', 'N/A')[:20]}...")
    print(f"Status:      {account.get('status', 'N/A')}")
    
    # Get positions
    print("\n[POSITIONS]")
    positions_json = await client.get_positions()
    positions = json.loads(positions_json)
    
    active_positions = [p for p in positions.get("results", []) if float(p.get("size", 0)) != 0]
    
    if active_positions:
        print(f"{'Market':<20} {'Size':<12} {'Entry Price':<15} {'PnL':<15}")
        print("-"*70)
        for pos in active_positions:
            market = pos.get("market", "N/A")
            size = pos.get("size", "0")
            entry = pos.get("avg_entry_price", "N/A")
            pnl = pos.get("unrealized_pnl", "0")
            print(f"{market:<20} {size:<12} ${entry:<14} ${pnl:<14}")
    else:
        print("No open positions")
    
    # Get open orders
    print("\n[OPEN ORDERS]")
    orders_json = await client.get_open_orders()
    orders = json.loads(orders_json)
    
    open_orders = orders.get("results", [])
    
    if open_orders:
        print(f"{'Market':<20} {'Side':<8} {'Size':<12} {'Price':<15} {'Status':<10}")
        print("-"*70)
        for order in open_orders[:10]:
            market = order.get("market", "N/A")
            side = order.get("side", "N/A")
            size = order.get("size", "0")
            price = order.get("limit_price", "N/A")
            status = order.get("status", "N/A")
            print(f"{market:<20} {side:<8} {size:<12} ${price:<14} {status:<10}")
    else:
        print("No open orders")
    
    # Get recent fills
    print("\n[RECENT FILLS (Last 24h)]")
    import time
    start_time = int(time.time() * 1000) - (24 * 60 * 60 * 1000)
    fills_json = await client.get_fills(start_time)
    fills = json.loads(fills_json)
    
    recent_fills = fills.get("results", [])[:5]
    
    if recent_fills:
        print(f"{'Market':<20} {'Side':<8} {'Size':<12} {'Price':<15}")
        print("-"*70)
        for fill in recent_fills:
            market = fill.get("market", "N/A")
            side = fill.get("side", "N/A")
            size = fill.get("size", "0")
            price = fill.get("price", "N/A")
            print(f"{market:<20} {side:<8} {size:<12} ${price:<14}")
    else:
        print("No recent fills")
    
    print("\n" + "="*70)
    print("✅ Portfolio check complete")


if __name__ == "__main__":
    asyncio.run(check_portfolio())
