import sqlite3
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# Load all songs from database
print("Loading songs from database...")
conn = sqlite3.connect("../song_recommender.db")

# Get total count in database
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM songs")
total_songs = cursor.fetchone()[0]
print(f"Total songs in database: {total_songs}")

# Load first 10000 songs
df = pd.read_sql_query("""
    SELECT title, artist, bpm, energy, danceability, loudness, valence, 
           acousticness, speechiness, instrumentalness
    FROM songs
    LIMIT 10000
""", conn)
conn.close()

print(f"\nLoaded {len(df)} songs for recommendations")

# Print all available songs in a clean format
print("\nAVAILABLE SONGS:")
print("-" * 80)
for idx, row in df.iterrows():
    print(f"{idx + 1:4d}. {row['title']} by {row['artist']}")
print("-" * 80)

# Fill missing values only in numeric columns
numeric_columns = ['bpm', 'energy', 'danceability', 'loudness', 'valence',
                   'acousticness', 'speechiness', 'instrumentalness']
df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

# Prepare features for similarity calculation
print("\nScaling features...")
features = df[numeric_columns]
scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(features)

# Calculate similarity matrix
print("Calculating similarity matrix...")
similarity_df = pd.DataFrame(
    cosine_similarity(scaled_features),
    index=df["title"] + " by " + df["artist"],
    columns=df["title"] + " by " + df["artist"]
)

print("Setup complete!")


def recommend_songs(song_input, num_recommendations=5):
    """Find similar songs based on audio features."""
    try:
        print(f"\nSearching for: '{song_input}'")

        # Look for exact match
        if song_input in similarity_df.index:
            similar_songs = similarity_df.loc[song_input].sort_values(ascending=False)[1:num_recommendations + 1]

            print(f"\n🎵 Songs similar to '{song_input}':")
            for song, score in similar_songs.items():
                print(f"- {song} (similarity: {score:.2f})")
            return similar_songs

        # If no exact match, try to find similar titles
        if " by " in song_input.lower():
            title, artist = song_input.lower().split(" by ", 1)
            matches = [s for s in similarity_df.index if title in s.lower() and artist in s.lower()]
        else:
            matches = [s for s in similarity_df.index if song_input.lower() in s.lower()]

        if matches:
            if len(matches) > 1:
                print("\nMultiple matches found:")
                for i, match in enumerate(matches, 1):
                    print(f"{i}. {match}")
                print("\nPlease specify using 'title by artist' format")
            else:
                return recommend_songs(matches[0], num_recommendations)
        else:
            print(f"❌ Song '{song_input}' not found in the dataset!")

    except Exception as e:
        print(f"Error: {e}")

    return []

# Example usage:
#recommend_songs("BACKBONE by DROELOE")
recommend_songs("No Limit by Young Thug")