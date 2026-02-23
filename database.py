import sqlite3

DATABASE = 'mustwatch.db'

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS lista (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            tipo TEXT NOT NULL,
            indicado_por TEXT
        )
    ''')
    conn.commit()
    conn.close()