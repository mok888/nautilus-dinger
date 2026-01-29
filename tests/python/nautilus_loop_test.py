#!/usr/bin/env python3
"""Full loop test through Nautilus Trader message bus"""

import asyncio
from datetime import datetime
from nautilus_trader.config import TradingNodeConfig
from nautilus_trader.live.node import TradingNode
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.objects import Quantity
from nautilus_trader.adapters.paradex.config import ParadexConfig, ParadexExecClientConfig
import os
from dotenv import load_dotenv

load_dotenv('.env')

async def main():
    # Config
    config = TradingNodeConfig(
        trader_id="TESTER-001",
        data_clients={
            "PARADEX": ParadexConfig(
                api_key=os.getenv('PARADEX_API_KEY'),
                api_secret=os.getenv('PARADEX_API_SECRET'),
                l2_address=os.getenv('PARADEX_ACCOUNT_ADDRESS'),
                subkey_private_key=os.getenv('PARADEX_L2_PRIVATE_KEY'),
            ),
        },
        exec_clients={
            "PARADEX": ParadexExecClientConfig(),
        },
    )
    
    # Create node
    node = TradingNode(config=config)
    
    # Start
    await node.start()
    
    print("✓ Connected to Nautilus Trader message bus\n")
    
    instrument_id = InstrumentId.from_str("BTC-USD-PERP.PARADEX")
    
    # Open 10 positions
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Opening 10 positions via Nautilus...\n")
    
    order_ids = []
    for i in range(10):
        order = node.trader.submit_order(
            instrument_id=instrument_id,
            order_side=OrderSide.BUY,
            quantity=Quantity.from_str("0.001"),
        )
        order_ids.append(order.client_order_id)
        
        print(f"  [{i+1}/10] Submitted order {order.client_order_id}")
        
        if i < 9:
            await asyncio.sleep(5)
    
    print(f"\n{'='*80}")
    print("All 10 orders submitted. Waiting 2 minutes...")
    print(f"{'='*80}\n")
    
    await asyncio.sleep(120)
    
    # Close positions
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Closing 10 positions via Nautilus...\n")
    
    for i in range(10):
        order = node.trader.submit_order(
            instrument_id=instrument_id,
            order_side=OrderSide.SELL,
            quantity=Quantity.from_str("0.001"),
        )
        
        print(f"  [{i+1}/10] Submitted close order {order.client_order_id}")
        
        if i < 9:
            await asyncio.sleep(5)
    
    print(f"\n{'='*80}")
    print("✓ Full loop test complete via Nautilus message bus!")
    print(f"{'='*80}")
    
    # Stop
    await node.stop()

if __name__ == "__main__":
    asyncio.run(main())
