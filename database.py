import sqlite3

# Connect to the database
conn = sqlite3.connect('articles.db')
cursor = conn.cursor()

# Create the 'articles' table if it doesn't exist
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

def insert_articles_to_db(articles):
    # Connect to the database
    conn = sqlite3.connect('articles.db')
    cursor = conn.cursor()

    # Insert articles into the database
    for article in articles:
        cursor.execute('''
            INSERT INTO articles (title, link, author, date, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (article['Title'], article['Link'], article['Author'], article['Date'], article['Category']))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def show_articles_from_db():
    # Connect to the database
    conn = sqlite3.connect('articles.db')
    cursor = conn.cursor()

    # Fetch all articles from the database
    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()

    # Print the articles
    for article in articles:
        print("Title:", article[1])
        print("Link:", article[2])
        print("Date:", article[3])
        print("Author:", article[4])
        print("Category:", article[5])
        print("\n")

    # Close the connection
    conn.close()
