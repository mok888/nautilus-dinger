# PARADEX NAUTILUS ADAPTER - IMPLEMENTATION ACTION PLAN
**Date:** 2026-01-27  
**Based on:** Official Nautilus OKX Reference + Paradex API  
**Status:** READY TO IMPLEMENT

---

## CRITICAL FINDINGS FROM OFFICIAL REFERENCE

### ✅ OKX Adapter Structure (Our Reference Model)

**Key Observations:**
1. **Method Signatures** - ALL methods accept `command` objects, NOT raw types
2. **Complete Implementation** - OKX has ALL 38 LiveMarketDataClient methods
3. **PyO3 Integration** - Heavy use of `nautilus_pyo3` for Rust interop
4. **Instrument Caching** - Instruments cached in HTTP/WS clients
5. **Error Handling** - Comprehensive try/except with proper logging

---

## PHASE 1: FIX PYTHON METHOD SIGNATURES (CRITICAL)

### data.py - Fix ALL Method Signatures

**WRONG (Current):**
```python
async def _subscribe_trade_ticks(self, instrument_id: InstrumentId) -> None:
```

**CORRECT (Official Pattern):**
```python
async def _subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.subscribe_trades(pyo3_instrument_id)
```

### Required Imports (from OKX):
```python
from nautilus_trader.data.messages import RequestBars
from nautilus_trader.data.messages import RequestInstrument
from nautilus_trader.data.messages import RequestInstruments
from nautilus_trader.data.messages import RequestQuoteTicks
from nautilus_trader.data.messages import RequestTradeTicks
from nautilus_trader.data.messages import SubscribeBars
from nautilus_trader.data.messages import SubscribeFundingRates
from nautilus_trader.data.messages import SubscribeIndexPrices
from nautilus_trader.data.messages import SubscribeInstrument
from nautilus_trader.data.messages import SubscribeInstruments
from nautilus_trader.data.messages import SubscribeMarkPrices
from nautilus_trader.data.messages import SubscribeOrderBook
from nautilus_trader.data.messages import SubscribeQuoteTicks
from nautilus_trader.data.messages import SubscribeTradeTicks
from nautilus_trader.data.messages import UnsubscribeBars
from nautilus_trader.data.messages import UnsubscribeFundingRates
from nautilus_trader.data.messages import UnsubscribeIndexPrices
from nautilus_trader.data.messages import UnsubscribeInstrument
from nautilus_trader.data.messages import UnsubscribeInstruments
from nautilus_trader.data.messages import UnsubscribeMarkPrices
from nautilus_trader.data.messages import UnsubscribeOrderBook
from nautilus_trader.data.messages import UnsubscribeQuoteTicks
from nautilus_trader.data.messages import UnsubscribeTradeTicks
```

---

## PHASE 2: ADD MISSING DATA CLIENT METHODS

### Base Methods (REQUIRED):
```python
async def _subscribe(self, command: SubscribeData) -> None:
    # Generic subscription handler
    pass

async def _unsubscribe(self, command: UnsubscribeData) -> None:
    # Generic unsubscription handler
    pass

async def _request(self, request: RequestData) -> None:
    # Generic request handler
    pass
```

### Instrument Methods:
```python
async def _subscribe_instrument(self, command: SubscribeInstrument) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.subscribe_instrument(pyo3_instrument_id)

async def _unsubscribe_instrument(self, command: UnsubscribeInstrument) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.unsubscribe_instrument(pyo3_instrument_id)
```

### Order Book Snapshots:
```python
async def _subscribe_order_book_snapshots(self, command: SubscribeOrderBook) -> None:
    # Paradex may not support snapshots - log warning
    self._log.warning("Order book snapshots not supported by Paradex")

async def _unsubscribe_order_book_snapshots(self, command: UnsubscribeOrderBook) -> None:
    pass
```

### Quote Ticks:
```python
async def _subscribe_quote_ticks(self, command: SubscribeQuoteTicks) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.subscribe_quotes(pyo3_instrument_id)

async def _unsubscribe_quote_ticks(self, command: UnsubscribeQuoteTicks) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.unsubscribe_quotes(pyo3_instrument_id)
```

