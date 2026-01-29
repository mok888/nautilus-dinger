# nautilus_trader/adapters/paradex/config.py
"""Configuration classes for Paradex adapter."""

from typing import Literal
from nautilus_trader.config import LiveDataClientConfig
from nautilus_trader.config import LiveExecClientConfig


class ParadexDataClientConfig(LiveDataClientConfig, frozen=True):
    """Configuration for ParadexDataClient."""

    environment: Literal["testnet", "mainnet"] = "testnet"
    subkey_private_key: str
    main_account_address: str
    rest_url: str | None = None
    ws_url: str | None = None
    max_reconnection_tries: int = 0
    reconnection_delay_secs: float = 5.0
    ping_interval_secs: float = 30.0


class ParadexExecClientConfig(LiveExecClientConfig, frozen=True):
    """Configuration for ParadexExecutionClient."""

    environment: Literal["testnet", "mainnet"] = "testnet"
    subkey_private_key: str
    main_account_address: str
    rest_url: str | None = None
    timeout_secs: float = 30.0
    max_concurrent_requests: int = 10
    reconcile_interval_secs: float = 300.0
