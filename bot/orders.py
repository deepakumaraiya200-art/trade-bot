import logging
from typing import Optional
from bot.client import BinanceFuturesClient, BinanceClientError
from bot.validators import validate_order_input, ValidationError

logger = logging.getLogger("trading_bot")


def place_order(client, symbol, side, order_type, quantity, price=None):
    validated = validate_order_input(symbol, side, order_type, quantity, price)
    logger.info(
        f"Order request  → symbol={validated['symbol']}  side={validated['side']}  "
        f"type={validated['order_type']}  qty={validated['quantity']}  price={validated['price']}"
    )
    response = client.place_order(
        symbol=validated["symbol"], side=validated["side"],
        order_type=validated["order_type"], quantity=validated["quantity"],
        price=validated["price"],
    )
    order_id = response.get("orderId")
    status = response.get("status")
    executed_qty = response.get("executedQty")
    avg_price = response.get("avgPrice", "N/A")
    logger.info(
        f"Order response ← orderId={order_id}  status={status}  "
        f"executedQty={executed_qty}  avgPrice={avg_price}"
    )
    return response


def format_order_result(response):
    lines = [
        "┌─────────────── Order Result ───────────────┐",
        f"│  Order ID      : {response.get('orderId')}",
        f"│  Symbol        : {response.get('symbol')}",
        f"│  Side          : {response.get('side')}",
        f"│  Type          : {response.get('type')}",
        f"│  Status        : {response.get('status')}",
        f"│  Quantity       : {response.get('origQty')}",
        f"│  Executed Qty  : {response.get('executedQty')}",
        f"│  Avg Price     : {response.get('avgPrice', 'N/A')}",
        f"│  Time In Force : {response.get('timeInForce', 'N/A')}",
        "└────────────────────────────────────────────┘",
    ]
    return "\n".join(lines)