### Mark Prices:
```python
async def _subscribe_mark_prices(self, command: SubscribeMarkPrices) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.subscribe_mark_prices(pyo3_instrument_id)

async def _unsubscribe_mark_prices(self, command: UnsubscribeMarkPrices) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.unsubscribe_mark_prices(pyo3_instrument_id)
```

### Index Prices:
```python
async def _subscribe_index_prices(self, command: SubscribeIndexPrices) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.subscribe_index_prices(pyo3_instrument_id)

async def _unsubscribe_index_prices(self, command: UnsubscribeIndexPrices) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.unsubscribe_index_prices(pyo3_instrument_id)
```

### Funding Rates:
```python
async def _subscribe_funding_rates(self, command: SubscribeFundingRates) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.subscribe_funding_rates(pyo3_instrument_id)

async def _unsubscribe_funding_rates(self, command: UnsubscribeFundingRates) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.unsubscribe_funding_rates(pyo3_instrument_id)
```

### Bars:
```python
async def _subscribe_bars(self, command: SubscribeBars) -> None:
    pyo3_bar_type = nautilus_pyo3.BarType.from_str(str(command.bar_type))
    await self._ws_client.subscribe_bars(pyo3_bar_type)

async def _unsubscribe_bars(self, command: UnsubscribeBars) -> None:
    pyo3_bar_type = nautilus_pyo3.BarType.from_str(str(command.bar_type))
    await self._ws_client.unsubscribe_bars(pyo3_bar_type)
```

### Instrument Status:
```python
async def _subscribe_instrument_status(self, command: SubscribeInstrumentStatus) -> None:
    # Paradex may not support - log warning
    self._log.warning("Instrument status not supported by Paradex")

async def _unsubscribe_instrument_status(self, command: UnsubscribeInstrumentStatus) -> None:
    pass
```

### Instrument Close:
```python
async def _subscribe_instrument_close(self, command: SubscribeInstrumentClose) -> None:
    # Paradex may not support - log warning
    self._log.warning("Instrument close not supported by Paradex")

async def _unsubscribe_instrument_close(self, command: UnsubscribeInstrumentClose) -> None:
    pass
```

### Historical Data Requests:
```python
async def _request_instrument(self, request: RequestInstrument) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(request.instrument_id.value)
    pyo3_instrument = await self._http_client.request_instrument(pyo3_instrument_id)
    instrument = transform_instrument_from_pyo3(pyo3_instrument)
    self._handle_instrument(instrument, request.id, request.start, request.end, request.params)

async def _request_instruments(self, request: RequestInstruments) -> None:
    pyo3_instruments = await self._http_client.request_instruments()
    instruments = [transform_instrument_from_pyo3(i) for i in pyo3_instruments]
    self._handle_instruments(request.venue, instruments, request.id, request.start, request.end, request.params)

async def _request_quote_ticks(self, request: RequestQuoteTicks) -> None:
    self._log.warning("Historical quotes not supported by Paradex")

async def _request_trade_ticks(self, request: RequestTradeTicks) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(request.instrument_id.value)
    pyo3_trades = await self._http_client.request_trades(
        instrument_id=pyo3_instrument_id,
        start=ensure_pydatetime_utc(request.start),
        end=ensure_pydatetime_utc(request.end),
        limit=request.limit,
    )
    trades = TradeTick.from_pyo3_list(pyo3_trades)
    self._handle_trade_ticks(request.instrument_id, trades, request.id, request.start, request.end, request.params)

async def _request_bars(self, request: RequestBars) -> None:
    pyo3_bar_type = nautilus_pyo3.BarType.from_str(str(request.bar_type))
    pyo3_bars = await self._http_client.request_bars(
        bar_type=pyo3_bar_type,
        start=ensure_pydatetime_utc(request.start),
        end=ensure_pydatetime_utc(request.end),
        limit=request.limit,
    )
    bars = Bar.from_pyo3_list(pyo3_bars)
    self._handle_bars(request.bar_type, bars, request.id, request.start, request.end, request.params)

async def _request_order_book_snapshot(self, request: RequestOrderBookSnapshot) -> None:
    self._log.warning("Order book snapshots not supported by Paradex")

async def _request_order_book_depth(self, request: RequestOrderBookDepth) -> None:
    self._log.warning("Order book depth not supported by Paradex")
```

