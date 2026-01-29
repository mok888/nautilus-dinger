#!/usr/bin/env python3
"""
Place actual order on Paradex testnet using credentials
"""

import os
import sys
import requests
import json
from decimal import Decimal

# Testnet credentials from memory-bank
L2_ADDRESS = "0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8"
SUBKEY_PRIVATE_KEY = "0x0441c1622edc5a77891cf97cd76c4ff097211f3df4493425fb9519e06ff8cf55"

# Check for API key in environment
API_KEY = os.getenv("PARADEX_API_KEY")

def get_btc_price():
    """Get current BTC price"""
    response = requests.get(
        "https://api.testnet.paradex.trade/v1/orderbook/BTC-USD-PERP",
        timeout=5
    )
    data = response.json()
    
    best_bid = Decimal(data["bids"][0][0])
    best_ask = Decimal(data["asks"][0][0])
    
    return {
        "bid": float(best_bid),
        "ask": float(best_ask),
        "mid": float((best_bid + best_ask) / 2)
    }

def calculate_prices(market_price):
    """Calculate entry, SL, TP"""
    price = Decimal(str(market_price))
    
    entry = price * Decimal("0.9995")  # -5bps
    stop_loss = entry * Decimal("0.95")  # -5%
    take_profit = entry * Decimal("1.05")  # +5%
    
    return {
        "entry": float(entry),
        "stop_loss": float(stop_loss),
        "take_profit": float(take_profit)
    }

def place_order(api_key, order_payload):
    """Place order on Paradex"""
    response = requests.post(
        "https://api.testnet.paradex.trade/v1/orders",
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json"
        },
        json=order_payload,
        timeout=10
    )
    
    return response

def main():
    print("\n" + "="*70)
    print("PLACE ORDER ON PARADEX TESTNET")
    print("="*70)
    
    # Check API key
    if not API_KEY:
        print("\n❌ ERROR: PARADEX_API_KEY environment variable not set")
        print("\nTo get an API key:")
        print("  1. Go to https://testnet.paradex.trade")
        print("  2. Connect wallet with L2 address:")
        print(f"     {L2_ADDRESS}")
        print("  3. Generate API key in settings")
        print("  4. Export: export PARADEX_API_KEY='your_key_here'")
        print("\nAlternatively, use JWT authentication (requires onboarding)")
        print("="*70 + "\n")
        return False
    
    print(f"\n✓ Using L2 Address: {L2_ADDRESS[:10]}...{L2_ADDRESS[-8:]}")
    print(f"✓ API Key found: {API_KEY[:20]}...")
    
    # Get price
    print("\n[1] Fetching BTC price...")
    prices = get_btc_price()
    print(f"    Bid: ${prices['bid']:,.2f}")
    print(f"    Ask: ${prices['ask']:,.2f}")
    print(f"    Mid: ${prices['mid']:,.2f}")
    
    # Calculate order prices
    print("\n[2] Calculating order prices...")
    order_prices = calculate_prices(prices['ask'])
    print(f"    Entry:  ${order_prices['entry']:,.2f} (-5bps)")
    print(f"    SL:     ${order_prices['stop_loss']:,.2f} (-5%)")
    print(f"    TP:     ${order_prices['take_profit']:,.2f} (+5%)")
    
    # Create order
    order = {
        "market": "BTC-USD-PERP",
        "side": "BUY",
        "type": "LIMIT",
        "size": "0.001",
        "price": f"{order_prices['entry']:.1f}",
        "time_in_force": "GTC"
    }
    
    print("\n[3] Order payload:")
    print(json.dumps(order, indent=2))
    
    # Confirm
    print("\n" + "="*70)
    confirm = input("Place this order on testnet? (yes/no): ")
    
    if confirm.lower() != "yes":
        print("Order cancelled.")
        return False
    
    # Place order
    print("\n[4] Placing order...")
    try:
        response = place_order(API_KEY, order)
        
        print(f"    Status: {response.status_code}")
        
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            print("\n✅ ORDER PLACED SUCCESSFULLY!")
            print(json.dumps(result, indent=2))
            return True
        else:
            print(f"\n❌ ORDER FAILED")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False
    
    finally:
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
