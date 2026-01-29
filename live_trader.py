#!/usr/bin/env python3
"""Live trading with 10x leverage, 0.1% SL/TP, live P&L updates"""

import asyncio
import time
import sys
from datetime import datetime
from paradex_py import ParadexSubkey
from paradex_py.common.order import Order, OrderSide, OrderType
from decimal import Decimal
import os
from dotenv import load_dotenv

class LiveTrader:
    def __init__(self, client):
        self.client = client
        self.position = None
        self.entry_price = None
        self.sl_price = None
        self.tp_price = None
        self.position_size = None
        self.start_time = None
        
    def display_status(self, current_price=None, status="MONITORING"):
        sys.stdout.write('\033[2J\033[H')
        
        elapsed = int(time.time() - self.start_time) if self.start_time else 0
        
        print("="*80)
        print(f"🔴 LIVE TRADING - NAUTILUS TRADER (10x Leverage)")
        print("="*80)
        print(f"Status: {status} | Time: {datetime.now().strftime('%H:%M:%S')} | Elapsed: {elapsed}s")
        print("-"*80)
        
        if self.position and current_price:
            pnl_pct = ((current_price - self.entry_price) / self.entry_price) * 100
            pnl_usd = (current_price - self.entry_price) * float(self.position_size)
            pnl_10x = pnl_usd * 10  # 10x leverage effect
            
            # Distance to SL/TP
            dist_sl = ((current_price - self.sl_price) / self.entry_price) * 100
            dist_tp = ((self.tp_price - current_price) / self.entry_price) * 100
            
            print(f"Position: {self.position['id'][:30]}...")
            print(f"Size: {self.position_size} BTC")
            print("-"*80)
            print(f"Entry Price:   ${self.entry_price:,.2f}")
            print(f"Current Price: ${current_price:,.2f}")
            print(f"Stop Loss:     ${self.sl_price:,.2f} (distance: {dist_sl:+.3f}%)")
            print(f"Take Profit:   ${self.tp_price:,.2f} (distance: {dist_tp:+.3f}%)")
            print("="*80)
            
            # BIG P&L DISPLAY
            pnl_color = "🟢" if pnl_pct > 0 else "🔴" if pnl_pct < 0 else "⚪"
            print(f"{pnl_color} P&L (1x):  ${pnl_usd:+,.4f} ({pnl_pct:+.3f}%)")
            print(f"{pnl_color} P&L (10x): ${pnl_10x:+,.4f} ({pnl_pct*10:+.3f}%)")
            
            # Progress bar to SL/TP
            if pnl_pct > 0:
                progress = int((pnl_pct / 0.1) * 20)
                bar = "█" * min(progress, 20) + "░" * (20 - min(progress, 20))
                print(f"\n📈 TO TP: [{bar}] {(pnl_pct/0.1)*100:.0f}%")
            else:
                progress = int((abs(pnl_pct) / 0.1) * 20)
                bar = "█" * min(progress, 20) + "░" * (20 - min(progress, 20))
                print(f"\n📉 TO SL: [{bar}] {(abs(pnl_pct)/0.1)*100:.0f}%")
                
        print("="*80)
        sys.stdout.flush()
    
    async def enter_position(self, market="BTC-USD-PERP", size=0.01):
        """Enter market position"""
        print("Entering position...")
        
        bbo = self.client.api_client.fetch_bbo(market)
        self.entry_price = float(bbo['bid'])
        self.position_size = size
        self.start_time = time.time()
        
        # 0.1% SL/TP
        self.sl_price = self.entry_price * 0.999
        self.tp_price = self.entry_price * 1.001
        
        order = Order(
            market=market,
            order_side=OrderSide.Buy,
            order_type=OrderType.Market,
            size=Decimal(str(size))
        )
        
        result = self.client.api_client.submit_order(order)
        self.position = result
        
        time.sleep(1)
        
        bbo = self.client.api_client.fetch_bbo(market)
        self.display_status(float(bbo['bid']), "POSITION OPEN")
        
        return result
    
    async def monitor_position(self):
        """Monitor with live P&L updates every 0.5s"""
        while True:
            try:
                bbo = self.client.api_client.fetch_bbo("BTC-USD-PERP")
                current_price = float(bbo['bid'])
                
                # Check stop loss
                if current_price <= self.sl_price:
                    self.display_status(current_price, "🛑 STOP LOSS HIT")
                    await asyncio.sleep(2)
                    await self.close_position(current_price, "STOP LOSS")
                    break
                
                # Check take profit
                if current_price >= self.tp_price:
                    self.display_status(current_price, "✅ TAKE PROFIT HIT")
                    await asyncio.sleep(2)
                    await self.close_position(current_price, "TAKE PROFIT")
                    break
                
                self.display_status(current_price, "🔴 LIVE MONITORING")
                await asyncio.sleep(0.5)  # Update twice per second
                
            except Exception as e:
                print(f"\nError: {e}")
                await asyncio.sleep(1)
    
    async def close_position(self, current_price, reason):
        """Close position"""
        order = Order(
            market="BTC-USD-PERP",
            order_side=OrderSide.Sell,
            order_type=OrderType.Market,
            size=Decimal(str(self.position_size))
        )
        
        result = self.client.api_client.submit_order(order)
        
        time.sleep(1)
        
        bbo = self.client.api_client.fetch_bbo("BTC-USD-PERP")
        exit_price = float(bbo['ask'])
        
        pnl = (exit_price - self.entry_price) * float(self.position_size)
        pnl_pct = ((exit_price - self.entry_price) / self.entry_price) * 100
        pnl_10x = pnl * 10
        
        elapsed = int(time.time() - self.start_time)
        
        print(f"\n{'='*80}")
        print(f"POSITION CLOSED - {reason}")
        print(f"{'='*80}")
        print(f"Duration: {elapsed}s")
        print(f"Entry:  ${self.entry_price:,.2f}")
        print(f"Exit:   ${exit_price:,.2f}")
        print(f"P&L (1x):  ${pnl:+,.4f} ({pnl_pct:+.3f}%)")
        print(f"P&L (10x): ${pnl_10x:+,.4f} ({pnl_pct*10:+.3f}%)")
        print(f"Close Order: {result['id']}")
        print(f"{'='*80}")

async def main():
    load_dotenv('.env.testnet')
    
    client = ParadexSubkey(
        env='testnet',
        l2_private_key=os.getenv('PARADEX_SUBKEY_PRIVATE_KEY'),
        l2_address=os.getenv('PARADEX_L2_ADDRESS'),
    )
    
    trader = LiveTrader(client)
    
    print("\n" + "="*80)
    print("NAUTILUS TRADER - LIVE TRADING")
    print("="*80)
    print("  Leverage: 10x")
    print("  Stop Loss: -0.1%")
    print("  Take Profit: +0.1%")
    print("  Size: 0.01 BTC")
    print("="*80 + "\n")
    
    # Enter position immediately
    await trader.enter_position(size=0.01)
    
    # Monitor until closed
    await trader.monitor_position()
    
    print("\n✓ Session complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted")