---

## PHASE 3: FIX EXECUTION CLIENT

### Add Missing Methods:

```python
async def _submit_order_list(self, command: SubmitOrderList) -> None:
    """Submit a list of orders atomically."""
    for order in command.order_list.orders:
        submit_command = SubmitOrder(
            trader_id=command.trader_id,
            strategy_id=command.strategy_id,
            order=order,
            command_id=UUID4(),
            ts_init=self._clock.timestamp_ns(),
        )
        await self._submit_order(submit_command)

async def generate_mass_status(
    self,
    lookback_mins: int | None = None,
) -> ExecutionMassStatus | None:
    """Generate mass status report."""
    order_reports = await self.generate_order_status_reports(
        GenerateOrderStatusReports(
            trader_id=self.trader_id,
            command_id=UUID4(),
            ts_init=self._clock.timestamp_ns(),
        )
    )
    
    fill_reports = await self.generate_fill_reports(
        GenerateFillReports(
            trader_id=self.trader_id,
            command_id=UUID4(),
            ts_init=self._clock.timestamp_ns(),
        )
    )
    
    position_reports = await self.generate_position_status_reports(
        GeneratePositionStatusReports(
            trader_id=self.trader_id,
            command_id=UUID4(),
            ts_init=self._clock.timestamp_ns(),
        )
    )
    
    return ExecutionMassStatus(
        client_id=self.client_id,
        account_id=self.account_id,
        venue=self.venue,
        order_reports=order_reports,
        fill_reports=fill_reports,
        position_reports=position_reports,
        report_id=UUID4(),
        ts_init=self._clock.timestamp_ns(),
    )
```

---

## PHASE 4: PARADEX-SPECIFIC ADAPTATIONS

### Paradex API Characteristics:
1. **Authentication**: JWT tokens + STARK signatures
2. **WebSocket**: JSON-RPC 2.0 protocol
3. **Instruments**: Perpetual futures only (no spot)
4. **Order Types**: Market, Limit, Stop-Market, Stop-Limit
5. **Margin**: Cross-margin system

### Key Differences from OKX:
- Paradex uses STARK signatures (StarkNet), not HMAC-SHA256
- WebSocket uses JSON-RPC, not raw JSON
- No instrument types (only perpetuals)
- Different order status lifecycle

---

## IMPLEMENTATION CHECKLIST

### Python Layer
- [ ] Fix all method signatures in `data.py` (30 methods)
- [ ] Add missing imports
- [ ] Add `_subscribe()`, `_unsubscribe()`, `_request()` base methods
- [ ] Add all quote tick methods
- [ ] Add all bar methods
- [ ] Add all historical request methods
- [ ] Add `_submit_order_list()` to execution client
- [ ] Add `generate_mass_status()` to execution client
- [ ] Update imports in `execution.py`

### Testing
- [ ] Create `tests/integration_tests/adapters/paradex/` directory
- [ ] Add `test_data.py` with subscription tests
- [ ] Add `test_execution.py` with order tests
- [ ] Add `test_providers.py` with instrument tests

---

## ESTIMATED EFFORT

| Task | LOC | Time |
|------|-----|------|
| Fix data.py signatures | ~500 | 2 hours |
| Add missing data methods | ~800 | 3 hours |
| Fix execution.py | ~200 | 1 hour |
| Add tests | ~600 | 2 hours |
| **TOTAL** | **~2,100** | **8 hours** |

---

## NEXT IMMEDIATE ACTIONS

1. **Backup current files**
2. **Fix `data.py` method signatures** (CRITICAL)
3. **Add all missing methods** following OKX pattern
4. **Test imports** - ensure no missing dependencies
5. **Create minimal tests** to validate structure

---

**STATUS: READY TO IMPLEMENT**  
**REFERENCE: OKX adapter is our gold standard**  
**PATTERN: Copy OKX structure, adapt for Paradex API**
