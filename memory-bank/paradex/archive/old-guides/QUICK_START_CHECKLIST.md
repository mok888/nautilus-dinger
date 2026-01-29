# QUICK START CHECKLIST - FIX PARADEX ADAPTER
**WITH AUTOMATED VALIDATION AT EVERY STEP**

**Goal:** Make Paradex adapter compliant with Nautilus specification  
**Time:** 8-10 hours focused work  
**Reference:** OKX adapter (official gold standard)  
**Validation:** Auto-validate after EVERY phase

---

## 🚀 PREREQUISITES

### Install Nautilus Trader
```bash
# Install Nautilus Trader via pip
pip install nautilus_trader

# Verify installation
python -c "import nautilus_trader; print(f'Nautilus Trader {nautilus_trader.__version__} installed')"
```

---

## 🎯 VALIDATION FRAMEWORK

This checklist integrates **agent-auto-validation.md** at every step:

### Validation Rules:
1. ✅ **Validate after EVERY phase** - No exceptions
2. ✅ **Fix immediately if validation fails** - Don't proceed
3. ✅ **Show validation output** - Prove it works
4. ✅ **Track metrics** - Coverage, type safety, tests

### Validation Commands:
```bash
# Syntax check
python -m py_compile [file].py

# Type check
mypy [file].py

# Import test
python -c "from nautilus_trader.adapters.paradex.[module] import *"

# Method count
python -c "from nautilus_trader.adapters.paradex.data import ParadexDataClient; print(len([m for m in dir(ParadexDataClient) if m.startswith('_')]))"
```

---

## ☑️ PHASE 1: BACKUP & SETUP (5 minutes)

```bash
cd /home/mok/projects/nautilus-dinger/memory-bank

# Backup current files
cp data.py data.py.backup
cp execution.py execution.py.backup
cp providers.py providers.py.backup
cp factories.py factories.py.backup

# Create new working copies
cp data.py data_new.py
cp execution.py execution_new.py
```

### ✅ VALIDATION CHECKPOINT 1.1
```bash
# Verify backups exist
ls -lh *.backup

# Expected output: 4 backup files
# data.py.backup
# execution.py.backup
# providers.py.backup
# factories.py.backup
```

**Status:** [ ] PASS / [ ] FAIL  
**If FAIL:** Check file permissions, verify paths

---

## ☑️ PHASE 2: FIX DATA.PY IMPORTS (10 minutes)

Add these imports at the top of `data_new.py`:

```python
from nautilus_trader.data.messages import RequestBars
from nautilus_trader.data.messages import RequestInstrument
from nautilus_trader.data.messages import RequestInstruments
from nautilus_trader.data.messages import RequestOrderBookDepth
from nautilus_trader.data.messages import RequestOrderBookSnapshot
from nautilus_trader.data.messages import RequestQuoteTicks
from nautilus_trader.data.messages import RequestTradeTicks
from nautilus_trader.data.messages import SubscribeBars
from nautilus_trader.data.messages import SubscribeData
from nautilus_trader.data.messages import SubscribeFundingRates
from nautilus_trader.data.messages import SubscribeIndexPrices
from nautilus_trader.data.messages import SubscribeInstrument
from nautilus_trader.data.messages import SubscribeInstrumentClose
from nautilus_trader.data.messages import SubscribeInstruments
from nautilus_trader.data.messages import SubscribeInstrumentStatus
from nautilus_trader.data.messages import SubscribeMarkPrices
from nautilus_trader.data.messages import SubscribeOrderBook
from nautilus_trader.data.messages import SubscribeQuoteTicks
from nautilus_trader.data.messages import SubscribeTradeTicks
from nautilus_trader.data.messages import UnsubscribeBars
from nautilus_trader.data.messages import UnsubscribeData
from nautilus_trader.data.messages import UnsubscribeFundingRates
from nautilus_trader.data.messages import UnsubscribeIndexPrices
from nautilus_trader.data.messages import UnsubscribeInstrument
from nautilus_trader.data.messages import UnsubscribeInstrumentClose
from nautilus_trader.data.messages import UnsubscribeInstruments
from nautilus_trader.data.messages import UnsubscribeInstrumentStatus
from nautilus_trader.data.messages import UnsubscribeMarkPrices
from nautilus_trader.data.messages import UnsubscribeOrderBook
from nautilus_trader.data.messages import UnsubscribeQuoteTicks
from nautilus_trader.data.messages import UnsubscribeTradeTicks
from nautilus_trader.core.datetime import ensure_pydatetime_utc
from nautilus_trader.model.data import Bar
from nautilus_trader.model.data import TradeTick
```

