import sqlite3

conn = sqlite3.connect('articles.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY,
        title TEXT,
        link TEXT,
        author TEXT,
        date TEXT,
        category TEXT
    )
''')

conn.commit()
conn.close()