#!/usr/bin/env python3
"""
Real-time monitoring dashboard for Paradex adapter
"""
import os
import sys
import asyncio
import json
import time
from datetime import datetime
from collections import deque

sys.path.insert(0, '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages')
os.environ['PYTHONPATH'] = '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages'

from dotenv import load_dotenv
load_dotenv(".env.testnet")

import paradex_adapter


class MonitoringDashboard:
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.latencies = deque(maxlen=100)
        self.last_price = None
        self.start_time = time.time()
        
    def record_request(self, latency_ms, success=True):
        self.request_count += 1
        if not success:
            self.error_count += 1
        self.latencies.append(latency_ms)
    
    def get_stats(self):
        uptime = time.time() - self.start_time
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
        success_rate = ((self.request_count - self.error_count) / self.request_count * 100) if self.request_count > 0 else 0
        
        return {
            "uptime": uptime,
            "requests": self.request_count,
            "errors": self.error_count,
            "success_rate": success_rate,
            "avg_latency": avg_latency,
            "min_latency": min(self.latencies) if self.latencies else 0,
            "max_latency": max(self.latencies) if self.latencies else 0,
        }


async def monitor_loop(client, dashboard):
    """Main monitoring loop"""
    while True:
        try:
            # Fetch orderbook
            start = time.time()
            orderbook_json = await client.get_orderbook("BTC-USD-PERP")
            latency = (time.time() - start) * 1000
            
            orderbook = json.loads(orderbook_json)
            dashboard.record_request(latency, success=True)
            dashboard.last_price = float(orderbook["asks"][0][0])
            
        except Exception as e:
            dashboard.record_request(0, success=False)
            print(f"Error: {e}")
        
        await asyncio.sleep(1)


async def display_dashboard(dashboard):
    """Display dashboard"""
    while True:
        stats = dashboard.get_stats()
        
        print("\033[2J\033[H")  # Clear screen
        print("="*70)
        print("PARADEX ADAPTER - MONITORING DASHBOARD")
        print("="*70)
        print(f"\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Uptime: {stats['uptime']:.0f}s")
        
        print("\n" + "-"*70)
        print("PERFORMANCE METRICS")
        print("-"*70)
        print(f"Total Requests:    {stats['requests']}")
        print(f"Errors:            {stats['errors']}")
        print(f"Success Rate:      {stats['success_rate']:.1f}%")
        print(f"")
        print(f"Avg Latency:       {stats['avg_latency']:.1f}ms")
        print(f"Min Latency:       {stats['min_latency']:.1f}ms")
        print(f"Max Latency:       {stats['max_latency']:.1f}ms")
        
        if dashboard.last_price:
            print("\n" + "-"*70)
            print("MARKET DATA")
            print("-"*70)
            print(f"BTC-USD-PERP:      ${dashboard.last_price:,.2f}")
        
        print("\n" + "-"*70)
        print("RATE LIMITING")
        print("-"*70)
        print(f"Limit:             10 req/sec")
        print(f"Current Rate:      {stats['requests']/stats['uptime']:.1f} req/sec")
        
        print("\n" + "="*70)
        print("Press Ctrl+C to stop")
        
        await asyncio.sleep(1)


async def main():
    print("Starting monitoring dashboard...")
    
    config = paradex_adapter.PyParadexConfig(
        "testnet",
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_SUBKEY_PRIVATE_KEY")
    )
    client = paradex_adapter.PyHttpClient(config)
    dashboard = MonitoringDashboard()
    
    # Run both tasks
    try:
        await asyncio.gather(
            monitor_loop(client, dashboard),
            display_dashboard(dashboard)
        )
    except KeyboardInterrupt:
        print("\n\n✅ Monitoring stopped")


if __name__ == "__main__":
    asyncio.run(main())
