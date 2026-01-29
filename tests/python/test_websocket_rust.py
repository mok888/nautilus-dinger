"""Test WebSocket with Rust JSON-RPC client."""

import os
import sys
from dotenv import load_dotenv
from paradex_py import ParadexSubkey

# Add paradex_adapter to path
sys.path.insert(0, '/home/mok/projects/nautilus-dinger')
import paradex_adapter

load_dotenv('.env.testnet')

# Get JWT token
client = ParadexSubkey(
    env='testnet',
    l2_private_key=os.getenv('PARADEX_SUBKEY_PRIVATE_KEY'),
    l2_address=os.getenv('PARADEX_L2_ADDRESS')
)

jwt_token = client.account.jwt_token
print(f"JWT Token: {jwt_token[:50]}...")

# Create WebSocket client
ws = paradex_adapter.PyParadexWebSocket()

# Connect
url = "wss://ws.api.testnet.paradex.trade/v1"
print(f"Connecting to {url}...")
ws.connect(url)
print("Connected!")

# Authenticate
print("Authenticating...")
ws.authenticate(jwt_token)
print("Authenticated!")

# Subscribe to trades (more active)
print("Subscribing to trades.BTC-USD-PERP...")
ws.subscribe("trades.BTC-USD-PERP")
print("Subscribed!")

# Receive messages
print("\nReceiving messages (30 seconds)...")
import time
start = time.time()
count = 0
while time.time() - start < 30:
    msg = ws.recv()
    if msg:
        count += 1
        print(f"Raw message {count}: {msg[:300]}")
    else:
        time.sleep(0.1)

print("\nClosing...")
ws.close()
print("Done!")
