# QUICK START WITH AUTO-VALIDATION - FIX PARADEX ADAPTER

**Goal:** Make Paradex adapter compliant with Nautilus specification  
**Time:** 8-10 hours focused work  
**Method:** Implement → Validate → Fix → Proceed  
**Reference:** OKX adapter + agent-auto-validation.md

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

## 🎯 VALIDATION-FIRST APPROACH

### Core Principle:
**VALIDATE AFTER EVERY PHASE - NO EXCEPTIONS**

### Validation Commands:
```bash
# Syntax check
python -m py_compile [file].py

# Import test  
python -c "from nautilus_trader.adapters.paradex import *"

# Method count
python count_methods.py

# Type check (if mypy available)
mypy [file].py --ignore-missing-imports
```

---

## PHASE 1: BACKUP & SETUP (5 min)

### Step 1.1: Create Backups
```bash
cd /home/mok/projects/nautilus-dinger/memory-bank

cp data.py data.py.backup
cp execution.py execution.py.backup
cp data.py data_new.py
cp execution.py execution_new.py
```

### ✅ VALIDATION 1.1
```bash
# Verify backups
ls -lh *.backup | wc -l
# Expected: 2 (data.py.backup, execution.py.backup)
```

**Checklist:**
- [ ] Backups created
- [ ] Working copies created
- [ ] No file errors

**Status:** PASS / FAIL  
**If FAIL:** Check permissions, verify paths

---

## PHASE 2: FIX DATA.PY IMPORTS (10 min)

### Step 2.1: Add Imports
Add to top of `data_new.py`:

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
from nautilus_trader.cache.transformers import transform_instrument_from_pyo3
```

### ✅ VALIDATION 2.1
```bash
# Test imports
python -c "
from nautilus_trader.data.messages import SubscribeTradeTicks
from nautilus_trader.data.messages import RequestBars
from nautilus_trader.core.datetime import ensure_pydatetime_utc
print('✅ All imports successful')
"
```

**Expected Output:** `✅ All imports successful`

**Checklist:**
- [ ] All imports added
- [ ] No import errors
- [ ] Syntax valid

**Status:** PASS / FAIL  
**If FAIL:** Check Nautilus installation, verify versions

---

## PHASE 3: FIX METHOD SIGNATURES (30 min)

### Step 3.1: Fix _subscribe_instruments
```python
# OLD:
async def _subscribe_instruments(self) -> None:

# NEW:
async def _subscribe_instruments(self, command: SubscribeInstruments) -> None:
```

### Step 3.2: Fix _unsubscribe_instruments
```python
# OLD:
async def _unsubscribe_instruments(self) -> None:

# NEW:
async def _unsubscribe_instruments(self, command: UnsubscribeInstruments) -> None:
```

### Step 3.3: Fix _subscribe_order_book_deltas
```python
# OLD:
async def _subscribe_order_book_deltas(self, instrument_id: InstrumentId, ...) -> None:

# NEW:
async def _subscribe_order_book_deltas(self, command: SubscribeOrderBook) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    # Use command.depth, command.book_type
```

### Step 3.4: Fix _unsubscribe_order_book_deltas
```python
# OLD:
async def _unsubscribe_order_book_deltas(self, instrument_id: InstrumentId) -> None:

# NEW:
async def _unsubscribe_order_book_deltas(self, command: UnsubscribeOrderBook) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
```

### Step 3.5: Fix _subscribe_trade_ticks
```python
# OLD:
async def _subscribe_trade_ticks(self, instrument_id: InstrumentId) -> None:

# NEW:
async def _subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
```

### Step 3.6: Fix _unsubscribe_trade_ticks
```python
# OLD:
async def _unsubscribe_trade_ticks(self, instrument_id: InstrumentId) -> None:

# NEW:
async def _unsubscribe_trade_ticks(self, command: UnsubscribeTradeTicks) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
```

### ✅ VALIDATION 3.1
```bash
# Syntax check
python -m py_compile data_new.py

# Count async methods
python -c "
import ast
with open('data_new.py') as f:
    tree = ast.parse(f.read())
    
