import sqlite3

con = sqlite3.connect("users.db")

con.execute(
    "create table User ( username TEXT UNIQUE NOT NULL, password PASSWORD NOT NULL)")

con.close()