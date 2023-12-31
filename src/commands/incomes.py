from api import dbapi
from commands import expenses
from datetime import datetime
from rich.console import Console
from rich.style import Style


def incomes(from_source2, how_much):

    current_date = datetime.now()
    processed_date = datetime(current_date.year, current_date.month, current_date.day)
    formated_date_str = processed_date.strftime("%m.%Y")


    blackday_procent = (15 / 100) * how_much


    dbapi.income(from_source2, how_much, formated_date_str)
    dbapi.blackday(round(blackday_procent))
    expenses.expense(round(blackday_procent), "blackday")

    console = Console()
    console.print(f"Receiving from a [bold white]{from_source2}[/bold white] with an amount of {how_much}")
    console.print(f"Automatically postponed to a [bold black]black day[/bold black] 15% ({round(blackday_procent)})")
