from api import dbapi
from rich.console import Console

def currencies(what_curerency, how_much, prushpare_price):
    dbapi.currencies(what_curerency, how_much, prushpare_price)

    console = Console()
    console.print(f"[white bold]{how_much} {what_curerency}[/white bold] added with prushpare price [bold white]{prushpare_price}[/bold white]")
