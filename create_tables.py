import sqlite3

DB_NAME = "movies.db"

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

# Create users table 
c.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                hash TEXT NOT NULL
            )""")

# Create movies table
c.execute("""CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                year INTEGER,
                poster_path TEXT,
                genres TEXT,
                director TEXT
            )""")

# Create watchlist table
c.execute("""CREATE TABLE IF NOT EXISTS watchlist (
                user_id INTEGER NOT NULL,
                movie_id INTEGER NOT NULL,
                rating INTEGER CHECK(rating >= 1 AND rating <= 10),
                PRIMARY KEY(user_id, movie_id),
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(movie_id) REFERENCES movies(id)
            )""")

# Safely add genres column if it doesn't exist
try:
    c.execute("ALTER TABLE movies ADD COLUMN genres TEXT")
    print("Added 'genres' column.")
except sqlite3.OperationalError:
    pass

conn.commit()
conn.close()

print("Database tables ready!")