class MethodCounter(ast.NodeVisitor):
    def __init__(self):
        self.methods = []
    def visit_AsyncFunctionDef(self, node):
        if node.name.startswith('_'):
            self.methods.append(node.name)
        self.generic_visit(node)

counter = MethodCounter()
counter.visit(tree)
print(f'Async methods: {len(counter.methods)}')
for m in sorted(counter.methods):
    print(f'  - {m}')
"
```

**Expected:** At least 14 methods (8 original + 6 fixed)

**Checklist:**
- [ ] All 6 signatures fixed
- [ ] No syntax errors
- [ ] PyO3 conversions added
- [ ] Command objects used

**Status:** PASS / FAIL  
**If FAIL:** Review each method, check for typos

**Metrics:**
- Methods updated: __/6
- Syntax errors: __
- PyO3 conversions: __/6

---

## PHASE 4: ADD BASE METHODS (15 min)

### Step 4.1: Add Generic Handlers
Add to `ParadexDataClient` class:

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

### ✅ VALIDATION 4.1
```bash
# Syntax check
python -m py_compile data_new.py

# Verify methods exist
python -c "
import ast
with open('data_new.py') as f:
    tree = ast.parse(f.read())
methods = [node.name for node in ast.walk(tree) if isinstance(node, ast.AsyncFunctionDef)]
required = ['_subscribe', '_unsubscribe', '_request']
for m in required:
    status = '✅' if m in methods else '❌'
    print(f'{status} {m}')
"
```

**Expected Output:**
```
✅ _subscribe
✅ _unsubscribe
✅ _request
```

**Checklist:**
- [ ] 3 base methods added
- [ ] Docstrings included
- [ ] No syntax errors

**Status:** PASS / FAIL

---

## PHASE 5: ADD SUBSCRIPTION METHODS (45 min)

### Step 5.1: Add All Subscription Methods
Copy-paste into `ParadexDataClient`:

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
    self._log.warning("Quote ticks not supported. Use order book instead")

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

### ✅ VALIDATION 5.1
```bash
# Syntax check
python -m py_compile data_new.py

# Count new methods
python -c "
import ast
with open('data_new.py') as f:
    tree = ast.parse(f.read())
methods = [node.name for node in ast.walk(tree) if isinstance(node, ast.AsyncFunctionDef) and node.name.startswith('_')]
print(f'Total async methods: {len(methods)}')
print(f'Expected: ~30 (8 original + 3 base + 16 subscription + requests)')
"
```

**Checklist:**
- [ ] 16 subscription methods added
- [ ] All use command objects
- [ ] PyO3 conversions correct
- [ ] Warnings for unsupported features
- [ ] No syntax errors

**Status:** PASS / FAIL

**Metrics:**
- Methods added: __/16
- Syntax errors: __
- Total methods: __

---

## PHASE 6: ADD REQUEST METHODS (60 min)

### Step 6.1: Add Historical Data Methods
```python
async def _request_instrument(self, request: RequestInstrument) -> None:
    try:
        pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(request.instrument_id.value)
        pyo3_instrument = await self._http_client.request_instrument(pyo3_instrument_id)
        instrument = transform_instrument_from_pyo3(pyo3_instrument)
    except Exception as e:
        self._log.error(f"Failed to request instrument: {e}")
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
    if not request.start or not request.end:
        self._log.warning("Cannot request trades: start and end required")
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
    self._log.warning("Order book snapshots not supported")

async def _request_order_book_depth(self, request: RequestOrderBookDepth) -> None:
    self._log.warning("Order book depth not supported")
```

### ✅ VALIDATION 6.1
```bash
# Final syntax check
python -m py_compile data_new.py

# Final method count
python -c "
import ast
with open('data_new.py') as f:
    tree = ast.parse(f.read())
