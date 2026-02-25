#!/usr/bin/env python3
import os
import sys
import typer
from dotenv import load_dotenv
from rich import print as rprint
from rich.panel import Panel
from bot.logging_config import setup_logging
from bot.client import BinanceFuturesClient, BinanceClientError
from bot.orders import place_order, format_order_result
from bot.validators import ValidationError

load_dotenv()

app = typer.Typer(
    name="trading-bot",
    help="Simplified Trading Bot for Binance Futures Testnet (USDT-M)",
    add_completion=False,
)


@app.command()
def order(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading pair symbol (e.g. BTCUSDT)"),
    side: str = typer.Option(..., "--side", help="Order side: BUY or SELL"),
    order_type: str = typer.Option(..., "--type", "-t", help="Order type: MARKET or LIMIT"),
    quantity: float = typer.Option(..., "--quantity", "-q", help="Order quantity"),
    price: float = typer.Option(None, "--price", "-p", help="Order price (required for LIMIT)"),
):
    logger = setup_logging()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        rprint("[bold red]Error:[/bold red] BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env")
        logger.error("Missing API credentials in environment.")
        raise typer.Exit(code=1)

    rprint(Panel(
        f"[bold]Symbol:[/bold]     {symbol}\n"
        f"[bold]Side:[/bold]       {side}\n"
        f"[bold]Type:[/bold]       {order_type}\n"
        f"[bold]Quantity:[/bold]   {quantity}\n"
        f"[bold]Price:[/bold]      {price if price else 'N/A (MARKET)'}",
        title="📋 Order Request", border_style="cyan",
    ))

    try:
        client = BinanceFuturesClient(api_key, api_secret)
        client.ping()
        logger.info("Ping successful — connected to Binance Futures Testnet.")
        response = place_order(client=client, symbol=symbol, side=side,
                               order_type=order_type, quantity=quantity, price=price)
        result_text = format_order_result(response)
        rprint(Panel(result_text, title="✅ Order Placed Successfully", border_style="green"))
        logger.info("Order placed successfully.")
    except ValidationError as ve:
        rprint(f"[bold red]Validation Error:[/bold red] {ve}")
        logger.error(f"Validation error: {ve}")
        raise typer.Exit(code=1)
    except BinanceClientError as bce:
        rprint(f"[bold red]API Error:[/bold red] {bce}")
        logger.error(f"Binance API error: {bce}")
        raise typer.Exit(code=1)
    except Exception as exc:
        rprint(f"[bold red]Unexpected Error:[/bold red] {exc}")
        logger.exception(f"Unexpected error: {exc}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
