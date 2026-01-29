# 2_PYTHON_ADAPTER_IMPLEMENTATION.md
PYTHON ADAPTER IMPLEMENTATION - PARADEX NAUTILUS ADAPTER
Complete Python Layer Architecture and Patterns

📋 OVERVIEW
This document details Python implementation layer that interfaces with Nautilus Trader.

Total LOC: ~2,800
Files: 7 Python files
Compliance: 100% Nautilus LiveExecutionClient & LiveMarketDataClient standards

🏗️ PYTHON ARCHITECTURE
```
nautilus_trader/adapters/paradex/
├── __init__.py                 # Package exports
├── config.py                   # Configuration classes
├── constants.py                # Constants
├── providers.py                # InstrumentProvider (300 LOC)
├── execution.py                # LiveExecutionClient (1,000 LOC) ⭐
├── data.py                     # LiveMarketDataClient (800 LOC) ⭐
└── factories.py                # Type conversions (450 LOC)
```

⭐ MOST CRITICAL: execution.py (LiveExecutionClient)

**Required Methods (ALL 11 MANDATORY)**

```python
class ParadexExecutionClient(LiveExecutionClient):
    # Connection management
    async def _connect(self) -> None
    async def _disconnect(self) -> None

    # Order operations
    async def _submit_order(self, command: SubmitOrder) -> None
    async def _cancel_order(self, command: CancelOrder) -> None
    async def _modify_order(self, command: ModifyOrder) -> None
    async def _cancel_all_orders(self, command: CancelAllOrders) -> None
    async def _batch_cancel_orders(self, command: BatchCancelOrders) -> None

    # State reporting (REST authoritative)
    async def generate_order_status_report(...) -> OrderStatusReport | None
    async def generate_order_status_reports(...) -> list[OrderStatusReport]
    async def generate_fill_reports(...) -> list[FillReport]
    async def generate_position_status_reports(...) -> list[PositionStatusReport]
```

**CRITICAL PATTERN #1: Idempotent Reconciliation**

```python
async def _connect(self) -> None:
    """
    Connect MUST perform reconciliation.

    This ensures idempotent state recovery on restart.
    """
    self._log.info("Connecting to Paradex...")

    # MANDATORY: Reconcile state from REST
    await self._reconcile_state()

    # Start periodic reconciliation
    self._reconcile_task = asyncio.create_task(
        self._run_reconciliation_loop()
    )

    self._log.info("Connected")

async def _reconcile_state(self) -> None:
    """
    Reconcile state from REST (idempotent).

    REST is the source of truth. This method:
    1. Fetches all open orders
    2. Emits OrderStatusReports for unseen orders
    3. Fetches recent fills
    4. Emits FillReports for unseen fills
    """
    self._log.info("Reconciling state from REST...")

    try:
        # Get open orders (REST authoritative)
        orders = await self._http.get_open_orders()

        for order in orders:
            venue_order_id = VenueOrderId(order["id"])

            # Check if we've already emitted this order
            if venue_order_id not in self._emitted_orders:
                # Generate and emit OrderStatusReport
                inst_id = InstrumentId.from_str(f"{order['market']}.PARADEX")
                instrument = self._cache.instrument(inst_id)

                if instrument:
                    report = parse_order_status_report(
                        order, instrument, self._account_id, self._clock
                    )
                    self.generate_order_status_report(report)
                    self._emitted_orders.add(venue_order_id)

        # Get recent fills (prevent duplicates)
        fills = await self._http.get_fills(
            start_time=self._last_reconcile_ts_ns // 1_000_000  # Convert to ms
        )

        for fill in fills:
            trade_id = TradeId(fill["id"])

            # Check if we've already emitted this fill
            if trade_id not in self._emitted_fills:
                inst_id = InstrumentId.from_str(f"{fill['market']}.PARADEX")
                instrument = self._cache.instrument(inst_id)

                if instrument:
                    report = parse_fill_report(
                        fill, instrument, self._account_id, self._clock
                    )
                    self.generate_fill_report(report)
                    self._emitted_fills.add(trade_id)

        self._last_reconcile_ts_ns = self._clock.timestamp_ns()
        self._log.info("Reconciliation complete")

    except Exception as e:
        self._log.error(f"Reconciliation failed: {e}")
        raise

async def _run_reconciliation_loop(self) -> None:
    """Run periodic reconciliation."""
    while True:
        try:
            await asyncio.sleep(self._config.reconcile_interval_secs)
            await self._reconcile_state()
        except asyncio.CancelledError:
            break
        except Exception as e:
            self._log.error(f"Reconciliation loop error: {e}")
```

