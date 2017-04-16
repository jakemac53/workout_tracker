import sqlite3, sys

def setupDb():
    conn = sqlite3.connect('db/workouts.sqldb')
    conn.execute('''CREATE TABLE IF NOT EXISTS workouts (name text)''')

    return conn
