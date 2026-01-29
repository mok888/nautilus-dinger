#!/usr/bin/env python3
"""
Place order using JWT authentication (no API key needed)
Uses the Rust adapter to generate JWT from private key
"""

import sys
sys.path.insert(0, '../../../target/release')

import requests
import json
from decimal import Decimal

# Testnet credentials
L2_ADDRESS = "0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8"
SUBKEY_PRIVATE_KEY = "0x0441c1622edc5a77891cf97cd76c4ff097211f3df4493425fb9519e06ff8cf55"

def get_btc_price():
    response = requests.get(
        "https://api.testnet.paradex.trade/v1/orderbook/BTC-USD-PERP",
        timeout=5
    )
    data = response.json()
    best_bid = Decimal(data["bids"][0][0])
    best_ask = Decimal(data["asks"][0][0])
    return {"bid": float(best_bid), "ask": float(best_ask)}

def main():
    print("\n" + "="*70)
    print("PLACE ORDER WITH JWT AUTHENTICATION")
    print("="*70)
    
    print("\n[INFO] This requires:")
    print("  1. Rust adapter built (cargo build --release)")
    print("  2. Account onboarded on Paradex testnet")
    print("  3. Funded testnet account")
    
    print(f"\n✓ L2 Address: {L2_ADDRESS[:10]}...{L2_ADDRESS[-8:]}")
    
    # Get price
    print("\n[1] Fetching BTC price...")
    prices = get_btc_price()
    print(f"    Bid: ${prices['bid']:,.2f}")
    print(f"    Ask: ${prices['ask']:,.2f}")
    
    # Calculate entry
    entry = Decimal(str(prices['ask'])) * Decimal("0.9995")
    print(f"\n[2] Entry price: ${float(entry):,.2f} (-5bps)")
    
    # Order payload
    order = {
        "market": "BTC-USD-PERP",
        "side": "BUY",
        "type": "LIMIT",
        "size": "0.001",
        "price": f"{float(entry):.1f}",
        "time_in_force": "GTC"
    }
    
    print("\n[3] Order:")
    print(json.dumps(order, indent=2))
    
    print("\n[4] To place this order:")
    print("    a) Build Rust adapter: cargo build --release")
    print("    b) Use adapter's JWT auth to get token")
    print("    c) POST to /v1/orders with Bearer token")
    
    print("\n[ALTERNATIVE] Use API key:")
    print("    1. Go to https://testnet.paradex.trade")
    print("    2. Connect with L2 address above")
    print("    3. Generate API key")
    print("    4. Run: export PARADEX_API_KEY='your_key'")
    print("    5. Run: python3 tests/place_order_live.py")
    
    print("\n" + "="*70)
    print("ORDER READY - Awaiting authentication")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
