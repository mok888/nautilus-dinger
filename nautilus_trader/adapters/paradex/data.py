# nautilus_trader/adapters/paradex/data.py
"""Data client for Paradex exchange."""

from typing import Any

from nautilus_trader.cache.cache import Cache
from nautilus_trader.common.component import LiveClock
from nautilus_trader.common.component import Logger
from nautilus_trader.common.component import MessageBus
from nautilus_trader.data.client import LiveDataClient
from nautilus_trader.data.messages import SubscribeTradeTicks
from nautilus_trader.data.messages import SubscribeQuoteTicks
from nautilus_trader.data.messages import SubscribeOrderBookDeltas
from nautilus_trader.data.messages import SubscribeOrderBookSnapshots
from nautilus_trader.data.messages import UnsubscribeTradeTicks
from nautilus_trader.data.messages import UnsubscribeQuoteTicks
# Bug #002: Add missing imports
from nautilus_trader.data.messages import SubscribeBars
from nautilus_trader.data.messages import SubscribeMarkPrices
from nautilus_trader.data.messages import SubscribeIndexPrices
from nautilus_trader.data.messages import SubscribeFundingRates
from nautilus_trader.data.messages import SubscribeInstrumentStatus
from nautilus_trader.data.messages import SubscribeInstrumentClose
from nautilus_trader.data.messages import SubscribeOpenInterest
from nautilus_trader.data.messages import SubscribeLiquidations
from nautilus_trader.data.messages import UnsubscribeBars
from nautilus_trader.data.messages import UnsubscribeMarkPrices
from nautilus_trader.data.messages import UnsubscribeIndexPrices
from nautilus_trader.data.messages import UnsubscribeFundingRates
from nautilus_trader.data.messages import UnsubscribeInstrumentStatus
from nautilus_trader.data.messages import UnsubscribeInstrumentClose
from nautilus_trader.data.messages import UnsubscribeOpenInterest
from nautilus_trader.data.messages import UnsubscribeLiquidations
from nautilus_trader.data.messages import UnsubscribeOrderBook
from nautilus_trader.data.messages import UnsubscribeOrderBookSnapshots
from nautilus_trader.data.messages import RequestBars
from nautilus_trader.data.messages import RequestQuoteTicks
from nautilus_trader.data.messages import RequestTradeTicks
from nautilus_trader.data.messages import RequestInstrument
from nautilus_trader.data.messages import RequestInstruments
from nautilus_trader.data.messages import RequestOrderBookSnapshot
from nautilus_trader.data.messages import RequestData
from nautilus_trader.data.enums import DataType
from nautilus_trader.core.uuid import UUID4


