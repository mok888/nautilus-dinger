#!/usr/bin/env python3
import os
import asyncio
from dotenv import load_dotenv

load_dotenv(".env.testnet")

L2_ADDRESS = os.getenv("PARADEX_L2_ADDRESS")
SUBKEY = os.getenv("PARADEX_SUBKEY_PRIVATE_KEY")

async def main():
    from paradex_py import ParadexSubkey
    from paradex_py.common.order import Order, OrderSide, OrderType
    from decimal import Decimal
    
    paradex = ParadexSubkey(
        env="testnet",
        l2_private_key=SUBKEY,
        l2_address=L2_ADDRESS
    )
    
    # Check positions
    print("Fetching positions...")
    positions = paradex.api_client.fetch_positions()
    
    if not positions.get("results"):
        print("No open positions")
        return
    
    print(f"\nOpen positions: {len(positions['results'])}")
    for pos in positions["results"]:
        size = float(pos["size"])
        if size != 0:
            print(f"  {pos['market']}: {size} @ ${pos['average_entry_price']}")
    
    # Close all positions
    confirm = input("\nClose all positions? (yes/no): ")
    if confirm.lower() != "yes":
        print("Cancelled")
        return
    
    print("\nClosing positions...")
    for pos in positions["results"]:
        size = Decimal(pos["size"])
        if size == 0:
            continue
            
        market = pos["market"]
        side = OrderSide.Sell if size > 0 else OrderSide.Buy
        
        order = Order(
            market=market,
            order_side=side,
            order_type=OrderType.Market,
            size=abs(size)
        )
        
        result = paradex.api_client.submit_order(order)
        print(f"✅ Closed {market}: {result['id']}")
    
    print("\nAll positions closed")

if __name__ == "__main__":
    asyncio.run(main())
