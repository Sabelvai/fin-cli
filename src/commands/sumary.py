from api import dbapi
from datetime import datetime
from rich.console import Console
from rich.table import Table

def summary():
    current_date = datetime.now()

    processed_date = datetime(current_date.year, current_date.month, current_date.day)

    formated_date_str = processed_date.strftime("%m.%Y")

    income_print = dbapi.summary_read("how_much", "from_source", "incomes", formated_date_str)
    expenses_print = dbapi.summary_read("how_much", "category", "expenses", formated_date_str)

    incomes_list = dbapi.summary_values("how_much", "incomes", formated_date_str)
    expenses_list = dbapi.summary_values("how_much", "expenses", formated_date_str)

    incomes = (sum(sum(sublist) for sublist in incomes_list))
    expenses = (sum(sum(sublist) for sublist in expenses_list))

    profit = incomes - expenses

    dates = dbapi.read("summary", "date")

    if any(formated_date_str in sublist for sublist in dates):
        dbapi.summary_updatedb(incomes, expenses, profit, formated_date_str)
    else:
        dbapi.summary_todb(incomes, expenses, profit, formated_date_str)


    table = Table()

    table.add_column("Incomes")
    table.add_column("Expenses")
    table.add_column("Profit")

    income_sorted = sorted(income_print, key=lambda x: x[0], reverse=True)
    expenses_sorted = sorted(expenses_print, key=lambda x: x[0], reverse=True)

    max_length = max(len(income_sorted), len(expenses_sorted))

    for i in range(max_length):
        row = [
            str(income_sorted[i][0]) + ' ' + str(income_sorted[i][1]) if i < len(income_sorted) else '',
            str(expenses_sorted[i][0]) + ' ' + str(expenses_sorted[i][1]) if i < len(expenses_sorted) else '',
            str(profit) if i == 0 else ''
        ]
        table.add_row(*row)

    console = Console()
    console.print(table)
