import sqlite3

conn = sqlite3.connect('instance/local.db')
cur = conn.cursor()

""" cur.execute("DELETE FROM departments")
cur.execute("DELETE FROM jobs")
cur.execute("DELETE FROM employees")
# Commit the transaction
conn.commit() """

cur.execute("SELECT * FROM departments")
print(cur.fetchall())
cur.execute("SELECT * FROM jobs")
print(cur.fetchall())
cur.execute("SELECT * FROM employees")
print(cur.fetchall())

conn.close()
