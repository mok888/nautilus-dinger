# NAUTILUS ADAPTER PATTERNS - QUICK REFERENCE
**Source:** OKX Official Implementation  
**Use:** Copy these exact patterns for Paradex

---

## PATTERN 1: Method Signature (CRITICAL)

### ❌ WRONG (Your Current Code):
```python
async def _subscribe_trade_ticks(self, instrument_id: InstrumentId) -> None:
    await self._ws_client.subscribe_trades(instrument_id)
```

### ✅ CORRECT (Official Pattern):
```python
async def _subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.subscribe_trades(pyo3_instrument_id)
```

**Key Points:**
- Accept `command` object, NOT raw types
- Extract `instrument_id` from `command.instrument_id`
- Convert to PyO3 type using `.from_str()`

---

## PATTERN 2: Order Book Subscription

```python
async def _subscribe_order_book_deltas(self, command: SubscribeOrderBook) -> None:
    if command.book_type != BookType.L2_MBP:
        self._log.warning(
            f"Book type {book_type_to_str(command.book_type)} not supported, skipping"
        )
        return
    
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.subscribe_book(pyo3_instrument_id, command.depth)
```

---

## PATTERN 3: Historical Data Request

```python
async def _request_trade_ticks(self, request: RequestTradeTicks) -> None:
    if request.start is None or request.end is None:
        self._log.warning(
            f"Cannot request historical trades: both start and end required"
        )
        return
    
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(request.instrument_id.value)
    pyo3_trades = await self._http_client.request_trades(
        instrument_id=pyo3_instrument_id,
        start=ensure_pydatetime_utc(request.start),
        end=ensure_pydatetime_utc(request.end),
        limit=request.limit,
    )
    
    trades = TradeTick.from_pyo3_list(pyo3_trades)
    self._handle_trade_ticks(
        request.instrument_id,
        trades,
        request.id,
        request.start,
        request.end,
        request.params,
    )
```

---

## PATTERN 4: Unsupported Features

```python
async def _subscribe_quote_ticks(self, command: SubscribeQuoteTicks) -> None:
    self._log.warning(
        "Quote ticks not supported by Paradex. Subscribe to order book instead"
    )

async def _unsubscribe_quote_ticks(self, command: UnsubscribeQuoteTicks) -> None:
    pass  # No-op for unsupported features
```

---

## PATTERN 5: Instrument Requests

```python
async def _request_instrument(self, request: RequestInstrument) -> None:
    try:
        pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(request.instrument_id.value)
        pyo3_instrument = await self._http_client.request_instrument(pyo3_instrument_id)
        
        # Cache in HTTP client
        self._cache_instrument(pyo3_instrument)
        
        # Transform to Nautilus type
        instrument = transform_instrument_from_pyo3(pyo3_instrument)
    except Exception as e:
        self._log.error(f"Failed to request instrument {request.instrument_id}: {e}")
        return
    
    self._handle_instrument(
        instrument,
        request.id,
        request.start,
        request.end,
        request.params,
    )
```

---

## PATTERN 6: Order Submission (Execution Client)

```python
async def _submit_order(self, command: SubmitOrder) -> None:
    order = command.order
    
    if order.is_closed:
        self._log.warning(f"Cannot submit already closed order: {order}")
        return
    
    # Convert to PyO3 types
    pyo3_trader_id = nautilus_pyo3.TraderId.from_str(order.trader_id.value)
    pyo3_strategy_id = nautilus_pyo3.StrategyId.from_str(order.strategy_id.value)
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(order.instrument_id.value)
    pyo3_client_order_id = nautilus_pyo3.ClientOrderId(order.client_order_id.value)
    pyo3_order_side = order_side_to_pyo3(order.side)
    pyo3_order_type = order_type_to_pyo3(order.order_type)
    pyo3_quantity = nautilus_pyo3.Quantity.from_str(str(order.quantity))
    pyo3_price = nautilus_pyo3.Price.from_str(str(order.price)) if order.has_price else None
    
    try:
        # Generate OrderSubmitted BEFORE sending to exchange
        self.generate_order_submitted(
            strategy_id=order.strategy_id,
            instrument_id=order.instrument_id,
            client_order_id=order.client_order_id,
            ts_event=self._clock.timestamp_ns(),
        )
        
        await self._ws_client.submit_order(
            trader_id=pyo3_trader_id,
            strategy_id=pyo3_strategy_id,
            instrument_id=pyo3_instrument_id,
            client_order_id=pyo3_client_order_id,
            order_side=pyo3_order_side,
            order_type=pyo3_order_type,
            quantity=pyo3_quantity,
            price=pyo3_price,
        )
    except Exception as e:
        self.generate_order_rejected(
            strategy_id=order.strategy_id,
            instrument_id=order.instrument_id,
            client_order_id=order.client_order_id,
            reason=str(e),
            ts_event=self._clock.timestamp_ns(),
        )
```