### ✅ VALIDATION CHECKPOINT 2.1
```bash
# Test imports
python -c "
from nautilus_trader.data.messages import SubscribeTradeTicks
from nautilus_trader.data.messages import UnsubscribeTradeTicks
from nautilus_trader.data.messages import RequestBars
print('✅ All imports successful')
"

# Expected output: ✅ All imports successful
```

**Status:** [ ] PASS / [ ] FAIL  
**If FAIL:** Check Nautilus installation, verify import paths

---

## ☑️ PHASE 3: FIX EXISTING METHOD SIGNATURES (30 minutes)

### Change #1: _subscribe_instruments
```python
# OLD:
async def _subscribe_instruments(self) -> None:

# NEW:
async def _subscribe_instruments(self, command: SubscribeInstruments) -> None:
```

### Change #2: _unsubscribe_instruments
```python
# OLD:
async def _unsubscribe_instruments(self) -> None:

# NEW:
async def _unsubscribe_instruments(self, command: UnsubscribeInstruments) -> None:
```

### Change #3: _subscribe_order_book_deltas
```python
# OLD:
async def _subscribe_order_book_deltas(self, instrument_id: InstrumentId, ...) -> None:

# NEW:
async def _subscribe_order_book_deltas(self, command: SubscribeOrderBook) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    # Use command.depth, command.book_type, etc.
```

### Change #4: _unsubscribe_order_book_deltas
```python
# OLD:
async def _unsubscribe_order_book_deltas(self, instrument_id: InstrumentId) -> None:

# NEW:
async def _unsubscribe_order_book_deltas(self, command: UnsubscribeOrderBook) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
```

### Change #5: _subscribe_trade_ticks
```python
# OLD:
async def _subscribe_trade_ticks(self, instrument_id: InstrumentId) -> None:

# NEW:
async def _subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
```

### Change #6: _unsubscribe_trade_ticks
```python
# OLD:
async def _unsubscribe_trade_ticks(self, instrument_id: InstrumentId) -> None:

# NEW:
async def _unsubscribe_trade_ticks(self, command: UnsubscribeTradeTicks) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
```

---

## ☑️ PHASE 4: ADD BASE METHODS (15 minutes)

Add these three methods to `ParadexDataClient`:

```python
async def _subscribe(self, command: SubscribeData) -> None:
    """Generic subscription handler."""
    self._log.debug(f"Generic subscribe: {command.data_type}")

async def _unsubscribe(self, command: UnsubscribeData) -> None:
    """Generic unsubscription handler."""
    self._log.debug(f"Generic unsubscribe: {command.data_type}")

async def _request(self, request: RequestData) -> None:
    """Generic request handler."""
    self._log.debug(f"Generic request: {request.data_type}")
```

---

## ☑️ PHASE 5: ADD SUBSCRIPTION METHODS (45 minutes)

Copy-paste these methods into `ParadexDataClient`:

