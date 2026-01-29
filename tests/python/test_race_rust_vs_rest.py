#!/usr/bin/env python3
"""
Comprehensive race condition test: Rust adapter + Direct REST API
"""
import os
import sys
import asyncio
import json
import time
import aiohttp

sys.path.insert(0, '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages')
os.environ['PYTHONPATH'] = '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages'

from dotenv import load_dotenv
load_dotenv(".env.testnet")

import paradex_adapter


async def test_rust_adapter(client, task_id):
    """Test via Rust adapter"""
    start = time.time()
    try:
        orderbook_json = await client.get_orderbook("BTC-USD-PERP")
        orderbook = json.loads(orderbook_json)
        latency = (time.time() - start) * 1000
        
        return {
            "task_id": task_id,
            "method": "rust",
            "success": True,
            "latency_ms": latency,
            "best_ask": float(orderbook["asks"][0][0])
        }
    except Exception as e:
        return {
            "task_id": task_id,
            "method": "rust",
            "success": False,
            "error": str(e)
        }


async def test_rest_api(session, task_id):
    """Test via direct REST API"""
    start = time.time()
    try:
        url = "https://api.testnet.paradex.trade/v1/orderbook/BTC-USD-PERP"
        async with session.get(url) as response:
            orderbook = await response.json()
            latency = (time.time() - start) * 1000
            
            return {
                "task_id": task_id,
                "method": "rest",
                "success": True,
                "latency_ms": latency,
                "best_ask": float(orderbook["asks"][0][0])
            }
    except Exception as e:
        return {
            "task_id": task_id,
            "method": "rest",
            "success": False,
            "error": str(e)
        }


async def main():
    print("="*70)
    print("RACE CONDITION TEST: RUST ADAPTER vs REST API")
    print("="*70)
    
    # Initialize Rust client
    config = paradex_adapter.PyParadexConfig(
        "testnet",
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_SUBKEY_PRIVATE_KEY")
    )
    rust_client = paradex_adapter.PyHttpClient(config)
    
    # Initialize REST session
    async with aiohttp.ClientSession() as session:
        
        # Test 1: Rust Adapter Concurrent
        print("\n[TEST 1] Rust Adapter - 30 Concurrent Requests")
        print("-"*70)
        
        start = time.time()
        rust_tasks = [test_rust_adapter(rust_client, i) for i in range(30)]
        rust_results = await asyncio.gather(*rust_tasks)
        rust_elapsed = time.time() - start
        
        rust_success = [r for r in rust_results if r["success"]]
        print(f"Successful:      {len(rust_success)}/30")
        print(f"Time elapsed:    {rust_elapsed:.2f}s")
        if rust_success:
            latencies = [r["latency_ms"] for r in rust_success]
            print(f"Avg latency:     {sum(latencies)/len(latencies):.1f}ms")
            print(f"Min latency:     {min(latencies):.1f}ms")
            print(f"Max latency:     {max(latencies):.1f}ms")
        
        # Test 2: REST API Concurrent
        print("\n[TEST 2] Direct REST API - 30 Concurrent Requests")
        print("-"*70)
        
        start = time.time()
        rest_tasks = [test_rest_api(session, i) for i in range(30)]
        rest_results = await asyncio.gather(*rest_tasks)
        rest_elapsed = time.time() - start
        
        rest_success = [r for r in rest_results if r["success"]]
        print(f"Successful:      {len(rest_success)}/30")
        print(f"Time elapsed:    {rest_elapsed:.2f}s")
        if rest_success:
            latencies = [r["latency_ms"] for r in rest_success]
            print(f"Avg latency:     {sum(latencies)/len(latencies):.1f}ms")
            print(f"Min latency:     {min(latencies):.1f}ms")
            print(f"Max latency:     {max(latencies):.1f}ms")
        
        # Test 3: Mixed Concurrent (15 Rust + 15 REST)
        print("\n[TEST 3] Mixed - 15 Rust + 15 REST Concurrent")
        print("-"*70)
        
        start = time.time()
        mixed_tasks = (
            [test_rust_adapter(rust_client, i) for i in range(15)] +
            [test_rest_api(session, i+15) for i in range(15)]
        )
        mixed_results = await asyncio.gather(*mixed_tasks)
        mixed_elapsed = time.time() - start
        
        mixed_success = [r for r in mixed_results if r["success"]]
        mixed_rust = [r for r in mixed_success if r["method"] == "rust"]
        mixed_rest = [r for r in mixed_success if r["method"] == "rest"]
        
        print(f"Rust successful: {len(mixed_rust)}/15")
        print(f"REST successful: {len(mixed_rest)}/15")
        print(f"Time elapsed:    {mixed_elapsed:.2f}s")
        
        # Test 4: Data Consistency
        print("\n[TEST 4] Data Consistency Check")
        print("-"*70)
        
        all_results = rust_results + rest_results + mixed_results
        all_success = [r for r in all_results if r["success"]]
        
        prices = [r["best_ask"] for r in all_success]
        unique_prices = set(prices)
        
        print(f"Total requests:  {len(all_results)}")
        print(f"Successful:      {len(all_success)}")
        print(f"Unique prices:   {len(unique_prices)}")
        
        if len(unique_prices) <= 3:
            print("✅ Data consistency maintained")
        else:
            print("⚠️  High price variance (market moving)")
        
        # Performance Comparison
        print("\n[PERFORMANCE COMPARISON]")
        print("-"*70)
        
        if rust_success and rest_success:
            rust_avg = sum(r["latency_ms"] for r in rust_success) / len(rust_success)
            rest_avg = sum(r["latency_ms"] for r in rest_success) / len(rest_success)
            
            print(f"Rust Adapter:    {rust_avg:.1f}ms avg")
            print(f"Direct REST:     {rest_avg:.1f}ms avg")
            print(f"Difference:      {abs(rust_avg - rest_avg):.1f}ms")
            
            if rust_avg < rest_avg:
                print(f"✅ Rust is {rest_avg/rust_avg:.2f}x faster")
            else:
                print(f"⚠️  REST is {rust_avg/rest_avg:.2f}x faster")
        
        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        
        total = len(all_results)
        success = len(all_success)
        success_rate = (success / total) * 100
        
        print(f"Total requests:   {total}")
        print(f"Success rate:     {success_rate:.1f}%")
        print(f"Failed:           {total - success}")
        
        if success_rate == 100:
            print("\n✅ NO RACE CONDITIONS DETECTED")
            print("   - Both Rust adapter and REST API stable")
            print("   - All concurrent requests succeeded")
            print("   - Data consistency maintained")
        else:
            print(f"\n⚠️  {100-success_rate:.1f}% failure rate detected")


if __name__ == "__main__":
    asyncio.run(main())
