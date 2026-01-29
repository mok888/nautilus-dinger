# nautilus_trader/adapters/paradex/providers.py
"""InstrumentProvider for Paradex."""

from typing import Any

from nautilus_trader.common.component import LiveClock
from nautilus_trader.common.component import Logger
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.instruments import InstrumentAny

from nautilus_trader.adapters.paradex.constants import PARADEX
from nautilus_trader.adapters.paradex.factories import parse_instrument


class ParadexInstrumentProvider:
    """Provides instruments from Paradex."""

    def __init__(self, http_client: Any, clock: LiveClock, logger: Logger) -> None:
        self._http = http_client
        self._clock = clock
        self._log = logger
        self._cache: dict[InstrumentId, InstrumentAny] = {}

    async def load_all_async(self, filters: dict[str, Any] | None = None) -> None:
        """Load all instruments."""
        self._log.info("Loading all instruments...")
        markets = await self._http.get_markets()
        for market in markets:
            instrument = parse_instrument(market, PARADEX)
            self._cache[instrument.id] = instrument
        self._log.info(f"Loaded {len(self._cache)} instruments")

    async def load_ids_async(
        self,
        instrument_ids: list[InstrumentId],
        filters: dict[str, Any] | None = None,
    ) -> None:
        """Load specific instruments."""
        await self.load_all_async(filters)
        self._cache = {k: v for k, v in self._cache.items() if k in instrument_ids}

    async def load_async(
        self,
        instrument_id: InstrumentId,
        filters: dict[str, Any] | None = None,
    ) -> None:
        """Load single instrument."""
        await self.load_ids_async([instrument_id], filters)

    def list_all(self) -> list[InstrumentAny]:
        """List all cached instruments."""
        return list(self._cache.values())

    def find(self, instrument_id: InstrumentId) -> InstrumentAny | None:
        """Find instrument by ID."""
        return self._cache.get(instrument_id)
