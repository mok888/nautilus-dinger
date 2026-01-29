# nautilus_trader/adapters/paradex/__init__.py
"""Paradex adapter for Nautilus Trader."""

from nautilus_trader.adapters.paradex.config import ParadexDataClientConfig
from nautilus_trader.adapters.paradex.config import ParadexExecClientConfig
from nautilus_trader.adapters.paradex.constants import PARADEX
from nautilus_trader.adapters.paradex.data import ParadexDataClient
from nautilus_trader.adapters.paradex.execution import ParadexExecutionClient
from nautilus_trader.adapters.paradex.factories import get_paradex_instrument_provider
from nautilus_trader.adapters.paradex.providers import ParadexInstrumentProvider


__all__ = [
    "PARADEX",
    "ParadexDataClient",
    "ParadexDataClientConfig",
    "ParadexExecClientConfig",
    "ParadexExecutionClient",
    "ParadexInstrumentProvider",
    "get_paradex_instrument_provider",
]
