from api import dbapi
from rich.console import Console
from rich.table import Table


def read_goals():
    goals = dbapi.read("savings","*")

    console = Console()

    table = Table()

    table.add_column("Goal", style="bold",justify="left")
    table.add_column("How Much Collected",justify="center")
    table.add_column("How Much Need", justify="right")

    for row in goals:
        table.add_row(str(row[0]), str(row[1]), str(row[2]))

    console.print(table)
