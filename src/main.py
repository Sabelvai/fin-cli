from api import dbapi, currency_check
from commands import incomes, expenses, sumary, currency_add, add_goal, read_goals, remove_goal
import typer
from rich.console import Console
import sqlite3
import firstrun
from typing import Optional

app = typer.Typer()
console = Console()

@app.command()
def income(from_source: str, how_much: int, blackday_percent: int, date: Optional[str] = None):
    '''insert your income'''
    if date:
        incomes.incomes(from_source, how_much, blackday_percent, date)
    else:
        incomes.incomes(from_source, how_much, blackday_percent)

@app.command()
def expense(how_much: int, category: str, date: Optional[str] = None):
    '''insert your expense'''
    expenses.expense(how_much, category, date)

@app.command()
def summary(date: Optional[str] = None):
    '''summary of incomes/expenses'''
    sumary.summary(date)

@app.command()
def read(table: str, column: str):
    '''read info from db'''
    print(dbapi.read(table, column))

@app.command()
def deletedb(table: str, column: str, value):
    '''delete value from db'''
    dbapi.delete(table, column, value)
    console.print("info deleted")

@app.command()
def currency(what_curerency: str, how_much: int, prushpare_price: float):
    '''add currency'''
    currency_add.currencies(what_curerency, how_much, prushpare_price)

@app.command()
def modifydb(table: str, column: str, new_value, old_value):
    '''modify database value'''
    dbapi.modify(table, column, new_value, old_value)
    console.print("data modified")

@app.command()
def curcheck(source_currency: str, destination_currency: str):
        '''check your currency price and increase'''
        currency_list = dbapi.currencies_increase(source_currency)

        for sublist_index, sublist in enumerate(currency_list, start=1):
            if len(sublist) == 2:
                list_value1, list_value2 = sublist
                currency_check.check(source_currency,destination_currency,list_value2,list_value1)

@app.command()
def blackday(how_much: int):
    '''add value to blackday savings'''
    dbapi.blackday(how_much)
    expenses.expense(how_much, "blackday")

@app.command()
def creategoal(goal: str, how_much_need: int):
    """
    create saving goal
    """
    dbapi.create_goal(goal, how_much_need)

@app.command()
def addgoal(goal: str, how_much_to_add: int):
    """
    add value to goal
    """
    add_goal.add_goal(goal, how_much_to_add)

@app.command()
def readgoals():
    """
    read goals
    """
    read_goals.read_goals()

@app.command()
def delgoals(goal: str):
    """
    delete goal
    """
    remove_goal.remove_goals(goal)

@app.command()
def takeblackday(how_much: int):
    """
    take money from blackday
    """
    dbapi.take_blackday(how_much)
    incomes.incomes("blackday", how_much, 0)


def check_for_first_run():
    db_path = "data/finance.db"

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    try:
        cur.execute("SELECT * FROM incomes LIMIT 1")
    except sqlite3.OperationalError:
        firstrun.firstrun()

if __name__ == "__main__":
    check_for_first_run()
    app()
