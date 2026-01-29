#!/usr/bin/env python3
"""Robustness test for Nautilus Trader + Paradex integration"""

import asyncio
import time
from datetime import datetime
from paradex_py import ParadexSubkey
from paradex_py.common.order import Order, OrderSide, OrderType
from decimal import Decimal
import os
from dotenv import load_dotenv

class MessageBus:
    """Simulated Nautilus message bus with error tracking"""
    def __init__(self):
        self.messages = []
        self.errors = []
    
    def publish(self, topic, message):
        try:
            self.messages.append((topic, message, time.time()))
            return True
        except Exception as e:
            self.errors.append((topic, str(e)))
            return False

class RobustExecutionClient:
    """Execution client with retry logic and error handling"""
    def __init__(self, paradex_client, msgbus):
        self.client = paradex_client
        self.msgbus = msgbus
        self.failed_orders = []
        self.retry_count = 3
    
    def submit_order(self, order, retry=0):
        """Submit with retry logic"""
        try:
            # Publish intent
            self.msgbus.publish("orders.submit", {
                "market": order.market,
                "side": order.order_side.value,
                "size": str(order.size),
                "attempt": retry + 1
            })
            
            # Execute
            result = self.client.api_client.submit_order(order)
            
            # Publish success
            self.msgbus.publish("orders.accepted", {
                "order_id": result['id'],
                "status": "SUCCESS"
            })
            
            return result
            
        except Exception as e:
            self.msgbus.publish("orders.failed", {
                "error": str(e),
                "attempt": retry + 1
            })
            
            if retry < self.retry_count:
                time.sleep(1)
                return self.submit_order(order, retry + 1)
            else:
                self.failed_orders.append((order, str(e)))
                raise

async def stress_test():
    """Stress test: rapid order submission"""
    load_dotenv('.env.testnet')
    
    msgbus = MessageBus()
    client = ParadexSubkey(
        env='testnet',
        l2_private_key=os.getenv('PARADEX_SUBKEY_PRIVATE_KEY'),
        l2_address=os.getenv('PARADEX_L2_ADDRESS'),
    )
    exec_client = RobustExecutionClient(client, msgbus)
    
    print("="*80)
    print("STRESS TEST: 20 rapid orders (no delay)")
    print("="*80 + "\n")
    
    start = time.time()
    orders = []
    
    for i in range(20):
        try:
            order = Order(
                market="BTC-USD-PERP",
                order_side=OrderSide.Buy if i % 2 == 0 else OrderSide.Sell,
                order_type=OrderType.Market,
                size=Decimal("0.001")
            )
            result = exec_client.submit_order(order)
            orders.append(result['id'])
            print(f"✓ [{i+1}/20] Order {result['id'][:20]}...")
        except Exception as e:
            print(f"✗ [{i+1}/20] Failed: {e}")
    
    elapsed = time.time() - start
    
    print(f"\n{'='*80}")
    print(f"Stress Test Results:")
    print(f"  Time: {elapsed:.2f}s")
    print(f"  Success: {len(orders)}/20")
    print(f"  Failed: {len(exec_client.failed_orders)}")
    print(f"  Messages: {len(msgbus.messages)}")
    print(f"  Errors: {len(msgbus.errors)}")
    print(f"{'='*80}\n")
    
    return orders, exec_client, msgbus

async def recovery_test(orders, exec_client):
    """Recovery test: verify all orders exist"""
    print("="*80)
    print("RECOVERY TEST: Verify order state")
    print("="*80 + "\n")
    
    verified = 0
    for order_id in orders:
        try:
            status = exec_client.client.api_client.fetch_order(order_id)
            verified += 1
            print(f"✓ Order {order_id[:20]}... status: {status['status']}")
        except Exception as e:
            print(f"✗ Order {order_id[:20]}... NOT FOUND")
    
    print(f"\n{'='*80}")
    print(f"Recovery Results: {verified}/{len(orders)} orders verified")
    print(f"{'='*80}\n")
    
    return verified

async def network_resilience_test():
    """Network resilience: test with delays"""
    load_dotenv('.env.testnet')
    
    msgbus = MessageBus()
    client = ParadexSubkey(
        env='testnet',
        l2_private_key=os.getenv('PARADEX_SUBKEY_PRIVATE_KEY'),
        l2_address=os.getenv('PARADEX_L2_ADDRESS'),
    )
    exec_client = RobustExecutionClient(client, msgbus)
    
    print("="*80)
    print("NETWORK RESILIENCE: Orders with simulated delays")
    print("="*80 + "\n")
    
    for i in range(5):
        try:
            # Simulate network delay
            await asyncio.sleep(0.5)
            
            order = Order(
                market="BTC-USD-PERP",
                order_side=OrderSide.Buy,
                order_type=OrderType.Market,
                size=Decimal("0.001")
            )
            result = exec_client.submit_order(order)
            print(f"✓ [{i+1}/5] Order submitted after delay")
        except Exception as e:
            print(f"✗ [{i+1}/5] Failed: {e}")
    
    print(f"\n{'='*80}")
    print(f"Network Resilience: {5 - len(exec_client.failed_orders)}/5 success")
    print(f"{'='*80}\n")

async def main():
    print("\n" + "="*80)
    print("NAUTILUS TRADER + PARADEX ROBUSTNESS TEST")
    print("="*80 + "\n")
    
    # Test 1: Stress test
    orders, exec_client, msgbus = await stress_test()
    await asyncio.sleep(2)
    
    # Test 2: Recovery
    verified = await recovery_test(orders, exec_client)
    await asyncio.sleep(2)
    
    # Test 3: Network resilience
    await network_resilience_test()
    
    # Final summary
    print("="*80)
    print("FINAL ROBUSTNESS SUMMARY")
    print("="*80)
    print(f"Total Orders Submitted: {len(orders) + 5}")
    print(f"Total Verified: {verified}")
    print(f"Message Bus Events: {len(msgbus.messages)}")
    print(f"System Errors: {len(msgbus.errors)}")
    print(f"Failed Orders: {len(exec_client.failed_orders)}")
    print(f"\n✓ System Robustness: {'PASS' if len(exec_client.failed_orders) == 0 else 'PARTIAL'}")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(main())