methods = [node.name for node in ast.walk(tree) if isinstance(node, ast.AsyncFunctionDef) and node.name.startswith('_')]
print(f'✅ Total methods: {len(methods)}')
print(f'Expected: 38 (LiveMarketDataClient requirement)')
print(f'Status: {'PASS' if len(methods) >= 38 else 'FAIL'}')
"
```

**Checklist:**
- [ ] 7 request methods added
- [ ] Error handling included
- [ ] Transform functions used
- [ ] No syntax errors
- [ ] Total methods >= 38

**Status:** PASS / FAIL

**Metrics:**
- Request methods: __/7
- Total methods: __/38
- Syntax errors: __

---

## PHASE 7: FIX EXECUTION CLIENT (30 min)

### Step 7.1: Add Imports
Add to `execution_new.py`:
```python
from nautilus_trader.execution.messages import SubmitOrderList
from nautilus_trader.execution.reports import ExecutionMassStatus
```

### Step 7.2: Add Missing Methods
```python
async def _submit_order_list(self, command: SubmitOrderList) -> None:
    """Submit list of orders."""
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

### ✅ VALIDATION 7.1
```bash
# Syntax check
python -m py_compile execution_new.py

# Method count
python -c "
import ast
with open('execution_new.py') as f:
    tree = ast.parse(f.read())
methods = [node.name for node in ast.walk(tree) if isinstance(node, ast.AsyncFunctionDef)]
required = ['_submit_order_list', 'generate_mass_status']
for m in required:
    status = '✅' if m in methods else '❌'
    print(f'{status} {m}')
print(f'Total methods: {len(methods)}')
print(f'Expected: >= 12')
"
```

**Checklist:**
- [ ] 2 methods added
- [ ] Imports added
- [ ] No syntax errors
- [ ] Total methods >= 12

**Status:** PASS / FAIL

---

## PHASE 8: FINAL VALIDATION (15 min)

### Step 8.1: Comprehensive Syntax Check
```bash
# Check both files
python -m py_compile data_new.py
python -m py_compile execution_new.py

echo "✅ Syntax validation complete"
```

### Step 8.2: Method Count Verification
```bash
# Create validation script
cat > validate_compliance.py << 'EOF'
import ast

def count_methods(filename):
    with open(filename) as f:
        tree = ast.parse(f.read())
    methods = [node.name for node in ast.walk(tree) 
               if isinstance(node, ast.AsyncFunctionDef) 
               and node.name.startswith('_')]
    return methods

data_methods = count_methods('data_new.py')
exec_methods = count_methods('execution_new.py')

print("=" * 60)
print("COMPLIANCE VALIDATION REPORT")
print("=" * 60)
print(f"\nData Client:")
print(f"  Methods found: {len(data_methods)}")
print(f"  Required: 38")
print(f"  Status: {'✅ PASS' if len(data_methods) >= 38 else '❌ FAIL'}")

print(f"\nExecution Client:")
print(f"  Methods found: {len(exec_methods)}")
print(f"  Required: 12")
print(f"  Status: {'✅ PASS' if len(exec_methods) >= 12 else '❌ FAIL'}")

print(f"\nOverall Status: {'✅ COMPLIANT' if len(data_methods) >= 38 and len(exec_methods) >= 12 else '❌ NOT COMPLIANT'}")
print("=" * 60)
EOF

python validate_compliance.py
```

### Step 8.3: Replace Original Files
```bash
# Only if validation passes!
if [ $? -eq 0 ]; then
    mv data_new.py data.py
    mv execution_new.py execution.py
    echo "✅ Files replaced successfully"
else
    echo "❌ Validation failed - keeping original files"
fi
```

### ✅ FINAL VALIDATION CHECKLIST

**Data Client (data.py):**
- [ ] 38+ methods implemented
- [ ] All signatures use command objects
- [ ] PyO3 conversions correct
- [ ] No syntax errors
- [ ] Imports complete

**Execution Client (execution.py):**
- [ ] 12+ methods implemented
- [ ] _submit_order_list added
- [ ] generate_mass_status added
- [ ] No syntax errors
- [ ] Imports complete

**Overall:**
- [ ] Both files compile
- [ ] Method counts correct
- [ ] Ready for testing
- [ ] Backups preserved

**Status:** PASS / FAIL

---

