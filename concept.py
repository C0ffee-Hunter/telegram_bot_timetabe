import sqlite3

conn = sqlite3.connect("etu_table.db", check_same_thread=False)
conn.execute("pragma journal_mode=wal;")
c = conn.cursor()
c.execute(
        '''CREATE TABLE test (id integer primary key, user_id integer, user_name text, user_surname text, username text)''')
conn.commit()
conn.close()