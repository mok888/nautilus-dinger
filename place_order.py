#!/usr/bin/env python3
import os
import asyncio
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv(".env.testnet")

L2_ADDRESS = os.getenv("PARADEX_L2_ADDRESS")
SUBKEY = os.getenv("PARADEX_SUBKEY_PRIVATE_KEY")

async def main():
    from paradex_py import ParadexSubkey
    
    # Initialize with L2 credentials only
    paradex = ParadexSubkey(
        env="testnet",
        l2_private_key=SUBKEY,
        l2_address=L2_ADDRESS
    )
    
    # Get BTC price
    orderbook = paradex.api_client.fetch_orderbook("BTC-USD-PERP")
    ask = Decimal(orderbook["asks"][0][0])
    print(f"BTC Ask: ${float(ask):,.2f}")
    
    # Calculate entry -5bps
    entry = ask * Decimal("0.9995")
    entry = (entry / Decimal("0.1")).quantize(Decimal("1")) * Decimal("0.1")  # Round to 0.1
    print(f"Entry: ${float(entry):,.2f} (-5bps)")
    print(f"SL: ${float(entry * Decimal('0.95')):,.2f} (-5%)")
    print(f"TP: ${float(entry * Decimal('1.05')):,.2f} (+5%)")
    
    # Place order
    from paradex_py.common.order import Order, OrderSide, OrderType
    
    order = Order(
        market="BTC-USD-PERP",
        order_side=OrderSide.Buy,
        order_type=OrderType.Limit,
        size=Decimal("0.001"),
        limit_price=entry
    )
    
    print("\nPlacing order...")
    result = paradex.api_client.submit_order(order)
    print(f"✅ Order placed: {result['id']}")

if __name__ == "__main__":
    asyncio.run(main())