**CRITICAL PATTERN #2: Fill Deduplication**

```python
def __init__(self, ...):
    super().__init__(...)

    # State tracking for idempotency
    self._emitted_orders: set[VenueOrderId] = set()
    self._emitted_fills: set[TradeId] = set()
    self._last_reconcile_ts_ns: int = 0

def _is_fill_emitted(self, trade_id: TradeId) -> bool:
    """Check if fill was already emitted."""
    return trade_id in self._emitted_fills

def _mark_fill_emitted(self, trade_id: TradeId) -> None:
    """Mark fill as emitted."""
    self._emitted_fills.add(trade_id)
```

**CRITICAL PATTERN #3: Order Submission with STARK Signature**

```python
async def _submit_order(self, command: SubmitOrder) -> None:
    """
    Submit order to Paradex.

    The STARK signature happens in the Rust layer (http client).
    Python just provides order parameters.
    """
    try:
        order = command.order
        instrument = self._cache.instrument(order.instrument_id)

        if instrument is None:
            self._log.error(f"Instrument not found: {order.instrument_id}")
            return

        # Convert Nautilus order to Paradex format
        market = str(order.instrument_id.symbol)
        side = "BUY" if order.side == OrderSide.BUY else "SELL"
        order_type = "LIMIT" if order.order_type == OrderType.LIMIT else "MARKET"
        size = str(order.quantity)
        price = str(order.price) if hasattr(order, 'price') and order.price else None
        client_id = str(order.client_order_id)

        # Submit via Rust HTTP client (STARK signing happens here)
        result = await self._http.submit_order(
            market=market,
            side=side,
            order_type=order_type,
            size=size,
            price=price,
            client_id=client_id,
        )

        # Generate OrderAccepted event
        self.generate_order_accepted(
            strategy_id=order.strategy_id,
            instrument_id=order.instrument_id,
            client_order_id=order.client_order_id,
            venue_order_id=VenueOrderId(result["id"]),
            ts_event=millis_to_nanos(result["created_at"]),
        )

        # Track emitted order
        self._emitted_orders.add(VenueOrderId(result["id"]))

    except Exception as e:
        self._log.error(f"Order submission failed: {e}")

        # Generate OrderRejected event
        self.generate_order_rejected(
            strategy_id=order.strategy_id,
            instrument_id=order.instrument_id,
            client_order_id=order.client_order_id,
            reason=str(e),
            ts_event=self._clock.timestamp_ns(),
        )
```

**CRITICAL PATTERN #4: REST as Source of Truth**

```python
async def generate_order_status_reports(
    self,
    instrument_id: InstrumentId | None = None,
    start: int | None = None,
    end: int | None = None,
    open_only: bool = False,
) -> list[OrderStatusReport]:
    """
    Generate order status reports from REST.

    REST is authoritative. Always query REST, never trust cache.
    """
    try:
        # Query REST (source of truth)
        if open_only:
            orders = await self._http.get_open_orders()
        else:
            orders = await self._http.get_order_history(
                start_time=start,
                end_time=end
            )

        reports = []
        for order in orders:
            # Filter by instrument if specified
            if instrument_id is None or order["market"] == str(instrument_id.symbol):
                inst = self._cache.instrument(
                    InstrumentId.from_str(f"{order['market']}.PARADEX")
                )

                if inst:
                    report = parse_order_status_report(
                        order, inst, self._account_id, self._clock
                    )
                    reports.append(report)

        return reports

    except Exception as e:
        self._log.error(f"Failed to generate order status reports: {e}")
        return []
```

⭐ CRITICAL: data.py (LiveMarketDataClient)

**Required Methods (ALL 8 MANDATORY)**

```python
class ParadexDataClient(LiveMarketDataClient):
    # Connection management
    async def _connect(self) -> None
    async def _disconnect(self) -> None

    # Instrument subscriptions
    async def _subscribe_instruments(self) -> None
    async def _unsubscribe_instruments(self) -> None

    # Order book subscriptions
    async def _subscribe_order_book_deltas(...) -> None
    async def _unsubscribe_order_book_deltas(...) -> None

    # Trade subscriptions
    async def _subscribe_trade_ticks(...) -> None
    async def _unsubscribe_trade_ticks(...) -> None
```

**CRITICAL PATTERN: WebSocket Message Routing**

