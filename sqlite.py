import sqlite3
from random import randint


db = sqlite3.connect('serv.db')
sql = db.cursor()


def reg(user_id):
    sql.execute("""CREATE TABLE IF NOT EXISTS users (
        login TEXT,
        cash BIGINT,
        source INT 
    )""")
    db.commit()

    users_login = user_id

    sql.execute(f"SELECT login FROM users WHERE login = '{users_login}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES (?, ?, ?)", (users_login, 1000, 1))
        db.commit()
    else:
        pass


def win_in_casino(user_id, user_bet):
    reg(user_id)
    for i in sql.execute(f"SELECT cash FROM users WHERE login = '{user_id}'"):
        balance = i[0]
    sql.execute(f"UPDATE users SET cash = {int(user_bet) + balance} WHERE login = '{user_id}'")
    db.commit()


def lose_in_casino(user_id, user_bet):
    reg(user_id)
    for i in sql.execute(f"SELECT cash FROM users WHERE login = '{user_id}'"):
        balance = i[0]
    sql.execute(f"UPDATE users SET cash = {balance - int(user_bet)} WHERE login = '{user_id}'")
    db.commit()


def gift_of_casino(user_id, gift_sum):
    for i in sql.execute(f"SELECT cash FROM users WHERE login = '{user_id}'"):
        balance = i[0]
    sql.execute(f"UPDATE users SET cash = {balance + gift_sum} WHERE login = '{user_id}'")


def enter(user_id):
    for i in sql.execute(f"SELECT login, cash FROM users WHERE login = '{user_id}'"):
        return i[1]


def enter_source(user_id):
    for i in sql.execute(f"SELECT login, source FROM users WHERE login = '{user_id}'"):
        balance = i[1]
        return balance


def new_source(user_id, source):
    sql.execute(f"UPDATE users SET source = {source} WHERE login = '{user_id}'")

