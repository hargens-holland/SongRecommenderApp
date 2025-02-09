import sqlite3

conn = sqlite3.connect("song_recommender.db")
cursor = conn.cursor()

cursor.execute("SELECT title, artist, year FROM songs LIMIT 10;")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()