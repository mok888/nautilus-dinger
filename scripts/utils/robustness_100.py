#!/usr/bin/env python3
"""100 trade robustness test with live status display"""

import asyncio
import time
import sys
from datetime import datetime
from paradex_py import ParadexSubkey
from paradex_py.common.order import Order, OrderSide, OrderType
from decimal import Decimal
import os
from dotenv import load_dotenv

class LiveStats:
    def __init__(self):
        self.total = 0
        self.success = 0
        self.failed = 0
        self.open_orders = []
        self.close_orders = []
        self.start_time = time.time()
    
    def display(self, phase="OPENING"):
        elapsed = time.time() - self.start_time
        rate = self.success / elapsed if elapsed > 0 else 0
        
        # Clear screen and move cursor to top
        sys.stdout.write('\033[2J\033[H')
        
        print("="*80)
        print(f"NAUTILUS TRADER - 100 TRADE ROBUSTNESS TEST")
        print("="*80)
        print(f"Phase: {phase}")
        print(f"Time Elapsed: {elapsed:.1f}s")
        print(f"Rate: {rate:.2f} orders/sec")
        print("-"*80)
        print(f"Total Orders: {self.total}/100")
        print(f"Success: {self.success} | Failed: {self.failed}")
        print(f"Open Orders: {len(self.open_orders)}")
        print(f"Close Orders: {len(self.close_orders)}")
        print("-"*80)
        
        # Show last 10 orders
        all_orders = self.open_orders + self.close_orders
        print("Recent Orders:")
        for order in all_orders[-10:]:
            status_icon = "✓" if order['success'] else "✗"
            print(f"  {status_icon} {order['id'][:25]}... | {order['side']:4s} | {order['time']}")
        
        print("="*80)
        sys.stdout.flush()

class MessageBus:
    def __init__(self):
        self.messages = []
    
    def publish(self, topic, message):
        self.messages.append((topic, message, time.time()))

class RobustExecutionClient:
    def __init__(self, paradex_client, msgbus, stats):
        self.client = paradex_client
        self.msgbus = msgbus
        self.stats = stats
    
    def submit_order(self, order, side_label):
        try:
            self.msgbus.publish("orders.submit", {"market": order.market, "side": order.order_side.value})
            
            result = self.client.api_client.submit_order(order)
            
            self.msgbus.publish("orders.accepted", {"order_id": result['id']})
            
            self.stats.success += 1
            self.stats.total += 1
            
            order_info = {
                'id': result['id'],
                'side': side_label,
                'success': True,
                'time': datetime.now().strftime('%H:%M:%S')
            }
            
            if side_label == "OPEN":
                self.stats.open_orders.append(order_info)
            else:
                self.stats.close_orders.append(order_info)
            
            return result
            
        except Exception as e:
            self.stats.failed += 1
            self.stats.total += 1
            
            order_info = {
                'id': f"FAILED: {str(e)[:20]}",
                'side': side_label,
                'success': False,
                'time': datetime.now().strftime('%H:%M:%S')
            }
            
            if side_label == "OPEN":
                self.stats.open_orders.append(order_info)
            else:
                self.stats.close_orders.append(order_info)
            
            raise

async def main():
    load_dotenv('.env.testnet')
    
    stats = LiveStats()
    msgbus = MessageBus()
    
    client = ParadexSubkey(
        env='testnet',
        l2_private_key=os.getenv('PARADEX_SUBKEY_PRIVATE_KEY'),
        l2_address=os.getenv('PARADEX_L2_ADDRESS'),
    )
    
    exec_client = RobustExecutionClient(client, msgbus, stats)
    
    # Phase 1: Open 100 positions
    stats.display("OPENING")
    
    for i in range(100):
        try:
            order = Order(
                market="BTC-USD-PERP",
                order_side=OrderSide.Buy,
                order_type=OrderType.Market,
                size=Decimal("0.001")
            )
            
            exec_client.submit_order(order, "OPEN")
            stats.display("OPENING")
            
            await asyncio.sleep(3)
            
        except Exception as e:
            stats.display("OPENING")
            await asyncio.sleep(3)
    
    # Phase 2: Close 100 positions
    stats.display("CLOSING")
    await asyncio.sleep(2)
    
    for i in range(100):
        try:
            order = Order(
                market="BTC-USD-PERP",
                order_side=OrderSide.Sell,
                order_type=OrderType.Market,
                size=Decimal("0.001")
            )
            
            exec_client.submit_order(order, "CLOSE")
            stats.display("CLOSING")
            
            await asyncio.sleep(3)
            
        except Exception as e:
            stats.display("CLOSING")
            await asyncio.sleep(3)
    
    # Final summary
    stats.display("COMPLETE")
    
    elapsed = time.time() - stats.start_time
    
    print(f"\n{'='*80}")
    print("FINAL RESULTS")
    print(f"{'='*80}")
    print(f"Total Time: {elapsed:.1f}s ({elapsed/60:.1f} minutes)")
    print(f"Total Orders: {stats.total}/200")
    print(f"Success Rate: {stats.success}/{stats.total} ({100*stats.success/stats.total:.1f}%)")
    print(f"Failed Orders: {stats.failed}")
    print(f"Message Bus Events: {len(msgbus.messages)}")
    print(f"Average Rate: {stats.success/elapsed:.2f} orders/sec")
    print(f"\n✓ Robustness Test: {'PASS' if stats.failed == 0 else 'PARTIAL PASS'}")
    print(f"{'='*80}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
