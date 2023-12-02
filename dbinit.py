import sqlite3

# Connect to SQLite DB (it will create the file if it doesn't exist)
conn = sqlite3.connect('./db/database.db')

# Create a table
conn.execute('''
    CREATE TABLE IF NOT EXISTS uploads (
        id INTEGER PRIMARY KEY,
        filename TEXT,
        filepath TEXT,
        filesize INTEGER,
        uploadtime DATETIME
    )
''')

# Commit changes and close connection
conn.commit()
conn.close()