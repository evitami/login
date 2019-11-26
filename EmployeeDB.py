import sqlite3

con = sqlite3.connect("employee.db")

con.execute(
    "create table Employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, password PASSWORD NOT NULL)")

con.close()