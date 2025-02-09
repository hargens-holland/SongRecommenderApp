import sqlite3

# Connect to database (creates it if it doesn’t exist)
conn = sqlite3.connect("song_recommender.db")
cursor = conn.cursor()

# Create songs table with UNIQUE constraint
cursor.execute('''
CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    year INTEGER,
    genre TEXT,
    popularity INTEGER,
    ranking INTEGER,
    lyrics TEXT,
    bpm REAL,
    energy REAL,
    danceability REAL,
    loudness REAL,
    liveness REAL,
    valence REAL,
    speechiness REAL,
    acousticness REAL,
    instrumentalness REAL,
    mode INTEGER,
    key INTEGER,
    time_signature INTEGER,
    duration REAL,
    spotify_url TEXT,
    deezer_url TEXT,
    UNIQUE (title, artist, year) ON CONFLICT REPLACE
);
''')

conn.commit()
conn.close()

print("✅ Database and table created successfully!")