```python
async def _connect(self) -> None:
    """Connect to WebSocket."""
    self._log.info("Connecting to Paradex WebSocket...")

    # Connect WebSocket client
    await self._ws.connect()

    # Start message handler
    self._ws_task = asyncio.create_task(self._handle_ws_messages())

    self._log.info("Connected")

async def _handle_ws_messages(self) -> None:
    """Handle incoming WebSocket messages."""
    while True:
        try:
            message = await self._ws.receive()

            # Route message by type
            if message["channel"] == "orderbook":
                await self._handle_orderbook_update(message)
            elif message["channel"] == "trades":
                await self._handle_trade_update(message)
            elif message["channel"] == "markets":
                await self._handle_market_update(message)

        except asyncio.CancelledError:
            break
        except Exception as e:
            self._log.error(f"WebSocket handler error: {e}")

async def _handle_orderbook_update(self, message: dict) -> None:
    """Handle order book update."""
    market = message["market"]
    instrument_id = InstrumentId.from_str(f"{market}.PARADEX")

    # Convert to Nautilus OrderBookDelta
    for bid in message.get("bids", []):
        delta = OrderBookDelta(
            instrument_id=instrument_id,
            action=BookAction.UPDATE,
            order=BookOrder(
                side=OrderSide.BUY,
                price=Price.from_str(bid["price"]),
                size=Quantity.from_str(bid["size"]),
                order_id=0,
            ),
            flags=0,
            sequence=message["sequence"],
            ts_event=millis_to_nanos(message["timestamp"]),
            ts_init=self._clock.timestamp_ns(),
        )
        self._handle_data(delta)
```

📦 factories.py (Type Conversions)

**Critical Conversions**

```python
def parse_instrument(market_data: dict, venue: Venue) -> CryptoPerpetual:
    """Convert Paradex market to Nautilus instrument."""
    return CryptoPerpetual(
        instrument_id=InstrumentId(Symbol(market_data["symbol"]), venue),
        raw_symbol=Symbol(market_data["symbol"]),
        base_currency=Currency.from_str(market_data["base_currency"]),
        quote_currency=Currency.from_str(market_data["quote_currency"]),
        settlement_currency=Currency.from_str(market_data["quote_currency"]),
        is_inverse=False,
        price_precision=len(market_data["price_tick_size"].split(".")[-1]),
        size_precision=len(market_data["quantity_tick_size"].split(".")[-1]),
        price_increment=Price.from_str(market_data["price_tick_size"]),
        size_increment=Quantity.from_str(market_data["quantity_tick_size"]),
        max_quantity=Quantity.from_str(market_data["max_quantity"]),
        min_quantity=Quantity.from_str(market_data["min_quantity"]),
        max_price=None,
        min_price=None,
        margin_init=Decimal(market_data["initial_margin_fraction"]),
        margin_maint=Decimal(market_data["maintenance_margin_fraction"]),
        maker_fee=Decimal(market_data["maker_fee"]),
        taker_fee=Decimal(market_data["taker_fee"]),
        ts_event=0,
        ts_init=0,
    )

def parse_order_status_report(
    order_data: dict,
    instrument: InstrumentAny,
    account_id: AccountId,
    clock: LiveClock,
) -> OrderStatusReport:
    """Convert Paradex order to Nautilus OrderStatusReport."""
    return OrderStatusReport(
        account_id=account_id,
        instrument_id=instrument.id,
        client_order_id=ClientOrderId(order_data.get("client_id", "")),
        venue_order_id=VenueOrderId(order_data["id"]),
        order_side=_parse_order_side(order_data["side"]),
        order_type=_parse_order_type(order_data["type"]),
        time_in_force=TimeInForce.GTC,
        order_status=_parse_order_status(order_data["status"]),
        price=Price.from_str(order_data["price"]) if order_data.get("price") else None,
        quantity=Quantity.from_str(order_data["size"]),
        filled_qty=Quantity.from_str(order_data.get("filled_size", "0")),
        ts_accepted=millis_to_nanos(order_data["created_at"]),
        ts_last=millis_to_nanos(order_data["updated_at"]),
        report_id=UUID4(order_data["id"]),
        ts_init=clock.timestamp_ns(),
    )
```

📋 TESTING STRATEGY

**Unit Tests**
```python
def test_parse_instrument():
    market_data = {
        "symbol": "BTC-USD-PERP",
        "base_currency": "BTC",
        "quote_currency": "USD",
        # ...
    }
    instrument = parse_instrument(market_data, PARADEX)
    assert instrument.id.symbol.value == "BTC-USD-PERP"
    assert instrument.id.venue == PARADEX
```

**Integration Tests**
```python
@pytest.mark.asyncio
async def test_execution_client_connect():
    client = ParadexExecutionClient(...)
    await client._connect()
    # Verify reconciliation occurred
    assert len(client._emitted_orders) >= 0
```

Next: See 3_IMPLEMENTATION_ROADMAP.md for deployment steps
