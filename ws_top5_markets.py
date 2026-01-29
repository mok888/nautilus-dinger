"""Get top 5 markets via WebSocket."""

import os
import sys
import json
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

# Get all markets
markets_data = client.api_client.fetch_markets()
all_markets = [m['symbol'] for m in markets_data['results']]

# Get market summaries to find top 5 by volume
summaries = client.api_client.fetch_markets_summary(params={'market': 'ALL'})
top5 = sorted(summaries['results'], key=lambda x: float(x.get('volume_24h', 0)), reverse=True)[:5]
top5_symbols = [m['symbol'] for m in top5]

print(f"Top 5 markets by 24h volume: {', '.join(top5_symbols)}\n")

# Connect WebSocket
ws = paradex_adapter.PyParadexWebSocket()
ws.connect("wss://ws.api.testnet.paradex.trade/v1")
ws.authenticate(client.account.jwt_token)

# Subscribe to top 5
for symbol in top5_symbols:
    ws.subscribe(f"markets_summary.{symbol}")

print("Market                 | Mark Price | 24h Volume  | Funding Rate | Open Interest")
print("-" * 90)

market_data = {}
while len(market_data) < 5:
    msg = ws.recv()
    if msg:
        data = json.loads(msg)
        if 'params' in data:
            channel = data['params']['channel']
            if channel.startswith('markets_summary.'):
                market = channel.replace('markets_summary.', '')
                info = data['params']['data']
                
                mark_price = info.get('mark_price', 'N/A')
                volume = float(info.get('volume_24h', 0))
                funding = float(info.get('funding_rate', 0)) * 100
                oi = float(info.get('open_interest', 0))
                
                market_data[market] = True
                print(f"{market:22} | ${mark_price:>9} | ${volume:>10,.0f} | {funding:>7.3f}% | ${oi:>12,.0f}")

ws.close()
print("\n✓ Real-time data received via WebSocket")
