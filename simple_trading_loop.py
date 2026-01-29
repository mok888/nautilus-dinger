#!/usr/bin/env python3
"""
Simple trading loop: Paradex data -> Decision -> Paradex order -> Feedback
No full Nautilus integration, just the core flow
"""
import os
import time
from decimal import Decimal
from dotenv import load_dotenv
from paradex_py import ParadexSubkey
from paradex_py.common.order import Order, OrderSide, OrderType

load_dotenv(".env.testnet")

def main():
    print("="*70)
    print("PARADEX TRADING LOOP - DATA -> DECISION -> ORDER -> FEEDBACK")
    print("="*70)
    
    # Initialize Paradex client
    print("\n[1] Connecting to Paradex...")
    paradex = ParadexSubkey(
        env="testnet",
        l2_private_key=os.getenv("PARADEX_SUBKEY_PRIVATE_KEY"),
        l2_address=os.getenv("PARADEX_L2_ADDRESS")
    )
    print("✅ Connected")
    
    # Get market data
    print("\n[2] Fetching BTC-USD-PERP market data...")
    orderbook = paradex.api_client.fetch_orderbook("BTC-USD-PERP")
    
    best_bid = float(orderbook["bids"][0][0])
    best_ask = float(orderbook["asks"][0][0])
    mid_price = (best_bid + best_ask) / 2
    
    print(f"   Best Bid: ${best_bid:,.2f}")
    print(f"   Best Ask: ${best_ask:,.2f}")
    print(f"   Mid Price: ${mid_price:,.2f}")
    
    # Trading decision (simple: buy at -5bps from mid)
    print("\n[3] Making trading decision...")
    entry_price = mid_price * 0.9995
    entry_price = round(entry_price, 1)  # Round to 1 decimal place
    size = Decimal("0.001")
    
    print(f"   Decision: BUY {size} BTC @ ${entry_price}")
    
    # Place order via Paradex
    print("\n[4] Submitting order to Paradex...")
    order = Order(
        market="BTC-USD-PERP",
        order_side=OrderSide.Buy,
        order_type=OrderType.Limit,
        size=size,
        limit_price=Decimal(str(entry_price))
    )
    
    result = paradex.api_client.submit_order(order)
    
    order_id = result.get('id')
    print(f"✅ Order submitted!")
    print(f"   Order ID: {order_id}")
    print(f"   Status: {result.get('status')}")
    print(f"   Market: {result.get('market')}")
    print(f"   Side: {result.get('side')}")
    print(f"   Size: {result.get('size')}")
    print(f"   Price: ${entry_price}")
    
    # Get feedback from Paradex
    print("\n[5] Getting order feedback from Paradex...")
    time.sleep(2)  # Wait for order to process
    
    # Fetch specific order
    order_status = paradex.api_client.fetch_order(order_id)
    
    print(f"✅ Order feedback:")
    print(f"   ID: {order_status.get('id')}")
    print(f"   Status: {order_status.get('status')}")
    print(f"   Type: {order_status.get('type')}")
    print(f"   Filled: {order_status.get('filled_qty')} / {order_status.get('size')}")
    print(f"   Limit Price: ${order_status.get('limit_price')}")
    print(f"   Created: {order_status.get('created_at')}")
    print(f"   Updated: {order_status.get('last_updated_at')}")
    
    # Check position
    print("\n[6] Checking positions...")
    positions = paradex.api_client.fetch_positions()
    
    for pos in positions.get("results", []):
        if float(pos.get("size", 0)) != 0:
            print(f"   {pos['market']}: {pos['size']} @ ${pos.get('avg_entry_price', 'N/A')}")
    
    print("\n" + "="*70)
    print("TRADING LOOP COMPLETE")
    print("="*70)
    print("\nFlow demonstrated:")
    print("  1. ✅ Get market data from Paradex")
    print("  2. ✅ Make trading decision")
    print("  3. ✅ Submit order to Paradex")
    print("  4. ✅ Receive order confirmation")
    print("  5. ✅ Get order feedback")
    print("  6. ✅ Check position status")

if __name__ == "__main__":
    main()
