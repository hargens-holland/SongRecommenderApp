import sqlite3

conn = sqlite3.connect("../song_recommender.db")
cursor = conn.cursor()

# Search for "Backbone" in the songs table
cursor.execute("SELECT title, artist FROM songs WHERE LOWER(title) LIKE LOWER('%Backbone%')")
results = cursor.fetchall()

conn.close()

if results:
    print("✅ 'Backbone' found in database:")
    for title, artist in results:
        print(f"Title: {title}, Artist: {artist}")
else:
    print("❌ 'Backbone' NOT found in database!")

cursor.execute("SELECT title, artist FROM songs WHERE title LIKE ?", ('%BACKBONE%',))
results = cursor.fetchall()
print("Found matches:", results)