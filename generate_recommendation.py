import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("song_recommender.db")

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
    if song_title not in similarity_df.index:
        print("❌ Song not found in database!")
        return []

    # Get similarity scores for the song
    similar_songs = similarity_df[song_title].sort_values(ascending=False)[1:num_recommendations + 1]

    # Create a mapping of titles to artists
    song_artist_map = df.set_index("title")["artist"].to_dict()

    # Print results
    print(f"🎵 Songs similar to '{song_title}' by {song_artist_map.get(song_title, 'Unknown Artist')}:")
    for song, score in similar_songs.items():
        artist = song_artist_map.get(song, "Unknown Artist")
        print(f"{song} by {artist} (Similarity: {score:.2f})")

    return [(song, song_artist_map.get(song, "Unknown Artist")) for song in similar_songs.index]


# Example test
song = input("What song would you like to look for recommendations for?")
recommend_songs(song)