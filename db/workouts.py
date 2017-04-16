import sqlite3, sys

def addWorkout(name, conn):
  conn.execute('INSERT INTO workouts (name) VALUES ("%s")' % name)

def listWorkouts(conn):
  c = conn.cursor()
  c.execute('SELECT * FROM workouts')
  return c.fetchall()
