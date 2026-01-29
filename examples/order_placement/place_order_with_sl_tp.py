#!/usr/bin/env python3
"""
Place limit order with stop loss and take profit
- Get BTC price from Paradex
- Place limit order at -5bps (0.05% below market)
- Set stop loss at -5% from entry
- Set take profit at +5% from entry
"""

import requests
import json
from decimal import Decimal

def get_btc_price():
    """Get current BTC price from Paradex"""
    response = requests.get(
        "https://api.testnet.paradex.trade/v1/orderbook/BTC-USD-PERP",
        timeout=5
    )
    data = response.json()
    
    best_bid = Decimal(data["bids"][0][0])
    best_ask = Decimal(data["asks"][0][0])
    mid_price = (best_bid + best_ask) / 2
    
    return {
        "bid": float(best_bid),
        "ask": float(best_ask),
        "mid": float(mid_price)
    }

def calculate_order_prices(market_price, side="BUY"):
    """Calculate entry, stop loss, and take profit prices"""
    price = Decimal(str(market_price))
    
    if side == "BUY":
        # Entry: -5bps below ask (better price)
        entry = price * Decimal("0.9995")  # -0.05%
        
        # Stop loss: -5% from entry
        stop_loss = entry * Decimal("0.95")  # -5%
        
        # Take profit: +5% from entry
        take_profit = entry * Decimal("1.05")  # +5%
    else:  # SELL
        # Entry: +5bps above bid
        entry = price * Decimal("1.0005")  # +0.05%
        
        # Stop loss: +5% from entry
        stop_loss = entry * Decimal("1.05")  # +5%
        
        # Take profit: -5% from entry
        take_profit = entry * Decimal("0.95")  # -5%
    
    return {
        "entry": float(entry),
        "stop_loss": float(stop_loss),
        "take_profit": float(take_profit)
    }

def create_order_payload(side, entry_price, size=0.001):
    """Create order payload for Paradex API"""
    return {
        "market": "BTC-USD-PERP",
        "side": side,
        "type": "LIMIT",
        "size": str(size),
        "price": f"{entry_price:.1f}",
        "time_in_force": "GTC",  # Good Till Cancel
        "post_only": False
    }

def main():
    print("\n" + "="*70)
    print("LIMIT ORDER WITH STOP LOSS & TAKE PROFIT")
    print("="*70)
    
    # Step 1: Get current BTC price
    print("\n[1] Fetching BTC price from Paradex...")
    prices = get_btc_price()
    print(f"    Bid: ${prices['bid']:,.2f}")
    print(f"    Ask: ${prices['ask']:,.2f}")
    print(f"    Mid: ${prices['mid']:,.2f}")
    
    # Step 2: Calculate order prices
    side = "BUY"
    print(f"\n[2] Calculating order prices for {side}...")
    order_prices = calculate_order_prices(prices['ask'], side)
    
    print(f"    Entry Price:  ${order_prices['entry']:,.2f} (-5bps from ask)")
    print(f"    Stop Loss:    ${order_prices['stop_loss']:,.2f} (-5% from entry)")
    print(f"    Take Profit:  ${order_prices['take_profit']:,.2f} (+5% from entry)")
    
    # Step 3: Calculate P&L
    entry = Decimal(str(order_prices['entry']))
    sl = Decimal(str(order_prices['stop_loss']))
    tp = Decimal(str(order_prices['take_profit']))
    size = Decimal("0.001")
    
    loss_per_btc = entry - sl
    profit_per_btc = tp - entry
    
    max_loss = float(loss_per_btc * size)
    max_profit = float(profit_per_btc * size)
    
    print(f"\n[3] Risk/Reward Analysis (0.001 BTC):")
    print(f"    Max Loss:     ${max_loss:,.2f} ({-5.0:.1f}%)")
    print(f"    Max Profit:   ${max_profit:,.2f} ({5.0:.1f}%)")
    print(f"    Risk/Reward:  1:{max_profit/max_loss:.2f}")
    
    # Step 4: Create order payloads
    print(f"\n[4] Order Payloads:")
    
    # Main limit order
    main_order = create_order_payload(side, order_prices['entry'], 0.001)
    print(f"\n    Main Order (Limit):")
    print(f"    {json.dumps(main_order, indent=6)}")
    
    # Stop loss order (conditional)
    sl_order = create_order_payload(
        "SELL" if side == "BUY" else "BUY",
        order_prices['stop_loss'],
        0.001
    )
    sl_order["type"] = "STOP_MARKET"
    sl_order["trigger_price"] = f"{order_prices['stop_loss']:.1f}"
    print(f"\n    Stop Loss Order:")
    print(f"    {json.dumps(sl_order, indent=6)}")
    
    # Take profit order (conditional)
    tp_order = create_order_payload(
        "SELL" if side == "BUY" else "BUY",
        order_prices['take_profit'],
        0.001
    )
    tp_order["type"] = "LIMIT"
    print(f"\n    Take Profit Order:")
    print(f"    {json.dumps(tp_order, indent=6)}")
    
    # Step 5: Execution instructions
    print("\n" + "="*70)
    print("EXECUTION INSTRUCTIONS")
    print("="*70)
    print("\nTo place these orders, you need:")
    print("  1. API key from Paradex")
    print("  2. Funded testnet account")
    print("  3. POST to /v1/orders with Authorization header")
    print("\nExample:")
    print("  curl -X POST https://api.testnet.paradex.trade/v1/orders \\")
    print("    -H 'Authorization: YOUR_API_KEY' \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{...order_payload...}'")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
