#!/usr/bin/env python3
"""
Minimal Nautilus Trader strategy with Paradex adapter
Places a single BTC order and monitors feedback
"""
import os
import sys
from decimal import Decimal
from dotenv import load_dotenv

sys.path.insert(0, '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages')
os.environ['PYTHONPATH'] = '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages'

load_dotenv(".env.testnet")

from nautilus_trader.config import TradingNodeConfig
from nautilus_trader.live.node import TradingNode
from nautilus_trader.model.identifiers import InstrumentId, Venue
from nautilus_trader.model.enums import OrderSide, TimeInForce
from nautilus_trader.model.objects import Price, Quantity
from nautilus_trader.trading.strategy import Strategy

from paradex_py import ParadexSubkey


class SimpleParadexStrategy(Strategy):
    """Minimal strategy that places one order"""
    
    def __init__(self, config=None):
        super().__init__(config)
        self.instrument_id = InstrumentId.from_str("BTC-USD-PERP.PARADEX")
        self.order_placed = False
        
    def on_start(self):
        self.log.info("Strategy starting...")
        # Subscribe to orderbook
        self.subscribe_order_book_deltas(self.instrument_id)
        self.subscribe_quote_ticks(self.instrument_id)
        
    def on_order_book_deltas(self, deltas):
        """Triggered when orderbook updates"""
        if self.order_placed:
            return
            
        # Get best ask
        orderbook = self.cache.order_book(self.instrument_id)
        if not orderbook or not orderbook.best_ask_price():
            return
            
        best_ask = float(orderbook.best_ask_price())
        self.log.info(f"Best ask: ${best_ask}")
        
        # Place buy order at -5bps
        entry_price = best_ask * 0.9995
        entry_price = round(entry_price / 0.1) * 0.1  # Round to 0.1
        
        self.log.info(f"Placing BUY order at ${entry_price}")
        
        order = self.order_factory.limit(
            instrument_id=self.instrument_id,
            order_side=OrderSide.BUY,
            quantity=Quantity.from_str("0.001"),
            price=Price.from_str(str(entry_price)),
            time_in_force=TimeInForce.GTC,
        )
        
        self.submit_order(order)
        self.order_placed = True
        
    def on_order_accepted(self, event):
        self.log.info(f"✅ Order ACCEPTED: {event.client_order_id}")
        
    def on_order_rejected(self, event):
        self.log.error(f"❌ Order REJECTED: {event.reason}")
        
    def on_order_filled(self, event):
        self.log.info(f"✅ Order FILLED: {event.last_qty} @ {event.last_px}")
        
    def on_stop(self):
        self.log.info("Strategy stopping...")


async def main():
    # Create Paradex client for data
    paradex = ParadexSubkey(
        env="testnet",
        l2_private_key=os.getenv("PARADEX_SUBKEY_PRIVATE_KEY"),
        l2_address=os.getenv("PARADEX_L2_ADDRESS")
    )
    
    # Nautilus config
    config = TradingNodeConfig(
        trader_id="TESTER-001",
        log_level="INFO",
        data_clients={
            "PARADEX": {
                "api_key": os.getenv("PARADEX_SUBKEY_PRIVATE_KEY"),
                "api_secret": os.getenv("PARADEX_L2_ADDRESS"),
            }
        },
        exec_clients={
            "PARADEX": {
                "api_key": os.getenv("PARADEX_SUBKEY_PRIVATE_KEY"),
                "api_secret": os.getenv("PARADEX_L2_ADDRESS"),
            }
        },
        strategies=[
            {
                "strategy_path": "nautilus_paradex_strategy:SimpleParadexStrategy",
                "config": {},
            }
        ],
    )
    
    # Create and run node
    node = TradingNode(config=config)
    
    try:
        node.start()
        await node.run_async()
    finally:
        node.stop()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
