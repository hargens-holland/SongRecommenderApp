import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("../song_recommender.db")
# Add this debug code

# Load songs and select useful features
query = """
SELECT title, artist, bpm, energy, danceability, loudness, valence, acousticness, speechiness, instrumentalness
FROM songs
WHERE bpm IS NOT NULL
"""
df = pd.read_sql_query(query, conn)

conn.close()

# Display first few rows
print(df.head())

# Save data for use in the recommendation system
df.to_csv("song_features.csv", index=False)
print("✅ Song features extracted and saved!")

from sklearn.preprocessing import MinMaxScaler

# Drop non-numeric columns for scaling
features = df.drop(columns=["title", "artist"])

# Normalize using MinMaxScaler (scales everything between 0 and 1)
scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(features)

# Convert back to DataFrame
df_scaled = pd.DataFrame(scaled_features, columns=features.columns)

# Add back title and artist
df_scaled.insert(0, "title", df["title"])
df_scaled.insert(1, "artist", df["artist"])

# Save processed data
df_scaled.to_csv("processed_song_features.csv", index=False)
print("✅ Song data preprocessed and normalized!")

from sklearn.metrics.pairwise import cosine_similarity

# Compute cosine similarity between all songs
similarity_matrix = cosine_similarity(scaled_features)

# Convert to DataFrame for easy lookup
similarity_df = pd.DataFrame(similarity_matrix, index=df["title"], columns=df["title"])


def recommend_songs(song_title, num_recommendations=5):
    """Finds similar songs based on features and displays both title & artist."""

    try:
        # Parse input for title and artist
        if " by " in song_input.lower():
            title, artist = song_input.split(" by ", 1)
            title = title.strip()
            artist = artist.strip()

            # Connect to database
            conn = sqlite3.connect("../song_recommender.db")
            cursor = conn.cursor()

            # Search for exact match with both title and artist
            cursor.execute("""
                        SELECT title, artist 
                        FROM songs 
                        WHERE LOWER(title) = LOWER(?) 
                        AND LOWER(artist) = LOWER(?)
                    """, (title, artist))
        else:
            # If no artist specified, just search by title
            title = song_input
            conn = sqlite3.connect("../song_recommender.db")
            cursor = conn.cursor()
            cursor.execute("""
                        SELECT title, artist 
                        FROM songs 
                        WHERE LOWER(title) = LOWER(?)
                    """, (title,))
        # Open connection
        conn = sqlite3.connect("../song_recommender.db")
        cursor = conn.cursor()

        # Search for the exact song in the database
        cursor.execute("SELECT title, artist FROM songs WHERE LOWER(title) = LOWER(?)", (song_title,))
        song_rows = cursor.fetchall()  # Get all matches, not just one

        if not song_rows:
            print(f"❌ Song '{song_title}' not found in database!")
            return []

        # If multiple matches, let user specify which artist
        if len(song_rows) > 1:
            print("\nMultiple matches found:")
            for i, (title, artist) in enumerate(song_rows):
                print(f"{i + 1}. '{title}' by {artist}")
            print("\nPlease specify which version by including the artist name")
            return []

        song_title, song_artist = song_rows[0]  # Take first match if only one
        print(f"🎵 Searching for similar songs to '{song_title}' by {song_artist}...")

        # Fetch song features from database
        query = """
            SELECT title, artist, bpm, energy, danceability, loudness, valence 
            FROM songs 
            WHERE bpm IS NOT NULL 
        """
        df = pd.read_sql_query(query, conn)

        # Rest of your similarity calculation code...

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()  # Close connection in finally block

# Example test
print("✅ Checking available song titles in similarity_df...")
print(similarity_df.index.tolist())
recommend_songs("Breathe")