```python
async def _subscribe_instrument(self, command: SubscribeInstrument) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.subscribe_instrument(pyo3_instrument_id)

async def _unsubscribe_instrument(self, command: UnsubscribeInstrument) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.unsubscribe_instrument(pyo3_instrument_id)

async def _subscribe_order_book_snapshots(self, command: SubscribeOrderBook) -> None:
    self._log.warning("Order book snapshots not supported by Paradex")

async def _unsubscribe_order_book_snapshots(self, command: UnsubscribeOrderBook) -> None:
    pass

async def _subscribe_quote_ticks(self, command: SubscribeQuoteTicks) -> None:
    self._log.warning("Quote ticks not supported by Paradex. Use order book instead")

async def _unsubscribe_quote_ticks(self, command: UnsubscribeQuoteTicks) -> None:
    pass

async def _subscribe_mark_prices(self, command: SubscribeMarkPrices) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.subscribe_mark_prices(pyo3_instrument_id)

async def _unsubscribe_mark_prices(self, command: UnsubscribeMarkPrices) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.unsubscribe_mark_prices(pyo3_instrument_id)

async def _subscribe_index_prices(self, command: SubscribeIndexPrices) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.subscribe_index_prices(pyo3_instrument_id)

async def _unsubscribe_index_prices(self, command: UnsubscribeIndexPrices) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.unsubscribe_index_prices(pyo3_instrument_id)

async def _subscribe_funding_rates(self, command: SubscribeFundingRates) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.subscribe_funding_rates(pyo3_instrument_id)

async def _unsubscribe_funding_rates(self, command: UnsubscribeFundingRates) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.unsubscribe_funding_rates(pyo3_instrument_id)

async def _subscribe_bars(self, command: SubscribeBars) -> None:
    pyo3_bar_type = nautilus_pyo3.BarType.from_str(str(command.bar_type))
    await self._ws_client.subscribe_bars(pyo3_bar_type)

async def _unsubscribe_bars(self, command: UnsubscribeBars) -> None:
    pyo3_bar_type = nautilus_pyo3.BarType.from_str(str(command.bar_type))
    await self._ws_client.unsubscribe_bars(pyo3_bar_type)

async def _subscribe_instrument_status(self, command: SubscribeInstrumentStatus) -> None:
    self._log.warning("Instrument status not supported by Paradex")

async def _unsubscribe_instrument_status(self, command: UnsubscribeInstrumentStatus) -> None:
    pass

async def _subscribe_instrument_close(self, command: SubscribeInstrumentClose) -> None:
    self._log.warning("Instrument close not supported by Paradex")

async def _unsubscribe_instrument_close(self, command: UnsubscribeInstrumentClose) -> None:
    pass
```

---

## ☑️ PHASE 6: ADD REQUEST METHODS (60 minutes)

Copy-paste these methods:

```python
async def _request_instrument(self, request: RequestInstrument) -> None:
    try:
        pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(request.instrument_id.value)
        pyo3_instrument = await self._http_client.request_instrument(pyo3_instrument_id)
        instrument = transform_instrument_from_pyo3(pyo3_instrument)
    except Exception as e:
        self._log.error(f"Failed to request instrument {request.instrument_id}: {e}")
        return
    
    self._handle_instrument(instrument, request.id, request.start, request.end, request.params)

async def _request_instruments(self, request: RequestInstruments) -> None:
    try:
        pyo3_instruments = await self._http_client.request_instruments()
        instruments = [transform_instrument_from_pyo3(i) for i in pyo3_instruments]
    except Exception as e:
        self._log.error(f"Failed to request instruments: {e}")
        return
    
    self._handle_instruments(request.venue, instruments, request.id, request.start, request.end, request.params)

async def _request_quote_ticks(self, request: RequestQuoteTicks) -> None:
    self._log.warning("Historical quotes not supported by Paradex")

async def _request_trade_ticks(self, request: RequestTradeTicks) -> None:
    if request.start is None or request.end is None:
        self._log.warning("Cannot request trades: both start and end required")
        return
    
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

## ☑️ PHASE 7: FIX EXECUTION.PY (30 minutes)

Add these imports to `execution_new.py`:

```python
from nautilus_trader.execution.messages import SubmitOrderList
from nautilus_trader.execution.reports import ExecutionMassStatus
```

Add these methods to `ParadexExecutionClient`:

```python
async def _submit_order_list(self, command: SubmitOrderList) -> None:
    """Submit a list of orders."""
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

