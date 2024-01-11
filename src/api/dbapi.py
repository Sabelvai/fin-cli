import sqlite3

con = sqlite3.connect("data/finance.db")
cur = con.cursor()

def create_table():
    cur.execute('''CREATE TABLE IF NOT EXISTS incomes
                        (from_source TEXT, how_much INTEGER, date TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS expenses
                (how_much INTEGER, category TEXT, date TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS summary
                (incomes INTEGER, expenses INTEGER, profit INTAGER, date TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS currencies
                (what_curerency TEXT, how_much INTEGER, prushpare_price FLOAT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS blackday
                (how_much INTEGER)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS savings
                (goal TEXT, how_much_collected INTEGER, how_much_need INTEGER)''')

def income(from_source, how_much, date):
    cur.execute(f"INSERT INTO incomes VALUES ('{from_source}','{how_much}','{date}')")
    con.commit()

def expense(how_much, category, date):
    cur.execute(f"INSERT INTO expenses VALUES ('{how_much}','{category}','{date}')")
    con.commit()

def modify(table, column, new_value, old_value):
    cur.execute(f'UPDATE {table} SET {column} = ? WHERE {column} = ?', (new_value, old_value))
    con.commit()

def read(table, column):
    rows = cur.execute(f"SELECT {column} FROM {table}").fetchall()
    result_list = [list(row) for row in rows]
    return result_list

def expense_update(new_value, category, date):
    cur.execute(f"UPDATE expenses SET how_much = how_much + ? WHERE category = ? AND date = ?", (new_value, category, date,))
    con.commit()

def expense_check_date(category):
    rows = cur.execute(f"SELECT date FROM expenses WHERE category = ?", (category,)).fetchall()
    return rows

def delete(table, column, data):
    cur.execute(f"DELETE FROM {table} WHERE {column} = '{data}'")
    con.commit()

def summary_read(column, column2, table, date):
    rows = cur.execute(f"SELECT {column} , {column2} FROM {table} WHERE date = ?", (date,)).fetchall()
    return rows

def summary_values(column, table, date):
    rows = cur.execute(f"SELECT {column} FROM {table} WHERE date = ?", (date,)).fetchall()
    return rows

def summary_todb(incomes, expenses, profit, date):
    cur.execute(f"INSERT INTO summary VALUES ('{incomes}','{expenses}','{profit}','{date}')")
    con.commit()

def summary_updatedb(incomes, expenses, profit, date):
    cur.execute(f"UPDATE summary SET incomes = ?, expenses = ?, profit = ? WHERE date = ?", (incomes, expenses, profit, date,))
    con.commit()

def currencies(what_curerency, how_much, prushpare_price):
    cur.execute(f"INSERT INTO currencies VALUES ('{what_curerency}','{how_much}','{prushpare_price}')")
    con.commit()

def currencies_increase(what_curerency):
    rows = cur.execute(f"SELECT prushpare_price, how_much FROM currencies WHERE what_curerency = ?", (what_curerency,)).fetchall()
    return rows

def blackday(how_much):
    cur.execute(f"SELECT how_much FROM blackday")

    result = cur.fetchone()

    if result:
        cur.execute(f"UPDATE blackday SET how_much = how_much + ?", (how_much,))
        con.commit()
    else:
        cur.execute(f"INSERT INTO blackday VALUES ({how_much})")
        con.commit()

def take_blackday(how_much):
    cur.execute(f"UPDATE blackday SET how_much = how_much - ?", (how_much,))
    con.commit()

def create_goal(goal, how_much_need):
    cur.execute(f"INSERT INTO savings VALUES ('{goal}', '0', '{how_much_need}')")
    con.commit()

def add_goal(goal, how_much_to_add):
    cur.execute(f"UPDATE savings SET how_much_collected = how_much_collected + ? WHERE goal = ?", (how_much_to_add, goal))
    con.commit()

def check_goal(goal):
    rows = cur.execute(f"SELECT how_much_collected, how_much_need FROM savings WHERE goal = ?", (goal,)).fetchall()
    return rows