## PHASE 9: CREATE VALIDATION TESTS (30 min)

### Step 9.1: Create Test Directory
```bash
mkdir -p tests/integration_tests/adapters/paradex
cd tests/integration_tests/adapters/paradex
```

### Step 9.2: Create Compliance Test
```python
# test_compliance.py
import pytest
from nautilus_trader.adapters.paradex.data import ParadexDataClient
from nautilus_trader.adapters.paradex.execution import ParadexExecutionClient

def test_data_client_has_all_required_methods():
    """Verify all 38 required methods exist."""
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
        assert hasattr(ParadexDataClient, method), f"Missing: {method}"
        assert callable(getattr(ParadexDataClient, method)), f"Not callable: {method}"

def test_execution_client_has_all_required_methods():
    """Verify all 12 required methods exist."""
    required_methods = [
        '_connect', '_disconnect',
        '_submit_order', '_submit_order_list',
        '_modify_order', '_cancel_order',
        '_cancel_all_orders', '_batch_cancel_orders',
        'generate_order_status_report', 'generate_order_status_reports',
        'generate_fill_reports', 'generate_position_status_reports',
        'generate_mass_status',
    ]
    
    for method in required_methods:
        assert hasattr(ParadexExecutionClient, method), f"Missing: {method}"
        assert callable(getattr(ParadexExecutionClient, method)), f"Not callable: {method}"

if __name__ == "__main__":
    test_data_client_has_all_required_methods()
    test_execution_client_has_all_required_methods()
    print("✅ All compliance tests passed!")
```

### ✅ VALIDATION 9.1
```bash
# Run compliance tests
python test_compliance.py

# Expected output:
# ✅ All compliance tests passed!
```

**Status:** PASS / FAIL

---

**Status:** PASS / FAIL

---

## PHASE 10: REFACTOR & CLEANUP (60 min)

### Step 10.1: Code Review
```bash
# Review all changes
git diff data.py.backup data.py
git diff execution.py.backup execution.py
```

### Step 10.2: Refactor Checklist
- [ ] Remove duplicate code
- [ ] Extract common patterns
- [ ] Improve variable names
- [ ] Add missing docstrings
- [ ] Simplify complex methods
- [ ] Remove debug prints
- [ ] Optimize imports

### Step 10.3: Apply Refactoring
```python
# Example refactoring:

# Before:
async def _subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.subscribe_trades(pyo3_instrument_id)

async def _subscribe_quote_ticks(self, command: SubscribeQuoteTicks) -> None:
    pyo3_instrument_id = nautilus_pyo3.InstrumentId.from_str(command.instrument_id.value)
    await self._ws_client.subscribe_quotes(pyo3_instrument_id)

# After (refactored with helper):
def _to_pyo3_instrument_id(self, instrument_id: InstrumentId) -> nautilus_pyo3.InstrumentId:
    """Convert Nautilus InstrumentId to PyO3 type."""
    return nautilus_pyo3.InstrumentId.from_str(instrument_id.value)

async def _subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
    pyo3_id = self._to_pyo3_instrument_id(command.instrument_id)
    await self._ws_client.subscribe_trades(pyo3_id)

async def _subscribe_quote_ticks(self, command: SubscribeQuoteTicks) -> None:
    pyo3_id = self._to_pyo3_instrument_id(command.instrument_id)
    await self._ws_client.subscribe_quotes(pyo3_id)
```

### ✅ VALIDATION 10.1
```bash
# Syntax check after refactoring
python -m py_compile data.py
python -m py_compile execution.py

# Verify no regressions
python validate_compliance.py

# Check code quality
pylint data.py --disable=C0111,R0913
pylint execution.py --disable=C0111,R0913
```

**Checklist:**
- [ ] Code refactored
- [ ] Duplicates removed
- [ ] Helper methods added
- [ ] Docstrings complete
- [ ] No regressions
- [ ] Quality improved

**Status:** PASS / FAIL

---

## PHASE 11: UNIT TESTS (90 min)

### Step 11.1: Create Test File
```bash
mkdir -p tests/unit
cd tests/unit
```

