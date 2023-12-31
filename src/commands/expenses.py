from api import dbapi
from datetime import datetime
from rich.console import Console

def expense(how_much, category):
    current_date = datetime.now()

    processed_date = datetime(current_date.year, current_date.month, current_date.day)

    formated_date_str = processed_date.strftime("%m.%Y")

    category_list = dbapi.read("expenses", "category")
    date = dbapi.expense_check_date(category)

    console = Console()

    if any(category in sublist for sublist in category_list):
        if (formated_date_str == date in sublist for sublist in date):
            dbapi.expense_update(how_much, category, formated_date_str)
            console.print(f"Added [bold white]{how_much}[/bold white] to [bold white]{category}[/bold white]")
    else:
        dbapi.expense(how_much, category, formated_date_str)
        console.print(f"Created category [bold white]{category}[/bold white] in this month expensed [bold white]{how_much}")
