from api import dbapi
from datetime import datetime
from rich.console import Console

def expense(how_much, category, date=None):
    current_date = datetime.now()
    processed_date = datetime(current_date.year, current_date.month, current_date.day)
    formated_date_str = date or processed_date.strftime("%m.%Y")

    category_list = dbapi.read("expenses", "category")
    all_dates_for_category = dbapi.expense_check_date(category)

    console = Console()

    if any(formated_date_str in dates for dates in all_dates_for_category):
        # Category and date exist, update the expense
        dbapi.expense_update(how_much, category, formated_date_str)
        console.print(f"Added [bold white]{how_much}[/bold white] to [bold white]{category}[/bold white] for [bold white]{formated_date_str}[/bold white]")
    else:
        # Check if the category exists
        if any(category in sublist for sublist in category_list):
            # Category exists, but the date doesn't, create a new entry
            dbapi.expense(how_much, category, formated_date_str)
            console.print(f"Created category [bold white]{category}[/bold white] and expensed [bold white]{how_much}[/bold white] for [bold white]{formated_date_str}[/bold white]")
        else:
            console.print(f"Category [bold white]{category}[/bold white] does not exist. Please create the category first.")