class ParadexDataClient(LiveDataClient):
    """
    Data client for Paradex exchange.

    Implements data subscriptions and requests via WebSocket/REST.
    """

    def __init__(
        self,
        ws_client: Any,
        instrument_provider: Any,
        cache: Cache,
        clock: LiveClock,
        logger: Logger,
        msgbus: MessageBus,
        config: Any,
    ) -> None:
        super().__init__(
            client_id=None,  # Will be set in parent
            venue=None,  # Will be set in parent
            instrument_provider=instrument_provider,
            msgbus=msgbus,
            cache=cache,
            clock=clock,
            logger=logger,
        )
        self._ws = ws_client
        self._config = config

    async def _connect(self) -> None:
        """Connect to WebSocket."""
        self._log.info("Connecting to Paradex data feed...")
        await self._ws.connect()
        self._log.info("Connected")

    async def _disconnect(self) -> None:
        """Disconnect from WebSocket."""
        self._log.info("Disconnecting from Paradex data feed...")
        await self._ws.disconnect()

    # -------------------------------------------------------------------------
    # SUBSCRIPTION METHODS (Bug #001 - Fixed: Now accept command objects)
    # -------------------------------------------------------------------------

    async def _subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
        """
        Subscribe to trade ticks.

        CORRECTED: Now accepts SubscribeTradeTicks command object instead of raw instrument_id.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Subscribing to trade ticks for {instrument_id}...")
        # TODO: Implement WebSocket subscription
        # await self._ws.subscribe_trades(instrument_id)

    async def _subscribe_quote_ticks(self, command: SubscribeQuoteTicks) -> None:
        """
        Subscribe to quote ticks.

        CORRECTED: Now accepts SubscribeQuoteTicks command object instead of raw instrument_id.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Subscribing to quote ticks for {instrument_id}...")
        # TODO: Implement WebSocket subscription
        # await self._ws.subscribe_quotes(instrument_id)

    async def _subscribe_order_book_deltas(self, command: SubscribeOrderBookDeltas) -> None:
        """
        Subscribe to order book deltas.

        CORRECTED: Now accepts SubscribeOrderBookDeltas command object.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Subscribing to order book deltas for {instrument_id}...")
        # TODO: Implement WebSocket subscription
        # await self._ws.subscribe_order_book_deltas(instrument_id, book_type=command.book_type)

    async def _subscribe_order_book_snapshots(self, command: SubscribeOrderBookSnapshots) -> None:
        """
        Subscribe to order book snapshots.

        CORRECTED: Now accepts SubscribeOrderBookSnapshots command object.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Subscribing to order book snapshots for {instrument_id}...")
        # TODO: Implement WebSocket subscription
        # await self._ws.subscribe_order_book_snapshots(instrument_id)

    # -------------------------------------------------------------------------
    # UNSUBSCRIPTION METHODS (Bug #001 - Fixed: Now accept command objects)
    # -------------------------------------------------------------------------

    async def _unsubscribe_trade_ticks(self, command: UnsubscribeTradeTicks) -> None:
        """
        Unsubscribe from trade ticks.

        CORRECTED: Now accepts UnsubscribeTradeTicks command object instead of raw instrument_id.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Unsubscribing from trade ticks for {instrument_id}...")
        # TODO: Implement WebSocket unsubscription
        # await self._ws.unsubscribe_trades(instrument_id)

    async def _unsubscribe_quote_ticks(self, command: UnsubscribeQuoteTicks) -> None:
        """
        Unsubscribe from quote ticks.
        
        CORRECTED: Now accepts UnsubscribeQuoteTicks command object instead of raw instrument_id.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Unsubscribing from quote ticks for {instrument_id}...")
        # TODO: Implement WebSocket unsubscription
        # await self._ws.unsubscribe_quotes(instrument_id)

    # -------------------------------------------------------------------------
    # BASE METHODS (Bug #002 - Missing: 3 methods)
    # -------------------------------------------------------------------------

    async def _subscribe(self, data_type: DataType) -> None:
        """
        Subscribe to data type (base method).
        
        Bug #002: Missing base method.
        Routes to specific subscription methods based on data type.
        """
        self._log.info(f"Subscribing to data type: {data_type}")
        # TODO: Route to specific subscription methods
        # Example:
        # if data_type == DataType.BAR:
        #     await self._subscribe_bars(...)
        pass

    async def _unsubscribe(self, data_type: DataType) -> None:
        """
        Unsubscribe from data type (base method).
        
        Bug #002: Missing base method.
        Routes to specific unsubscription methods based on data type.
        """
        self._log.info(f"Unsubscribing from data type: {data_type}")
        # TODO: Route to specific unsubscription methods
        pass

    async def _request(self, data_type: DataType, correlation_id: UUID4) -> None:
        """
        Request data (base method).
        
        Bug #002: Missing base method.
        Routes to specific request methods based on data type.
        """
        self._log.info(f"Requesting data type: {data_type}, correlation_id: {correlation_id}")
        # TODO: Route to specific request methods
        pass

    # -------------------------------------------------------------------------
    # ADDITIONAL SUBSCRIPTION METHODS (Bug #002 - Missing: 8 methods)
    # -------------------------------------------------------------------------

    async def _subscribe_bars(self, command: SubscribeBars) -> None:
        """
        Subscribe to OHLCV bars.
        
        Bug #002: Missing subscription method.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Subscribing to bars for {instrument_id}...")
        # TODO: Implement WebSocket subscription
        # await self._ws.subscribe_bars(instrument_id, bar_type=command.bar_type)

    async def _subscribe_mark_price(self, command: SubscribeMarkPrices) -> None:
        """
        Subscribe to mark prices (mark-to-market).
        
        Bug #002: Missing subscription method.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Subscribing to mark prices for {instrument_id}...")
        # TODO: Implement WebSocket subscription

    async def _subscribe_funding_rate(self, command: SubscribeFundingRates) -> None:
        """
        Subscribe to funding rates.
        
        Bug #002: Missing subscription method.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Subscribing to funding rates for {instrument_id}...")
        # TODO: Implement WebSocket subscription

    async def _subscribe_index_price(self, command: SubscribeIndexPrices) -> None:
        """
        Subscribe to index prices.
        
        Bug #002: Missing subscription method.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Subscribing to index prices for {instrument_id}...")
        # TODO: Implement WebSocket subscription

    async def _subscribe_instrument_status(self, command: SubscribeInstrumentStatus) -> None:
        """
        Subscribe to instrument status updates.
        
        Bug #002: Missing subscription method.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Subscribing to instrument status for {instrument_id}...")
        # TODO: Implement WebSocket subscription

    async def _subscribe_instrument_close(self, command: SubscribeInstrumentClose) -> None:
        """
        Subscribe to instrument close updates.
        
        Bug #002: Missing subscription method.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Subscribing to instrument close for {instrument_id}...")
        # TODO: Implement WebSocket subscription

    async def _subscribe_open_interest(self, command: SubscribeOpenInterest) -> None:
        """
        Subscribe to open interest updates.
        
        Bug #002: Missing subscription method.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Subscribing to open interest for {instrument_id}...")
        # TODO: Implement WebSocket subscription

    async def _subscribe_liquidations(self, command: SubscribeLiquidations) -> None:
        """
        Subscribe to liquidation events.
        
        Bug #002: Missing subscription method.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Subscribing to liquidations for {instrument_id}...")
        # TODO: Implement WebSocket subscription

    # -------------------------------------------------------------------------
    # ADDITIONAL UNSUBSCRIPTION METHODS (Bug #002 - Missing: 10 methods)
    # -------------------------------------------------------------------------

    async def _unsubscribe_bars(self, command: UnsubscribeBars) -> None:
        """
        Unsubscribe from OHLCV bars.
        
        Bug #002: Missing unsubscription method.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Unsubscribing from bars for {instrument_id}...")
        # TODO: Implement WebSocket unsubscription

    async def _unsubscribe_mark_price(self, command: UnsubscribeMarkPrices) -> None:
        """
        Unsubscribe from mark prices.
        
        Bug #002: Missing unsubscription method.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Unsubscribing from mark prices for {instrument_id}...")
        # TODO: Implement WebSocket unsubscription

    async def _unsubscribe_funding_rate(self, command: UnsubscribeFundingRates) -> None:
        """
        Unsubscribe from funding rates.
        
        Bug #002: Missing unsubscription method.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Unsubscribing from funding rates for {instrument_id}...")
        # TODO: Implement WebSocket unsubscription

    async def _unsubscribe_index_price(self, command: UnsubscribeIndexPrices) -> None:
        """
        Unsubscribe from index prices.
        
        Bug #002: Missing unsubscription method.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Unsubscribing from index prices for {instrument_id}...")
        # TODO: Implement WebSocket unsubscription

    async def _unsubscribe_instrument_status(self, command: UnsubscribeInstrumentStatus) -> None:
        """
        Unsubscribe from instrument status updates.
        
        Bug #002: Missing unsubscription method.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Unsubscribing from instrument status for {instrument_id}...")
        # TODO: Implement WebSocket unsubscription

    async def _unsubscribe_instrument_close(self, command: UnsubscribeInstrumentClose) -> None:
        """
        Unsubscribe from instrument close updates.
        
        Bug #002: Missing unsubscription method.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Unsubscribing from instrument close for {instrument_id}...")
        # TODO: Implement WebSocket unsubscription

    async def _unsubscribe_open_interest(self, command: UnsubscribeOpenInterest) -> None:
        """
        Unsubscribe from open interest updates.
        
        Bug #002: Missing unsubscription method.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Unsubscribing from open interest for {instrument_id}...")
        # TODO: Implement WebSocket unsubscription

    async def _unsubscribe_liquidations(self, command: UnsubscribeLiquidations) -> None:
        """
        Unsubscribe from liquidation events.
        
        Bug #002: Missing unsubscription method.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Unsubscribing from liquidations for {instrument_id}...")
        # TODO: Implement WebSocket unsubscription

    async def _unsubscribe_order_book_deltas(self, command: UnsubscribeOrderBook) -> None:
        """
        Unsubscribe from order book deltas.
        
        Bug #002: Missing unsubscription method.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Unsubscribing from order book deltas for {instrument_id}...")
        # TODO: Implement WebSocket unsubscription

    async def _unsubscribe_order_book_snapshots(self, command: UnsubscribeOrderBookSnapshots) -> None:
        """
        Unsubscribe from order book snapshots.
        
        Bug #002: Missing unsubscription method.
        """
        instrument_id = command.instrument_id
        self._log.info(f"Unsubscribing from order book snapshots for {instrument_id}...")
        # TODO: Implement WebSocket unsubscription

    # -------------------------------------------------------------------------
    # REQUEST METHODS (Bug #002 - Missing: 7 methods)
    # -------------------------------------------------------------------------

    async def _request_quote_ticks(self, request: RequestQuoteTicks) -> None:
        """
        Request historical quote ticks.
        
        Bug #002: Missing request method.
        """
        instrument_id = request.instrument_id
        self._log.debug(f"Requesting quote ticks for {instrument_id}...")
        # TODO: Implement REST request
        # await self._http.get_quote_ticks(instrument_id, start=request.start, end=request.end)

    async def _request_trade_ticks(self, request: RequestTradeTicks) -> None:
        """
        Request historical trade ticks.
        
        Bug #002: Missing request method.
        """
        instrument_id = request.instrument_id
        self._log.debug(f"Requesting trade ticks for {instrument_id}...")
        # TODO: Implement REST request
        # await self._http.get_trade_ticks(instrument_id, start=request.start, end=request.end)

    async def _request_bars(self, request: RequestBars) -> None:
        """
        Request historical OHLCV bars.
        
        Bug #002: Missing request method.
        """
        instrument_id = request.instrument_id
        self._log.debug(f"Requesting bars for {instrument_id}...")
        # TODO: Implement REST request
        # await self._http.get_bars(instrument_id, bar_type=request.bar_type, start=request.start, end=request.end)

    async def _request_instrument(self, request: RequestInstrument) -> None:
        """
        Request instrument information.
        
        Bug #002: Missing request method.
        """
        instrument_id = request.instrument_id
        self._log.debug(f"Requesting instrument info for {instrument_id}...")
        # TODO: Implement REST request or cache lookup
        # instrument = self._instrument_provider.find(instrument_id)

    async def _request_instruments(self, request: RequestInstruments) -> None:
        """
        Request all instruments for venue.
        
        Bug #002: Missing request method.
        """
        venue = request.venue
        self._log.debug(f"Requesting instruments for venue {venue}...")
        # TODO: Implement REST request or cache lookup
        # instruments = self._instrument_provider.list_all()

    async def _request_order_book_snapshot(self, request: RequestOrderBookSnapshot) -> None:
        """
        Request current order book snapshot.
        
        Bug #002: Missing request method.
        """
        instrument_id = request.instrument_id
        self._log.debug(f"Requesting order book snapshot for {instrument_id}...")
        # TODO: Implement REST request
        # await self._http.get_order_book(instrument_id, depth=request.depth)

    async def _request_data(self, request: RequestData) -> None:
        """
        Generic data request method.
        
        Bug #002: Missing request method.
        Routes to specific request methods based on data type.
        """
        data_type = request.data_type
        self._log.debug(f"Requesting data: {data_type}")
        # TODO: Route to specific request methods
        pass

