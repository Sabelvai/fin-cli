from api import dbapi
from datetime import datetime
from rich.console import Console
from rich.table import Table

def summary(date=None):
    current_date = datetime.now()
    processed_date = datetime(current_date.year, current_date.month, current_date.day)
    formated_date_str = date or processed_date.strftime("%m.%Y")

    income_print = dbapi.summary_read("how_much", "from_source", "incomes", formated_date_str)
    expenses_print = dbapi.summary_read("how_much", "category", "expenses", formated_date_str)

    incomes_list = dbapi.summary_values("how_much", "incomes", formated_date_str)
    expenses_list = dbapi.summary_values("how_much", "expenses", formated_date_str)

    total_income = sum(sum(sublist) for sublist in incomes_list)
    total_expenses = sum(sum(sublist) for sublist in expenses_list)

    profit = total_income - total_expenses

    dates = dbapi.read("summary", "date")

    if any(formated_date_str in sublist for sublist in dates):
        dbapi.summary_updatedb(total_income, total_expenses, profit, formated_date_str)
    else:
        dbapi.summary_todb(total_income, total_expenses, profit, formated_date_str)

    table = Table()

    table.add_column("Incomes", style="green", justify="left")
    table.add_column("Expenses", style="red", justify="center")
    table.add_column("Expense Percentage", style="red", justify="left")
    table.add_column("Profit", style="bold", justify="right")
    table.add_column("Profit Percentage", style="bold", justify="left")

    income_sorted = sorted(income_print, key=lambda x: x[0], reverse=True)
    expenses_sorted = sorted(expenses_print, key=lambda x: x[0], reverse=True)

    max_length = max(len(income_sorted), len(expenses_sorted))

    for i in range(max_length):
        income_value = income_sorted[i][0] if i < len(income_sorted) else 0
        expense_value = expenses_sorted[i][0] if i < len(expenses_sorted) else 0

        expense_percentage = (expense_value / total_expenses) * 100 if total_expenses != 0 else 0
        profit_percentage = (profit / total_income) * 100 if total_income != 0 else 0

        row = [
            f"{income_value} {income_sorted[i][1]}" if i < len(income_sorted) else '',
            f"{expense_value} {expenses_sorted[i][1]}" if i < len(expenses_sorted) else '',
            f"{round(expense_percentage, 2)}%" if i < len(expenses_sorted) else '',
            f"{round(profit, 2)}" if i == 0 else '',
            f"{round(profit_percentage, 2)}%" if i == 0 else ''
        ]
        table.add_row(*row)

    console = Console()
    console.print(table)