### Step 11.2: Write Unit Tests
```python
# tests/unit/test_data_client.py
import pytest
from unittest.mock import Mock, AsyncMock
from nautilus_trader.adapters.paradex.data import ParadexDataClient
from nautilus_trader.data.messages import SubscribeTradeTicks
from nautilus_trader.model.identifiers import InstrumentId

@pytest.fixture
def mock_ws_client():
    client = Mock()
    client.subscribe_trades = AsyncMock()
    return client

@pytest.fixture
def data_client(mock_ws_client):
    # Create minimal client for testing
    client = Mock(spec=ParadexDataClient)
    client._ws_client = mock_ws_client
    client._log = Mock()
    return client

def test_subscribe_trade_ticks_converts_to_pyo3():
    """Test that instrument_id is converted to PyO3 type."""
    # Test implementation
    pass

def test_subscribe_trade_ticks_calls_ws_client():
    """Test that WebSocket client is called."""
    # Test implementation
    pass

def test_unsupported_features_log_warning():
    """Test that unsupported features log warnings."""
    # Test implementation
    pass

# Add 10-15 more tests...
```

### ✅ VALIDATION 11.1
```bash
# Run unit tests
pytest tests/unit/test_data_client.py -v

# Check coverage
pytest tests/unit/ --cov=nautilus_trader/adapters/paradex --cov-report=term

# Expected: >80% coverage
```

**Checklist:**
- [ ] Unit tests created
- [ ] All methods tested
- [ ] Edge cases covered
- [ ] Tests passing
- [ ] Coverage >80%

**Status:** PASS / FAIL

---

## PHASE 12: INTEGRATION TESTS (60 min)

### Step 12.1: Create Integration Tests
```python
# tests/integration/adapters/paradex/test_integration.py
import pytest
import asyncio
from nautilus_trader.adapters.paradex.data import ParadexDataClient
from nautilus_trader.adapters.paradex.execution import ParadexExecutionClient

@pytest.mark.asyncio
async def test_data_client_connection_lifecycle():
    """Test connect/disconnect flow."""
    # Test implementation
    pass

@pytest.mark.asyncio
async def test_execution_client_reconciliation():
    """Test reconciliation on connect."""
    # Test implementation
    pass

@pytest.mark.asyncio
async def test_order_submission_flow():
    """Test end-to-end order submission."""
    # Test implementation
    pass
```

### ✅ VALIDATION 12.1
```bash
# Run integration tests
pytest tests/integration/adapters/paradex/ -v

# Full test suite
pytest tests/ -v --cov=nautilus_trader/adapters/paradex --cov-report=html

# Expected: All tests pass, >85% coverage
```

**Checklist:**
- [ ] Integration tests created
- [ ] Connection flow tested
- [ ] Reconciliation tested
- [ ] All tests passing
- [ ] Coverage >85%

**Status:** PASS / FAIL

---

## PHASE 13: PERFORMANCE OPTIMIZATION (45 min)

### Step 13.1: Profile Code
```bash
# Profile Python code
python -m cProfile -o profile.stats test_performance.py
python -m pstats profile.stats
```

### Step 13.2: Optimize Bottlenecks
```python
# Example optimizations:

# Before: Multiple conversions
async def _subscribe_multiple(self, commands):
    for cmd in commands:
        pyo3_id = nautilus_pyo3.InstrumentId.from_str(cmd.instrument_id.value)
        await self._ws_client.subscribe(pyo3_id)

# After: Batch conversion
async def _subscribe_multiple(self, commands):
    pyo3_ids = [
        nautilus_pyo3.InstrumentId.from_str(cmd.instrument_id.value)
        for cmd in commands
    ]
    await self._ws_client.subscribe_batch(pyo3_ids)
```

### ✅ VALIDATION 13.1
```bash
# Benchmark performance
python tests/benchmark_adapter.py

# Expected metrics:
# - State access: <1ms
# - Order submission: <10ms
# - Reconciliation: <5s
```

**Checklist:**
- [ ] Code profiled
- [ ] Bottlenecks identified
- [ ] Optimizations applied
- [ ] Performance improved
- [ ] Benchmarks met

