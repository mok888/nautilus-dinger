# nautilus_trader/adapters/paradex/constants.py
"""Paradex adapter constants."""

from enum import Enum
from nautilus_trader.model.identifiers import Venue


class Environment(str, Enum):
    """Paradex environment."""

    TESTNET = "testnet"
    MAINNET = "mainnet"


PARADEX = Venue("PARADEX")

PARADEX_TESTNET_HTTP_URL = "https://api.testnet.paradex.trade"
PARADEX_MAINNET_HTTP_URL = "https://api.paradex.trade"
PARADEX_TESTNET_WS_URL = "wss://ws.testnet.paradex.trade/v1"
PARADEX_MAINNET_WS_URL = "wss://ws.paradex.trade/v1"

DEFAULT_RECONCILE_INTERVAL_SECS = 300  # 5 minutes
