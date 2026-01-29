# nautilus_trader/adapters/paradex/factories.py
"""Type conversion factories for Paradex."""

from decimal import Decimal

from nautilus_trader.core.datetime import millis_to_nanos
from nautilus_trader.execution.reports import FillReport
from nautilus_trader.execution.reports import OrderStatusReport
from nautilus_trader.execution.reports import PositionStatusReport
from nautilus_trader.model.enums import LiquiditySide
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.enums import OrderSide as Side
from nautilus_trader.model.enums import OrderStatus
from nautilus_trader.model.enums import OrderType
from nautilus_trader.model.enums import PositionSide
from nautilus_trader.model.identifiers import AccountId
from nautilus_trader.model.identifiers import ClientOrderId
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import Symbol
from nautilus_trader.model.identifiers import TradeId
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.identifiers import VenueOrderId
from nautilus_trader.model.instruments import CryptoPerpetual
from nautilus_trader.model.objects import Money
from nautilus_trader.model.objects import Price
from nautilus_trader.model.objects import Quantity


def parse_instrument(market_data: dict, venue: Venue) -> CryptoPerpetual:
    """Parse Paradex market to Nautilus instrument."""
    return CryptoPerpetual(
        instrument_id=InstrumentId(Symbol(market_data["symbol"]), venue),
        raw_symbol=Symbol(market_data["symbol"]),
        base_currency=market_data["base_currency"],
        quote_currency=market_data["quote_currency"],
        settlement_currency=market_data["quote_currency"],
        is_inverse=False,
        price_precision=len(market_data["price_tick_size"].split(".")[-1]),
        size_precision=len(market_data["quantity_tick_size"].split(".")[-1]),
        price_increment=Price.from_str(market_data["price_tick_size"]),
        size_increment=Quantity.from_str(market_data["quantity_tick_size"]),
        max_quantity=Quantity.from_str(market_data["max_quantity"]),
        min_quantity=Quantity.from_str(market_data["min_quantity"]),
        max_price=None,
        min_price=None,
        margin_init=Decimal("0.1"),
        margin_maint=Decimal("0.05"),
        maker_fee=Decimal("0.0002"),
        taker_fee=Decimal("0.0005"),
        ts_event=0,
        ts_init=0,
    )


def parse_order_status_report(
    order_data: dict,
    instrument: CryptoPerpetual,
    account_id: AccountId,
    clock,
) -> OrderStatusReport:
    """Parse Paradex order to OrderStatusReport."""
    return OrderStatusReport(
        account_id=account_id,
        instrument_id=instrument.id,
        client_order_id=ClientOrderId(order_data.get("client_id", "")),
        venue_order_id=VenueOrderId(order_data["id"]),
        order_side=OrderSide.BUY if order_data["side"] == "BUY" else OrderSide.SELL,
        order_type=OrderType.LIMIT if order_data["type"] == "LIMIT" else OrderType.MARKET,
        time_in_force="GTC",
        order_status=_parse_order_status(order_data["status"]),
        price=Price.from_str(order_data["price"]) if order_data.get("price") else None,
        quantity=Quantity.from_str(order_data["size"]),
        filled_qty=Quantity.from_str(order_data.get("filled_size", "0")),
        ts_accepted=millis_to_nanos(order_data["created_at"]),
        ts_last=millis_to_nanos(order_data["updated_at"]),
        report_id=order_data["id"],
        ts_init=clock.timestamp_ns(),
    )


def parse_fill_report(
    fill_data: dict,
    instrument: CryptoPerpetual,
    account_id: AccountId,
    clock,
) -> FillReport:
    """Parse Paradex fill to FillReport."""
    return FillReport(
        account_id=account_id,
        instrument_id=instrument.id,
        venue_order_id=VenueOrderId(fill_data["order_id"]),
        trade_id=TradeId(fill_data["id"]),
        order_side=OrderSide.BUY if fill_data["side"] == "BUY" else OrderSide.SELL,
        last_qty=Quantity.from_str(fill_data["size"]),
        last_px=Price.from_str(fill_data["price"]),
        commission=Money.from_str(f"{fill_data['fee']} {fill_data['fee_currency']}"),
        liquidity_side=LiquiditySide.MAKER if fill_data["liquidity"] == "MAKER" else LiquiditySide.TAKER,
        ts_event=millis_to_nanos(fill_data["created_at"]),
        report_id=fill_data["id"],
        ts_init=clock.timestamp_ns(),
    )


def parse_position_status_report(
    position_data: dict,
    instrument: CryptoPerpetual,
    account_id: AccountId,
    clock,
) -> PositionStatusReport:
    """Parse Paradex position to PositionStatusReport."""
    side = PositionSide.LONG if position_data["side"] == "LONG" else PositionSide.SHORT
    quantity = Quantity.from_str(position_data["size"])

    return PositionStatusReport(
        account_id=account_id,
        instrument_id=instrument.id,
        position_side=side,
        quantity=quantity,
        quantity_px=None,  # Average entry price
        break_even_price=None,
        realized_pnl=None,
        unrealized_pnl=None,
        total_pnl=None,
        ts_last=millis_to_nanos(position_data["updated_at"]),
        report_id=position_data["id"],
        ts_init=clock.timestamp_ns(),
    )


def _parse_order_status(status: str) -> OrderStatus:
    """Convert Paradex order status to Nautilus."""
    mapping = {
        "PENDING": OrderStatus.SUBMITTED,
        "OPEN": OrderStatus.ACCEPTED,
        "PARTIALLY_FILLED": OrderStatus.PARTIALLY_FILLED,
        "FILLED": OrderStatus.FILLED,
        "CANCELLED": OrderStatus.CANCELED,
        "REJECTED": OrderStatus.REJECTED,
    }
    return mapping.get(status, OrderStatus.PENDING_CANCEL)


def get_paradex_instrument_provider(http_client, clock, logger):
    """Factory function for instrument provider."""
    from nautilus_trader.adapters.paradex.providers import ParadexInstrumentProvider
    return ParadexInstrumentProvider(http_client, clock, logger)
