"""Full loop test: Paradex → Nautilus → Paradex with feedback.
Opens 5 positions with 10s delay, closes each after 2 mins at market price.
"""

import os
import sys
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

# Get current BTC price
market = "BTC-USD-PERP"
bbo = client.api_client.fetch_bbo(market)
current_price = float(bbo['bid'])
print(f"Current {market} price: ${current_price:,.2f}\n")

positions = []

# Open 10 positions with 5s delay
for i in range(10):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Opening position {i+1}/10...")
    
    # Get fresh price
    bbo = client.api_client.fetch_bbo(market)
    price = float(bbo['bid'])
    
    # Create order via Paradex API
    from paradex_py.common.order import Order, OrderSide, OrderType
    from decimal import Decimal
    
    order = Order(
        market=market,
        order_side=OrderSide.Buy,
        order_type=OrderType.Market,
        size=Decimal("0.001")
    )
    
    order_result = client.api_client.submit_order(order)
    order_id = order_result['id']
    
    # Wait for order to be processed
    time.sleep(1)
    
    # Feedback from Paradex
    order_status = client.api_client.fetch_order(order_id)
    
    positions.append({
        'id': order_id,
        'open_time': time.time(),
        'open_price': price,
        'size': 0.001,
        'status': order_status['status']
    })
    
    print(f"  ✓ Order {order_id} | Status: {order_status['status']} | Price: ${price:,.2f}")
    
    if i < 9:  # Don't delay after last position
        print(f"  Waiting 5s before next position...\n")
        time.sleep(5)

print(f"\n{'='*80}")
print(f"All 10 positions opened. Waiting 2 minutes before closing...")
print(f"{'='*80}\n")

# Wait 2 minutes
time.sleep(120)

# Close all positions
print(f"[{datetime.now().strftime('%H:%M:%S')}] Closing all positions...\n")

for i, pos in enumerate(positions):
    print(f"Closing position {i+1}/10 (Order ID: {pos['id']})...")
    
    # Get current price
    bbo = client.api_client.fetch_bbo(market)
    close_price = float(bbo['ask'])
    
    # Create close order
    close_order = Order(
        market=market,
        order_side=OrderSide.Sell,
        order_type=OrderType.Market,
        size=Decimal(str(pos['size']))
    )
    
    close_result = client.api_client.submit_order(close_order)
    close_order_id = close_result['id']
    
    # Wait for order to be processed
    time.sleep(1)
    
    # Feedback from Paradex
    close_status = client.api_client.fetch_order(close_order_id)
    
    # Calculate P&L
    pnl = (close_price - pos['open_price']) * pos['size']
    pnl_pct = ((close_price - pos['open_price']) / pos['open_price']) * 100
    
    print(f"  ✓ Close Order {close_order_id} | Status: {close_status['status']}")
    print(f"  Open: ${pos['open_price']:,.2f} → Close: ${close_price:,.2f}")
    print(f"  P&L: ${pnl:,.4f} ({pnl_pct:+.2f}%)\n")
    
    if i < 9:  # Don't delay after last close
        time.sleep(5)

# Final account check
print(f"{'='*80}")
print("Final Account Status:")
print(f"{'='*80}")

account = client.api_client.fetch_account_summary()
print(f"Account Value: ${float(account.account_value):,.2f}")

balances = client.api_client.fetch_balances()
if balances and len(balances) > 0:
    if isinstance(balances, list):
        usdc_balance = next((b for b in balances if b.get('asset') == 'USDC'), None)
        if usdc_balance:
            print(f"USDC Balance: ${float(usdc_balance['available_balance']):,.2f}")
    else:
        print(f"USDC Balance: ${float(balances.get('available_balance', 0)):,.2f}")

# Check positions
positions_data = client.api_client.fetch_positions()
open_positions = [p for p in positions_data['results'] if float(p['size']) != 0]
print(f"Open Positions: {len(open_positions)}")

print(f"\n✓ Full loop test complete!")
