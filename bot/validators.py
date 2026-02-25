from typing import Optional

VALID_SIDES = ("BUY", "SELL")
VALID_ORDER_TYPES = ("MARKET", "LIMIT")


class ValidationError(Exception):
    """Raised when user input fails validation."""
    pass


def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if not symbol:
        raise ValidationError("Symbol cannot be empty.")
    if len(symbol) < 2 or not symbol.isalpha():
        raise ValidationError(f"Invalid symbol '{symbol}'. Must be alphabetic (e.g., BTCUSDT).")
    return symbol


def validate_side(side: str) -> str:
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValidationError(f"Invalid side '{side}'. Must be one of {VALID_SIDES}.")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(f"Invalid order type '{order_type}'. Must be one of {VALID_ORDER_TYPES}.")
    return order_type


def validate_quantity(quantity: float) -> float:
    if quantity <= 0:
        raise ValidationError(f"Invalid quantity '{quantity}'. Must be a positive number.")
    return quantity


def validate_price(price: Optional[float], order_type: str) -> Optional[float]:
    if order_type == "LIMIT":
        if price is None or price <= 0:
            raise ValidationError("Price is required and must be positive for LIMIT orders.")
    return price


def validate_order_input(symbol, side, order_type, quantity, price=None) -> dict:
    return {
        "symbol": validate_symbol(symbol),
        "side": validate_side(side),
        "order_type": validate_order_type(order_type),
        "quantity": validate_quantity(quantity),
        "price": validate_price(price, order_type.strip().upper()),
    }
