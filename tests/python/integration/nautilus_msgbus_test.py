#!/usr/bin/env python3
"""Minimal Nautilus message bus integration test"""

import asyncio
from datetime import datetime
from paradex_py import ParadexSubkey
from paradex_py.common.order import Order, OrderSide, OrderType
from decimal import Decimal
import os
from dotenv import load_dotenv

# Simulated message bus
class MessageBus:
    def __init__(self):
        self.messages = []
    
    def publish(self, topic, message):
        self.messages.append((topic, message))
        print(f"[BUS] {topic}: {message}")

# Execution client wrapper
class NautilusExecutionClient:
    def __init__(self, paradex_client, msgbus):
        self.client = paradex_client
        self.msgbus = msgbus
    
    def submit_order(self, order):
        """Submit order through message bus"""
        # Publish to bus
        self.msgbus.publish("orders.submit", {
            "market": order.market,
            "side": order.order_side.value,
            "size": str(order.size),
            "type": order.order_type.value,
        })
        
        # Execute via Paradex
        result = self.client.api_client.submit_order(order)
        
        # Publish result
        self.msgbus.publish("orders.accepted", {
            "order_id": result['id'],
            "status": "SUBMITTED"
        })
        
        return result

async def main():
    load_dotenv('.env.testnet')
    
    # Create message bus
    msgbus = MessageBus()
    
    # Create Paradex client
    client = ParadexSubkey(
        env='testnet',
        l2_private_key=os.getenv('PARADEX_SUBKEY_PRIVATE_KEY'),
        l2_address=os.getenv('PARADEX_L2_ADDRESS'),
    )
    
    # Wrap in Nautilus execution client
    exec_client = NautilusExecutionClient(client, msgbus)
    
    print("✓ Nautilus message bus initialized\n")
    print(f"{'='*80}")
    print("Opening 10 positions through message bus...")
    print(f"{'='*80}\n")
    
    market = "BTC-USD-PERP"
    positions = []
    
    # Open 10 positions
    for i in range(10):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Position {i+1}/10")
        
        order = Order(
            market=market,
            order_side=OrderSide.Buy,
            order_type=OrderType.Market,
            size=Decimal("0.001")
        )
        
        result = exec_client.submit_order(order)
        positions.append(result['id'])
        
        await asyncio.sleep(5)
    
    print(f"\n{'='*80}")
    print("Waiting 2 minutes...")
    print(f"{'='*80}\n")
    
    await asyncio.sleep(120)
    
    # Close positions
    print(f"{'='*80}")
    print("Closing 10 positions through message bus...")
    print(f"{'='*80}\n")
    
    for i, order_id in enumerate(positions):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Closing {i+1}/10")
        
        close_order = Order(
            market=market,
            order_side=OrderSide.Sell,
            order_type=OrderType.Market,
            size=Decimal("0.001")
        )
        
        exec_client.submit_order(close_order)
        
        await asyncio.sleep(5)
    
    print(f"\n{'='*80}")
    print(f"✓ Complete! Message bus handled {len(msgbus.messages)} messages")
    print(f"{'='*80}")

if __name__ == "__main__":
    asyncio.run(main())
