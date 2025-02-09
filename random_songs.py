import sqlite3
import random

def get_random_songs(num_songs=10):
    """Fetch and print a random selection of songs from the database."""
    conn = sqlite3.connect("../song_recommender.db")
    cursor = conn.cursor()

    # Get total number of songs
    cursor.execute("SELECT COUNT(*) FROM songs")
    total_songs = cursor.fetchone()[0]

    if total_songs == 0:
        print("❌ No songs found in the database!")
        conn.close()
        return

    # Select 10 random songs
    cursor.execute("SELECT title, artist FROM songs ORDER BY RANDOM() LIMIT ?", (num_songs,))
    random_songs = cursor.fetchall()

    conn.close()

    print("\n🎵 **Random Songs:**")
    for idx, (title, artist) in enumerate(random_songs, start=1):
        print(f"{idx}. {title} - {artist}")

# Run the script
if __name__ == "__main__":
    get_random_songs()