**Status:** PASS / FAIL

---

## PHASE 14: FINAL CODE REVIEW (30 min)

### Step 14.1: Review Checklist
```bash
# Create review checklist
cat > code_review_checklist.md << 'EOF'
# Code Review Checklist

## Code Quality
- [ ] No duplicate code
- [ ] Clear variable names
- [ ] Proper error handling
- [ ] All methods documented
- [ ] Type hints complete
- [ ] No TODOs or FIXMEs

## Compliance
- [ ] All 38 data methods implemented
- [ ] All 12 execution methods implemented
- [ ] Signatures match spec
- [ ] PyO3 conversions correct
- [ ] Reconciliation implemented

## Testing
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Coverage >85%
- [ ] Performance benchmarks met

## Documentation
- [ ] All changes documented
- [ ] Bug fixes recorded
- [ ] Validation results saved
- [ ] Progress updated
EOF
```

### Step 14.2: Final Review
```bash
# Review all files
for file in data.py execution.py providers.py; do
    echo "Reviewing $file..."
    # Manual review
done
```

### ✅ VALIDATION 14.1
```bash
# Final compliance check
python tests/validation/validate_compliance.py

# Generate final report
python tests/validation/generate_report.py > memory-bank/PHASE1_COMPLETION_REPORT.md
```

**Checklist:**
- [ ] Code reviewed
- [ ] All items checked
- [ ] Issues fixed
- [ ] Documentation updated
- [ ] Ready for Phase 2

**Status:** PASS / FAIL

---

## ✅ PHASE 1 COMPLETION CHECKLIST

### Implementation:
- [ ] 6 signatures fixed
- [ ] 3 base methods added
- [ ] 16 subscription methods added
- [ ] 7 request methods added
- [ ] 2 execution methods added
- [ ] Reconciliation implemented

### Refactoring:
- [ ] Code cleaned up
- [ ] Duplicates removed
- [ ] Helper methods extracted
- [ ] Docstrings added
- [ ] Imports optimized

### Testing:
- [ ] Unit tests created (~300 LOC)
- [ ] Integration tests created (~200 LOC)
- [ ] All tests passing
- [ ] Coverage >85%

### Validation:
- [ ] Syntax check passed
- [ ] Import test passed
- [ ] Method count: 38/38 (data), 12/12 (execution)
- [ ] Compliance test passed
- [ ] Performance benchmarks met

### Documentation:
- [ ] Bug fixes documented
- [ ] Improvements logged
- [ ] Validation results saved
- [ ] Progress updated

### Quality Metrics:
- **Total LOC:** ~1,750
- **Test Coverage:** __%
- **Syntax Errors:** 0
- **Compliance:** YES/NO
- **Time Spent:** __h
- **Credits Used:** __

**PHASE 1 STATUS:** [ ] COMPLETE / [ ] INCOMPLETE

---

## 🎯 SUCCESS CRITERIA

**✅ COMPLIANT when:**
1. Data client has >= 38 methods
2. Execution client has >= 12 methods
3. All methods use command objects
4. No syntax errors
5. Compliance tests pass

**Current Status:** [ ] COMPLIANT / [ ] NOT COMPLIANT

---

## 📊 VALIDATION SUMMARY

Create this summary after completion:

```
═══════════════════════════════════════════════════════
PARADEX ADAPTER COMPLIANCE REPORT
═══════════════════════════════════════════════════════
Date: [DATE]
Time Spent: [HOURS]

DATA CLIENT:
  Methods: __/38
  Status: PASS/FAIL
  
EXECUTION CLIENT:
  Methods: __/12
  Status: PASS/FAIL

OVERALL:
  Compliance: YES/NO
  Syntax Errors: __
  Tests Created: __
  Ready for Rust: YES/NO

═══════════════════════════════════════════════════════
```

---

**FOLLOW THIS CHECKLIST EXACTLY**  
**VALIDATE AFTER EVERY PHASE**  
**FIX IMMEDIATELY IF VALIDATION FAILS**
