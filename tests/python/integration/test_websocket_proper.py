"""Test WebSocket using paradex-py client directly."""

import os
import asyncio
from dotenv import load_dotenv
from paradex_py import ParadexSubkey
from paradex_py.api.ws_client import ParadexWebsocketChannel

load_dotenv('.env.testnet')

async def main():
    # Initialize client
    print("Initializing client...")
    client = ParadexSubkey(
        env='testnet',
        l2_private_key=os.getenv('PARADEX_SUBKEY_PRIVATE_KEY'),
        l2_address=os.getenv('PARADEX_L2_ADDRESS')
    )
    print("Client initialized")

    # Initialize account for authenticated channels
    print("Initializing account...")
    client.ws_client.init_account(client.account)
    print("Account initialized")

    # Connect
    print(f"Connecting to {client.ws_client.api_url}...")
    try:
        result = await asyncio.wait_for(client.ws_client.connect(), timeout=5.0)
        if not result:
            print("Failed to connect")
            return
        print("Connected!")
    except asyncio.TimeoutError:
        print("Connection timeout")
        return
    except Exception as e:
        print(f"Connection error: {e}")
        return

    # Subscribe to BBO (Best Bid/Offer) for BTC-USD-PERP
    def on_bbo(data):
        print(f"BBO: {data}")

    client.ws_client.subscribe(
        ParadexWebsocketChannel.BBO,
        on_bbo,
        params={"market": "BTC-USD-PERP"}
    )

    print("Subscribed to BTC-USD-PERP BBO")
    print("Subscriptions:", client.ws_client.get_subscriptions())

    # Pump messages for 10 seconds
    for i in range(100):
        await client.ws_client.pump_once()
        await asyncio.sleep(0.1)

    print("\nClosing connection...")
    await client.ws_client.close()

if __name__ == "__main__":
    asyncio.run(main())
