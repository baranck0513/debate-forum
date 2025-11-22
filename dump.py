import sqlite3
db = sqlite3.connect('debate.sqlite')
with open("dump.sql", "w") as f:
    for line in db.iterdump():
        f.write(line + '\n')