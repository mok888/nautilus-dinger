#!/usr/bin/env python3
"""
Check account value and balance via Rust adapter
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


async def check_account_value():
    print("="*70)
    print("ACCOUNT VALUE & BALANCE")
    print("="*70)
    
    config = paradex_adapter.PyParadexConfig(
        "testnet",
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_SUBKEY_PRIVATE_KEY")
    )
    client = paradex_adapter.PyHttpClient(config)
    
    # Get account
    account_json = await client.get_account()
    account = json.loads(account_json)
    
    print("\n[ACCOUNT]")
    print(f"Address:     {os.getenv('PARADEX_L2_ADDRESS')}")
    print(f"Status:      {account.get('status', 'N/A')}")
    
    # Get positions for portfolio value
    positions_json = await client.get_positions()
    positions = json.loads(positions_json)
    
    print("\n[BALANCES]")
    
    # Parse account summary if available
    if isinstance(account, dict):
        for key, value in account.items():
            if 'balance' in key.lower() or 'equity' in key.lower() or 'margin' in key.lower():
                print(f"{key:<25} {value}")
    
    # Show full account data
    print("\n[FULL ACCOUNT DATA]")
    print(json.dumps(account, indent=2))
    
    # Calculate position values
    print("\n[POSITION VALUES]")
    total_position_value = 0
    
    for pos in positions.get("results", []):
        size = float(pos.get("size", 0))
        if size != 0:
            market = pos.get("market", "N/A")
            entry = float(pos.get("avg_entry_price", 0))
            pnl = float(pos.get("unrealized_pnl", 0))
            notional = abs(size * entry)
            
            print(f"\n{market}:")
            print(f"  Size:           {size}")
            print(f"  Entry Price:    ${entry:,.2f}")
            print(f"  Notional Value: ${notional:,.2f}")
            print(f"  Unrealized PnL: ${pnl:,.2f}")
            
            total_position_value += notional
    
    if total_position_value > 0:
        print(f"\nTotal Position Value: ${total_position_value:,.2f}")
    else:
        print("\nNo open positions")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    asyncio.run(check_account_value())
