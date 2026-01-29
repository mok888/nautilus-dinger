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

from paradex_py import ParadexSubkey


async def check_account():
    print("="*70)
    print("ACCOUNT VALUE & BALANCE")
    print("="*70)
    
    # Use paradex-py directly for account summary (not yet in Rust adapter)
    paradex = ParadexSubkey(
        env="testnet",
        l2_private_key=os.getenv("PARADEX_SUBKEY_PRIVATE_KEY"),
        l2_address=os.getenv("PARADEX_L2_ADDRESS")
    )
    
    # Get account info
    account_info = paradex.api_client.fetch_account_info()
    
    print("\n[ACCOUNT INFO]")
    print(f"Address:     {account_info.get('account', 'N/A')}")
    print(f"Username:    {account_info.get('username', 'N/A')}")
    print(f"Status:      {account_info.get('status', 'N/A')}")
    print(f"Account Type: {account_info.get('kind', 'N/A')}")
    
    # Get account summary
    summary = paradex.api_client.fetch_account_summary()
    
    print("\n[ACCOUNT VALUE]")
    print(f"Account Value:       ${float(summary.account_value):>15,.2f}")
    print(f"Total Collateral:    ${float(summary.total_collateral):>15,.2f}")
    print(f"Free Collateral:     ${float(summary.free_collateral):>15,.2f}")
    
    print("\n[MARGIN]")
    print(f"Initial Margin Req:  ${float(summary.initial_margin_requirement):>15,.2f}")
    print(f"Maint. Margin Req:   ${float(summary.maintenance_margin_requirement):>15,.2f}")
    print(f"Margin Cushion:      ${float(summary.margin_cushion):>15,.2f}")
    
    # Get balances
    balances = paradex.api_client.fetch_balances()
    
    print("\n[BALANCES]")
    for balance in balances.get("results", []):
        token = balance.get("token", "N/A")
        size = float(balance.get("size", 0))
        print(f"{token}:  ${size:>20,.4f}")
    
    # Get positions
    positions = paradex.api_client.fetch_positions()
    
    print("\n[POSITIONS]")
    active = [p for p in positions.get("results", []) if float(p.get("size", 0)) != 0]
    
    if active:
        print(f"{'Market':<20} {'Size':<12} {'Entry':<15} {'Unrealized PnL':<15}")
        print("-"*70)
        for pos in active:
            market = pos.get("market", "N/A")
            size = pos.get("size", "0")
            entry = float(pos.get("avg_entry_price", 0))
            pnl = float(pos.get("unrealized_pnl", 0))
            print(f"{market:<20} {size:<12} ${entry:<14,.2f} ${pnl:<14,.2f}")
    else:
        print("No open positions")
    
    # Get fees
    print("\n[FEE RATES]")
    fees = account_info.get("fees", {})
    print(f"Maker Rate:  {float(fees.get('maker_rate', 0))*100:>6.3f}%")
    print(f"Taker Rate:  {float(fees.get('taker_rate', 0))*100:>6.3f}%")
    
    print("\n" + "="*70)
    print("✅ Account check complete")


if __name__ == "__main__":
    asyncio.run(check_account())
