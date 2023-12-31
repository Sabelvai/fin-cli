import sqlite3
from api import dbapi
from rich.console import Console
from rich.progress import Progress

console = Console()

console.print('''
    _______       ______            __             __   ___
   / ____(_)___  / ____/___  ____  / /__________  / /  <  /
  / /_  / / __ \/ /   / __ \/ __ \/ __/ ___/ __ \/ /   / /
 / __/ / / / / / /___/ /_/ / / / / /_/ /  / /_/ / /___/ /
/_/   /_/_/ /_/\____/\____/_/ /_/\__/_/   \____/_____/_/

''',style="bold italic", justify="center")

with Progress(transient=False) as progress:
    task = progress.add_task("Creating database", total=4)

    progress.advance(task)
    con = sqlite3.connect("data/finance.db")
    progress.advance(task)
    cur = con.cursor()
    progress.advance(task)
    dbapi.create_table()
    progress.advance(task)

console.print("Hi welcome to Finance Control Command Line 1nterface (FinCL1)")
console.print("TRY python main.py --help")
