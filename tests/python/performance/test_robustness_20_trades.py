#!/usr/bin/env python3
"""
Nautilus Trader Paradex Adapter - Robustness Test
20 market orders with 20 second delays
"""
import os
import asyncio
from dotenv import load_dotenv

load_dotenv(".env.testnet")

async def main():
    from paradex_py import ParadexSubkey
    from paradex_py.common.order import Order, OrderSide, OrderType
    from decimal import Decimal
    
    print("="*70)
    print("NAUTILUS PARADEX ADAPTER - 20 TRADE ROBUSTNESS TEST")
    print("="*70)
    
    paradex = ParadexSubkey(
        env="testnet",
        l2_private_key=os.getenv("PARADEX_SUBKEY_PRIVATE_KEY"),
        l2_address=os.getenv("PARADEX_L2_ADDRESS")
    )
    
    print("\n[SETUP] Checking initial state...")
    positions = paradex.api_client.fetch_positions()
    initial_pos = next((p for p in positions["results"] if Decimal(p["size"]) != 0), None)
    if initial_pos:
        print(f"⚠️  Existing position: {initial_pos['market']} {initial_pos['size']}")
    else:
        print("✅ No existing positions")
    
    # Cancel all orders
    paradex.api_client.cancel_all_orders()
    print("✅ Cancelled all open orders")
    
    print(f"\n[START] Executing 20 market orders (20s delay between trades)")
    print("="*70)
    
    trade_results = []
    
    for i in range(1, 21):
        print(f"\n--- Trade {i}/20 ---")
        
        # Get current price
        orderbook = paradex.api_client.fetch_orderbook("BTC-USD-PERP")
        bid = Decimal(orderbook["bids"][0][0])
        ask = Decimal(orderbook["asks"][0][0])
        mid = (bid + ask) / 2
        
        print(f"Price: ${float(mid):,.2f}")
        
        # Alternate buy/sell
        side = OrderSide.Buy if i % 2 == 1 else OrderSide.Sell
        
        # Place market order
        order = Order(
            market="BTC-USD-PERP",
            order_side=side,
            order_type=OrderType.Market,
            size=Decimal("0.001")
        )
        
        try:
            result = paradex.api_client.submit_order(order)
            order_id = result["id"]
            status = result["status"]
            
            trade_results.append({
                "trade": i,
                "side": "BUY" if side == OrderSide.Buy else "SELL",
                "price": float(mid),
                "order_id": order_id,
                "status": status,
                "success": True
            })
            
            print(f"✅ {side.name.upper()} 0.001 BTC")
            print(f"   Order ID: {order_id}")
            print(f"   Status: {status}")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
            trade_results.append({
                "trade": i,
                "side": "BUY" if side == OrderSide.Buy else "SELL",
                "price": float(mid),
                "error": str(e),
                "success": False
            })
        
        # Wait 20 seconds before next trade
        if i < 20:
            print(f"⏳ Waiting 20 seconds...")
            await asyncio.sleep(20)
    
    # Final summary
    print("\n" + "="*70)
    print("TEST COMPLETE - SUMMARY")
    print("="*70)
    
    successful = sum(1 for t in trade_results if t["success"])
    failed = len(trade_results) - successful
    
    print(f"\nTotal trades: {len(trade_results)}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    
    # Check final position
    print("\n[FINAL STATE]")
    final_positions = paradex.api_client.fetch_positions()
    for pos in final_positions["results"]:
        size = Decimal(pos["size"])
        if size != 0:
            print(f"Position: {pos['market']} {size} @ ${pos['average_entry_price']}")
    
    # Show trade log
    print("\n[TRADE LOG]")
    for t in trade_results:
        if t["success"]:
            print(f"  {t['trade']:2d}. {t['side']:4s} @ ${t['price']:,.2f} - {t['order_id']}")
        else:
            print(f"  {t['trade']:2d}. {t['side']:4s} @ ${t['price']:,.2f} - FAILED: {t.get('error', 'Unknown')}")
    
    print("\n" + "="*70)
    print(f"ROBUSTNESS TEST: {successful}/{len(trade_results)} trades successful")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
