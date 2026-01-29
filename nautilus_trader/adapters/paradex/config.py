# nautilus_trader/adapters/paradex/config.py
"""Paradex adapter configuration."""

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from nautilus_trader.adapters.paradex.constants import Environment
from nautilus_trader.adapters.paradex.constants import PARADEX_TESTNET_HTTP_URL
from nautilus_trader.adapters.paradex.constants import PARADEX_TESTNET_WS_URL
from nautilus_trader.adapters.paradex.constants import DEFAULT_RECONCILE_INTERVAL_SECS


@dataclass
class ParadexConfig:
    """Configuration for Paradex adapter."""

    environment: Environment = Environment.TESTNET
    api_key: str = ""
    api_secret: str = ""
    l2_address: str = ""
    subkey_private_key: str = ""

    http_url: str = field(init=False)
    ws_url: str = field(init=False)

    def __post_init__(self) -> None:
        if self.environment == Environment.TESTNET:
            self.http_url = PARADEX_TESTNET_HTTP_URL
            self.ws_url = PARADEX_TESTNET_WS_URL
        else:
            self.http_url = "https://api.paradex.trade"
            self.ws_url = "wss://ws.paradex.trade/v1"


@dataclass
class ParadexExecClientConfig:
    """Configuration for Paradex execution client."""

    reconcile_interval_secs: int = DEFAULT_RECONCILE_INTERVAL_SECS
    account_id: str = "PARADEX"

    # STARK signing configuration
    use_rust_signer: bool = True  # Use Rust-based STARK signer
    stark_chain_id: str = "SN_SEPOLIA"  # Testnet chain ID

    # HTTP client configuration
    http_timeout_secs: int = 30
    http_max_retries: int = 3
    http_retry_delay_secs: float = 1.0

    # WebSocket configuration
    ws_ping_interval_secs: int = 30
    ws_ping_timeout_secs: int = 10
    ws_max_reconnect_attempts: int = 5
    ws_reconnect_delay_secs: float = 5.0