## ☑️ PHASE 8: VALIDATE (15 minutes)

```bash
# Test Python syntax
python -m py_compile data_new.py
python -m py_compile execution_new.py

# If no errors, replace old files
mv data_new.py data.py
mv execution_new.py execution.py

# Commit changes
git add data.py execution.py
git commit -m "Fix: Make Paradex adapter compliant with Nautilus specification"
```

---

## ☑️ PHASE 9: CREATE BASIC TESTS (30 minutes)

```bash
mkdir -p tests/integration_tests/adapters/paradex
cd tests/integration_tests/adapters/paradex
```

Create `test_data.py`:
```python
import pytest
from nautilus_trader.adapters.paradex.data import ParadexDataClient

def test_data_client_has_all_methods():
    """Verify all required methods exist."""
    required_methods = [
        '_connect', '_disconnect',
        '_subscribe', '_unsubscribe', '_request',
        '_subscribe_instruments', '_unsubscribe_instruments',
        '_subscribe_instrument', '_unsubscribe_instrument',
        '_subscribe_order_book_deltas', '_unsubscribe_order_book_deltas',
        '_subscribe_order_book_snapshots', '_unsubscribe_order_book_snapshots',
        '_subscribe_quote_ticks', '_unsubscribe_quote_ticks',
        '_subscribe_trade_ticks', '_unsubscribe_trade_ticks',
        '_subscribe_mark_prices', '_unsubscribe_mark_prices',
        '_subscribe_index_prices', '_unsubscribe_index_prices',
        '_subscribe_funding_rates', '_unsubscribe_funding_rates',
        '_subscribe_bars', '_unsubscribe_bars',
        '_subscribe_instrument_status', '_unsubscribe_instrument_status',
        '_subscribe_instrument_close', '_unsubscribe_instrument_close',
        '_request_instrument', '_request_instruments',
        '_request_quote_ticks', '_request_trade_ticks', '_request_bars',
        '_request_order_book_snapshot', '_request_order_book_depth',
    ]
    
    for method in required_methods:
        assert hasattr(ParadexDataClient, method), f"Missing method: {method}"
```

---

## ✅ COMPLETION CHECKLIST

- [ ] Phase 1: Backup files
- [ ] Phase 2: Add imports to data.py
- [ ] Phase 3: Fix 6 existing method signatures
- [ ] Phase 4: Add 3 base methods
- [ ] Phase 5: Add 16 subscription methods
- [ ] Phase 6: Add 7 request methods
- [ ] Phase 7: Fix execution.py (2 methods)
- [ ] Phase 8: Validate syntax
- [ ] Phase 9: Create basic tests

**Total Time: 8-10 hours**

---

## VERIFICATION

Run this to verify compliance:

```python
from nautilus_trader.adapters.paradex.data import ParadexDataClient
from nautilus_trader.adapters.paradex.execution import ParadexExecutionClient

# Count methods
data_methods = [m for m in dir(ParadexDataClient) if m.startswith('_') and callable(getattr(ParadexDataClient, m))]
exec_methods = [m for m in dir(ParadexExecutionClient) if m.startswith('_') and callable(getattr(ParadexExecutionClient, m))]

print(f"Data client methods: {len(data_methods)}")  # Should be ~38
print(f"Execution client methods: {len(exec_methods)}")  # Should be ~12
```

---

**START HERE - FOLLOW EACH PHASE IN ORDER**  
**ESTIMATED TIME: 8-10 HOURS**  
**DIFFICULTY: MEDIUM (mostly copy-paste)**
