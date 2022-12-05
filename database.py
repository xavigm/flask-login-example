import sqlite3
from sqlite3 import Error

def create_new_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        conn.execute('''CREATE TABLE settings
                (USER            BLOB NOT NULL,
                PASSWORD         BLOB NOT NULL,
                EMAIL         BLOB NOT NULL
                );''') #Creates the table
        conn.commit() # Commits the entries to the database
        conn.execute('''INSERT INTO settings VALUES ("admin","admin","test@test.com")''')
        conn.commit() # Commits the entries to the database

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            


def selectUser():

    conn = sqlite3.connect(r"pythonsqlite.db")
    try:
        cur = conn.cursor()
        rows= cur.execute('''SELECT USER,PASSWORD FROM settings''').fetchone()

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

    print(rows)
    return '{"'+str(rows[0])+'": {"password": "'+str(rows[1])+'"}}'