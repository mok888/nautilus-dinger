"""Live data stream for top 5 markets via WebSocket with latency."""

import os
import sys
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from paradex_py import ParadexSubkey

sys.path.insert(0, '/home/mok/projects/nautilus-dinger')
import paradex_adapter

load_dotenv('.env.testnet')

client = ParadexSubkey(
    env='testnet',
    l2_private_key=os.getenv('PARADEX_SUBKEY_PRIVATE_KEY'),
    l2_address=os.getenv('PARADEX_L2_ADDRESS')
)

# Get top 5 by volume
summaries = client.api_client.fetch_markets_summary(params={'market': 'ALL'})
top5 = sorted(summaries['results'], key=lambda x: float(x.get('volume_24h', 0)), reverse=True)[:5]
top5_symbols = [m['symbol'] for m in top5]

# Connect WebSocket
ws = paradex_adapter.PyParadexWebSocket()
ws.connect("wss://ws.api.testnet.paradex.trade/v1")
ws.authenticate(client.account.jwt_token)

# Subscribe to top 5
for symbol in top5_symbols:
    ws.subscribe(f"markets_summary.{symbol}")

print(f"🔴 LIVE: Top 5 Markets - {', '.join(top5_symbols)}\n")
print(f"{'Market':<20} {'Price':>12} {'24h Vol':>12} {'Funding':>10} {'24h Chg':>10} {'Updated':>10}")
print("=" * 90)

# Print initial rows
for sym in top5_symbols:
    print(f"{sym:<20} {'Waiting...':>12}")

market_data = {}
msg_count = 0
line_map = {sym: i for i, sym in enumerate(top5_symbols)}  # Track which line each market is on

try:
    while True:
        start = time.time()
        msg = ws.recv()
        latency_ms = (time.time() - start) * 1000
        
        if msg:
            msg_count += 1
            data = json.loads(msg)
            
            if 'params' in data:
                channel = data['params']['channel']
                if channel.startswith('markets_summary.'):
                    market = channel.replace('markets_summary.', '')
                    info = data['params']['data']
                    
                    market_data[market] = {
                        'mark_price': info.get('mark_price', 'N/A'),
                        'volume_24h': float(info.get('volume_24h', 0)),
                        'funding_rate': float(info.get('funding_rate', 0)) * 100,
                        'price_change': float(info.get('price_change_rate_24h', 0)) * 100,
                        'last_update': datetime.now().strftime('%H:%M:%S')
                    }
                    
                    # Move cursor to the market's line and update
                    line_num = line_map[market]
                    d = market_data[market]
                    price_color = '\033[92m' if d['price_change'] >= 0 else '\033[91m'
                    reset = '\033[0m'
                    
                    # Move cursor up to the correct line, update, then return
                    lines_to_move = len(top5_symbols) - line_num
                    print(f"\033[{lines_to_move}A\r{market:<20} ${d['mark_price']:>11} ${d['volume_24h']:>11,.0f} {d['funding_rate']:>9.3f}% {price_color}{d['price_change']:>9.2f}%{reset} {d['last_update']:>10} | {latency_ms:>5.1f}ms\033[{lines_to_move}B", end='', flush=True)
        
        time.sleep(0.01)  # Small delay to prevent CPU spinning

except KeyboardInterrupt:
    print("\n\n✓ Stream stopped")
    ws.close()
