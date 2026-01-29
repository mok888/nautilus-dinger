# nautilus_trader/adapters/paradex/data.py
"""LiveMarketDataClient implementation for Paradex."""

import asyncio
from typing import Any

from nautilus_trader.cache.cache import Cache
from nautilus_trader.common.component import LiveClock
from nautilus_trader.common.component import Logger
from nautilus_trader.common.component import MessageBus
from nautilus_trader.live.data_client import LiveMarketDataClient
from nautilus_trader.model.data import OrderBookDelta
from nautilus_trader.model.data import TradeTick
from nautilus_trader.model.enums import BookType
from nautilus_trader.model.identifiers import ClientId
from nautilus_trader.model.identifiers import InstrumentId

from nautilus_trader.adapters.paradex.config import ParadexDataClientConfig
from nautilus_trader.adapters.paradex.constants import PARADEX


class ParadexDataClient(LiveMarketDataClient):
    """Market data client for Paradex."""

    def __init__(
        self,
        http_client: Any,
        ws_client: Any,
        cache: Cache,
        clock: LiveClock,
        logger: Logger,
        msgbus: MessageBus,
        config: ParadexDataClientConfig,
    ) -> None:
        super().__init__(
            client_id=ClientId(PARADEX.value),
            venue=PARADEX,
            msgbus=msgbus,
            cache=cache,
            clock=clock,
            logger=logger,
        )
        self._http = http_client
        self._ws = ws_client
        self._config = config
        self._subscriptions: dict[InstrumentId, set[str]] = {}

    async def _connect(self) -> None:
        """Connect to WebSocket."""
        self._log.info("Connecting to Paradex WebSocket...")
        await self._ws.connect()
        self._log.info("Connected")

    async def _disconnect(self) -> None:
        """Disconnect from WebSocket."""
        await self._ws.disconnect()

    async def _subscribe_instruments(self) -> None:
        """Subscribe to instrument updates."""
        pass

    async def _unsubscribe_instruments(self) -> None:
        """Unsubscribe from instrument updates."""
        pass

    async def _subscribe_order_book_deltas(
        self,
        instrument_id: InstrumentId,
        book_type: BookType,
        depth: int | None = None,
        kwargs: dict | None = None,
    ) -> None:
        """Subscribe to order book deltas."""
        market = str(instrument_id.symbol)
        await self._ws.subscribe_orderbook(market)
        if instrument_id not in self._subscriptions:
            self._subscriptions[instrument_id] = set()
        self._subscriptions[instrument_id].add("orderbook")

    async def _unsubscribe_order_book_deltas(self, instrument_id: InstrumentId) -> None:
        """Unsubscribe from order book deltas."""
        market = str(instrument_id.symbol)
        await self._ws.unsubscribe_orderbook(market)

    async def _subscribe_trade_ticks(self, instrument_id: InstrumentId) -> None:
        """Subscribe to trade ticks."""
        market = str(instrument_id.symbol)
        await self._ws.subscribe_trades(market)
        if instrument_id not in self._subscriptions:
            self._subscriptions[instrument_id] = set()
        self._subscriptions[instrument_id].add("trades")

    async def _unsubscribe_trade_ticks(self, instrument_id: InstrumentId) -> None:
        """Unsubscribe from trade ticks."""
        market = str(instrument_id.symbol)
        await self._ws.unsubscribe_trades(market)
