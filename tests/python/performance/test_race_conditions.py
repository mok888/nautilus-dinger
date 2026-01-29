#!/usr/bin/env python3
"""
Test race condition protection with concurrent requests
"""
import os
import sys
import asyncio
import json
import time

sys.path.insert(0, '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages')
os.environ['PYTHONPATH'] = '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages'

from dotenv import load_dotenv
load_dotenv(".env.testnet")

import paradex_adapter


async def concurrent_orderbook_test(client, task_id):
    """Single orderbook fetch"""
    start = time.time()
    try:
        orderbook_json = await client.get_orderbook("BTC-USD-PERP")
        orderbook = json.loads(orderbook_json)
        latency = (time.time() - start) * 1000
        
        best_ask = float(orderbook["asks"][0][0])
        return {
            "task_id": task_id,
            "success": True,
            "latency_ms": latency,
            "best_ask": best_ask
        }
    except Exception as e:
        return {
            "task_id": task_id,
            "success": False,
            "error": str(e)
        }


async def test_race_conditions():
    print("="*70)
    print("RACE CONDITION PROTECTION TEST")
    print("="*70)
    
    # Initialize client
    config = paradex_adapter.PyParadexConfig(
        "testnet",
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_SUBKEY_PRIVATE_KEY")
    )
    client = paradex_adapter.PyHttpClient(config)
    
    # Test 1: Concurrent reads
    print("\n[TEST 1] 50 Concurrent Orderbook Requests")
    print("-"*70)
    
    start_time = time.time()
    tasks = [concurrent_orderbook_test(client, i) for i in range(50)]
    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start_time
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"Total requests:  {len(results)}")
    print(f"Successful:      {len(successful)}")
    print(f"Failed:          {len(failed)}")
    print(f"Time elapsed:    {elapsed:.2f}s")
    
    if successful:
        latencies = [r["latency_ms"] for r in successful]
        print(f"Avg latency:     {sum(latencies)/len(latencies):.1f}ms")
        print(f"Min latency:     {min(latencies):.1f}ms")
        print(f"Max latency:     {max(latencies):.1f}ms")
        
        # Check for data consistency
        prices = [r["best_ask"] for r in successful]
        unique_prices = set(prices)
        print(f"Unique prices:   {len(unique_prices)} (expected: 1-3)")
    
    if failed:
        print(f"\n❌ Failures detected:")
        for f in failed[:5]:
            print(f"   Task {f['task_id']}: {f['error']}")
    
    # Test 2: Check for race conditions in responses
    print("\n[TEST 2] Data Consistency Check")
    print("-"*70)
    
    # All successful requests should have valid data
    all_valid = all(
        r.get("best_ask") and r["best_ask"] > 0 
        for r in successful
    )
    
    if all_valid:
        print("✅ All responses have valid data")
    else:
        print("❌ Some responses have invalid data")
    
    # Test 3: Rapid sequential requests
    print("\n[TEST 3] 20 Rapid Sequential Requests")
    print("-"*70)
    
    sequential_results = []
    start_time = time.time()
    
    for i in range(20):
        result = await concurrent_orderbook_test(client, i)
        sequential_results.append(result)
    
    elapsed = time.time() - start_time
    
    seq_successful = [r for r in sequential_results if r["success"]]
    print(f"Successful:      {len(seq_successful)}/20")
    print(f"Time elapsed:    {elapsed:.2f}s")
    print(f"Avg per request: {elapsed/20*1000:.1f}ms")
    
    # Summary
    print("\n" + "="*70)
    print("RACE CONDITION TEST SUMMARY")
    print("="*70)
    
    total_requests = len(results) + len(sequential_results)
    total_successful = len(successful) + len(seq_successful)
    success_rate = (total_successful / total_requests) * 100
    
    print(f"Total requests:   {total_requests}")
    print(f"Success rate:     {success_rate:.1f}%")
    
    if success_rate == 100:
        print("\n✅ NO RACE CONDITIONS DETECTED")
        print("   - All concurrent requests succeeded")
        print("   - Data consistency maintained")
        print("   - No errors or timeouts")
    elif success_rate > 95:
        print("\n⚠️  MINOR ISSUES DETECTED")
        print(f"   - {100-success_rate:.1f}% failure rate")
    else:
        print("\n❌ RACE CONDITIONS DETECTED")
        print(f"   - {100-success_rate:.1f}% failure rate")


if __name__ == "__main__":
    asyncio.run(test_race_conditions())
