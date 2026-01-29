# nautilus_trader/adapters/paradex/__init__.py
"""Paradex adapter for Nautilus Trader."""

from nautilus_trader.adapters.paradex.config import ParadexConfig
from nautilus_trader.adapters.paradex.config import ParadexExecClientConfig
from nautilus_trader.adapters.paradex.constants import PARADEX

__all__ = [
    "PARADEX",
    "ParadexConfig",
    "ParadexExecClientConfig",
]
