# nautilus_trader/adapters/paradex/constants.py
"""Constants for Paradex adapter."""

from nautilus_trader.model.identifiers import Venue

PARADEX = Venue("PARADEX")

PARADEX_TESTNET_REST_URL = "https://api.testnet.paradex.trade/v1"
PARADEX_TESTNET_WS_URL = "wss://ws.testnet.paradex.trade/v1"
PARADEX_MAINNET_REST_URL = "https://api.prod.paradex.trade/v1"
PARADEX_MAINNET_WS_URL = "wss://ws.prod.paradex.trade/v1"

PARADEX_TESTNET_CHAIN_ID = "PRIVATE_SN_POTC_SEPOLIA"
PARADEX_MAINNET_CHAIN_ID = "SN_MAIN"

DEFAULT_TIMEOUT_SECS = 30.0
DEFAULT_RECONCILE_INTERVAL_SECS = 300.0
DEFAULT_PING_INTERVAL_SECS = 30.0
MAX_CONCURRENT_REQUESTS = 10
