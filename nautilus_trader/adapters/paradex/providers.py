# nautilus_trader/adapters/paradex/providers.py
"""Instrument provider for Paradex exchange."""

from typing import Any

from nautilus_trader.common.component import LiveClock
from nautilus_trader.common.component import Logger
from nautilus_trader.core.correctness import PY_PREV
from nautilus_trader.model.identifiers import InstrumentId


class ParadexInstrumentProvider:
    """
    Instrument provider for Paradex.

    Fetches and caches market instruments from REST API.
    """

    def __init__(
        self,
        http_client: Any,
        clock: LiveClock,
        logger: Logger,
    ) -> None:
        self._http = http_client
        self._clock = clock
        self._log = logger

        self._instruments: dict[InstrumentId, Any] = {}

    async def initialize(self) -> None:
        """Initialize instrument provider by fetching all markets."""
        self._log.info("Initializing Paradex instrument provider...")

        try:
            markets = await self._http.get_markets()

            for market_data in markets:
                from nautilus_trader.adapters.paradex.factories import parse_instrument
                from nautilus_trader.adapters.paradex.constants import PARADEX

                instrument = parse_instrument(market_data, PARADEX)
                self._instruments[instrument.id] = instrument

            self._log.info(f"Loaded {len(self._instruments)} instruments")
        except Exception as e:
            self._log.error(f"Failed to initialize instruments: {e}")
            raise

    def find_instrument(self, instrument_id: InstrumentId) -> Any:
        """Find instrument by ID."""
        return self._instruments.get(instrument_id)

    def list_all(self) -> list[Any]:
        """List all instruments."""
        return list(self._instruments.values())
