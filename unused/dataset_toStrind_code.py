import sqlite3

con = sqlite3.connect("Dataset/dataset.sql")
cur = con.cursor()

for res in cur.execute("SELECT * FROM posts").fetchall():
    print(res)