---

## PATTERN 7: Generate Reports

```python
async def generate_order_status_reports(
    self,
    command: GenerateOrderStatusReports,
) -> list[OrderStatusReport]:
    if not self._http_client.is_initialized():
        await self._cache_instruments()
    
    self._log.debug("Requesting OrderStatusReports...")
    
    pyo3_reports: list[nautilus_pyo3.OrderStatusReport] = []
    reports: list[OrderStatusReport] = []
    
    try:
        if command.instrument_id:
            pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(
                command.instrument_id.value
            )
            response = await self._http_client.request_order_status_reports(
                account_id=self.pyo3_account_id,
                instrument_id=pyo3_instrument_id,
                start=ensure_pydatetime_utc(command.start),
                end=ensure_pydatetime_utc(command.end),
                open_only=command.open_only,
            )
            pyo3_reports.extend(response)
        else:
            # Request for all instruments
            response = await self._http_client.request_order_status_reports(
                account_id=self.pyo3_account_id,
                start=ensure_pydatetime_utc(command.start),
                end=ensure_pydatetime_utc(command.end),
                open_only=command.open_only,
            )
            pyo3_reports.extend(response)
        
        for pyo3_report in pyo3_reports:
            report = OrderStatusReport.from_pyo3(pyo3_report)
            self._log.debug(f"Received {report}", LogColor.MAGENTA)
            reports.append(report)
    
    except Exception as e:
        self._log.exception("Failed to generate OrderStatusReports", e)
    
    return reports
```

---

## PATTERN 8: WebSocket Message Handler

```python
def _handle_msg(self, msg: Any) -> None:
    if isinstance(msg, nautilus_pyo3.ParadexWebSocketError):
        self._log.error(repr(msg))
        return
    
    try:
        if nautilus_pyo3.is_pycapsule(msg):
            # Capsule contains pointer to Data managed by Rust
            data = capsule_to_data(msg)
            self._handle_data(data)
        elif isinstance(msg, nautilus_pyo3.OrderAccepted):
            event = OrderAccepted.from_dict(msg.to_dict())
            self._send_order_event(event)
        elif isinstance(msg, nautilus_pyo3.OrderCanceled):
            event = OrderCanceled.from_dict(msg.to_dict())
            self._send_order_event(event)
        elif isinstance(msg, nautilus_pyo3.FillReport):
            report = FillReport.from_pyo3(msg)
            self._handle_fill_report(report)
        else:
            self._log.warning(f"Unhandled message type: {type(msg)}")
    except Exception as e:
        self._log.exception("Error handling websocket message", e)
```

---

## PATTERN 9: Instrument Caching

```python
def _cache_instruments(self) -> None:
    """Cache instruments in HTTP and WebSocket clients."""
    instruments_pyo3 = self.instrument_provider.instruments_pyo3()
    for inst in instruments_pyo3:
        self._http_client.cache_instrument(inst)
        if self._ws_client:
            self._ws_client.cache_instrument(inst)
    self._log.debug("Cached instruments", LogColor.MAGENTA)
```

---

## PATTERN 10: Connection Lifecycle

```python
async def _connect(self) -> None:
    # 1. Initialize instrument provider
    await self._instrument_provider.initialize()
    
    # 2. Cache instruments
    self._cache_instruments()
    
    # 3. Send instruments to data engine
    self._send_all_instruments_to_data_engine()
    
    # 4. Connect WebSocket
    instruments = self.instrument_provider.instruments_pyo3()
    await self._ws_client.connect(
        instruments=instruments,
        callback=self._handle_msg,
    )
    
    # 5. Wait for connection
    await self._ws_client.wait_until_active(timeout_secs=30.0)
    self._log.info(f"Connected to {self._ws_client.url}", LogColor.BLUE)
    
    # 6. Subscribe to channels
    await self._ws_client.subscribe_trades()
    await self._ws_client.subscribe_orders()

async def _disconnect(self) -> None:
    # 1. Cancel HTTP requests
    self._http_client.cancel_all_requests()
    
    # 2. Delay for unsubscribe messages
    await asyncio.sleep(1.0)
    
    # 3. Close WebSocket
    if not self._ws_client.is_closed():
        await self._ws_client.close()
        self._log.info(f"Disconnected from {self._ws_client.url}", LogColor.BLUE)
```

---

## KEY TAKEAWAYS

1. **Always use `command` objects** - Never accept raw types
2. **Convert to PyO3 types** - Use `.from_str()` for IDs
3. **Handle errors gracefully** - Log warnings for unsupported features
4. **Cache instruments** - Required for parsing responses
5. **Generate events** - Use `self.generate_*()` methods
6. **Use proper logging** - Include LogColor for visibility

---

**COPY THESE PATTERNS EXACTLY**  
**ADAPT ONLY THE PARADEX-SPECIFIC API CALLS**
