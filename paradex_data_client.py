"""
Paradex Data Client for Nautilus Trader
"""
import asyncio
from decimal import Decimal
from paradex_py import ParadexSubkey
from nautilus_trader.adapters.env import get_env_key
from nautilus_trader.common.component import LiveClock, MessageBus
from nautilus_trader.live.data_client import LiveMarketDataClient
from nautilus_trader.model.identifiers import ClientId, InstrumentId, Venue
from nautilus_trader.model.instruments import CryptoPerpetual
from nautilus_trader.model.data import OrderBookDelta, QuoteTick
from nautilus_trader.model.objects import Price, Quantity
from nautilus_trader.model.enums import BookAction, OrderSide, AggressorSide
from nautilus_trader.core.datetime import millis_to_nanos


class ParadexDataClient(LiveMarketDataClient):
    """Paradex market data client"""
    
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        client: ParadexSubkey,
        msgbus: MessageBus,
        cache,
        clock: LiveClock,
    ):
        super().__init__(
            loop=loop,
            client_id=ClientId("PARADEX"),
            venue=Venue("PARADEX"),
            msgbus=msgbus,
            cache=cache,
            clock=clock,
        )
        self._client = client
        self._update_task = None
        
    async def _connect(self):
        self._log.info("Connecting to Paradex...")
        # Load instruments
        markets = self._client.api_client.fetch_markets()
        for market in markets.get("results", []):
            instrument = self._parse_instrument(market)
            self._handle_data(instrument)
        self._log.info(f"Loaded {len(markets.get('results', []))} instruments")
        
    async def _disconnect(self):
        self._log.info("Disconnecting from Paradex...")
        if self._update_task:
            self._update_task.cancel()
            
    def _parse_instrument(self, market: dict) -> CryptoPerpetual:
        """Parse market data into Nautilus instrument"""
        symbol = market["symbol"]
        instrument_id = InstrumentId.from_str(f"{symbol}.PARADEX")
        
        return CryptoPerpetual(
            instrument_id=instrument_id,
            raw_symbol=symbol,
            base_currency=symbol.split("-")[0],
            quote_currency="USD",
            settlement_currency="USDC",
            is_inverse=False,
            price_precision=1,
            size_precision=3,
            price_increment=Price.from_str("0.1"),
            size_increment=Quantity.from_str("0.001"),
            max_quantity=Quantity.from_str("1000"),
            min_quantity=Quantity.from_str("0.001"),
            max_price=Price.from_str("1000000"),
            min_price=Price.from_str("0.1"),
            margin_init=Decimal("0.1"),
            margin_maint=Decimal("0.05"),
            maker_fee=Decimal("0.0002"),
            taker_fee=Decimal("0.0005"),
            ts_event=self._clock.timestamp_ns(),
            ts_init=self._clock.timestamp_ns(),
        )
        
    async def _subscribe_order_book_deltas(self, instrument_id: InstrumentId):
        """Subscribe to orderbook updates"""
        self._log.info(f"Subscribing to orderbook: {instrument_id}")
        
        # Start polling task
        if not self._update_task:
            self._update_task = self._loop.create_task(self._poll_orderbook(instrument_id))
            
    async def _poll_orderbook(self, instrument_id: InstrumentId):
        """Poll orderbook updates"""
        symbol = instrument_id.symbol.value.replace(".PARADEX", "")
        
        while True:
            try:
                orderbook = self._client.api_client.fetch_orderbook(symbol)
                
                # Send deltas
                ts_event = self._clock.timestamp_ns()
                
                # Process bids
                for bid in orderbook.get("bids", [])[:5]:
                    delta = OrderBookDelta(
                        instrument_id=instrument_id,
                        action=BookAction.UPDATE,
                        order=None,  # Simplified
                        ts_event=ts_event,
                        ts_init=ts_event,
                    )
                    self._handle_data(delta)
                    
                # Process asks
                for ask in orderbook.get("asks", [])[:5]:
                    delta = OrderBookDelta(
                        instrument_id=instrument_id,
                        action=BookAction.UPDATE,
                        order=None,  # Simplified
                        ts_event=ts_event,
                        ts_init=ts_event,
                    )
                    self._handle_data(delta)
                    
                await asyncio.sleep(1)  # Poll every second
                
            except Exception as e:
                self._log.error(f"Error polling orderbook: {e}")
                await asyncio.sleep(5)
