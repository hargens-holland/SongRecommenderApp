import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("song_recommender.db")
cursor = conn.cursor()

# Load CSV while skipping problematic lines
df1 = pd.read_csv("Best Songs on Spotify from 2000-2023.csv", on_bad_lines="skip", encoding="utf-8")
df2 = pd.read_csv("billboard_24years_lyrics_spotify.csv", on_bad_lines="skip", encoding="utf-8")


# Rename columns for consistency
df1.rename(columns={'top genre': 'genre', 'bpm': 'bpm', 'dB': 'loudness'}, inplace=True)
df2.rename(columns={'song': 'title', 'band_singer': 'artist', 'tempo': 'bpm'}, inplace=True)

# Convert duration from ms to seconds
if "duration_ms" in df2.columns:
    df2['duration'] = df2['duration_ms'] / 1000

# Ensure both datasets have the same columns
common_columns = [
    "title", "artist", "year", "genre", "popularity", "ranking", "lyrics", "bpm", "energy",
    "danceability", "loudness", "liveness", "valence", "speechiness", "acousticness",
    "instrumentalness", "mode", "key", "time_signature", "duration"
]

# Add missing columns with None
for col in common_columns:
    if col not in df1.columns:
        df1[col] = None
    if col not in df2.columns:
        df2[col] = None

df1 = df1[common_columns]
df2 = df2[common_columns]

# Function to insert data while handling duplicates
def insert_songs(df):
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO songs (title, artist, year, genre, popularity, ranking, lyrics, bpm, energy,
                              danceability, loudness, liveness, valence, speechiness, acousticness,
                              instrumentalness, mode, key, time_signature, duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(title, artist, year) DO UPDATE SET
                genre=COALESCE(excluded.genre, songs.genre),
                popularity=COALESCE(excluded.popularity, songs.popularity),
                ranking=COALESCE(excluded.ranking, songs.ranking),
                lyrics=COALESCE(excluded.lyrics, songs.lyrics),
                bpm=COALESCE(excluded.bpm, songs.bpm),
                energy=COALESCE(excluded.energy, songs.energy),
                danceability=COALESCE(excluded.danceability, songs.danceability),
                loudness=COALESCE(excluded.loudness, songs.loudness),
                liveness=COALESCE(excluded.liveness, songs.liveness),
                valence=COALESCE(excluded.valence, songs.valence),
                speechiness=COALESCE(excluded.speechiness, songs.speechiness),
                acousticness=COALESCE(excluded.acousticness, songs.acousticness),
                instrumentalness=COALESCE(excluded.instrumentalness, songs.instrumentalness),
                mode=COALESCE(excluded.mode, songs.mode),
                key=COALESCE(excluded.key, songs.key),
                time_signature=COALESCE(excluded.time_signature, songs.time_signature),
                duration=COALESCE(excluded.duration, songs.duration)
        ''', tuple(row))

    conn.commit()

# Check for missing titles
missing_titles_df = df1[df1["title"].isna()]

if not missing_titles_df.empty:
    print("⚠️ WARNING: There are missing song titles. Here are some examples:")
    print(missing_titles_df.head())

# Drop rows with missing song titles
df1 = df1.dropna(subset=["title"])
df2 = df2.dropna(subset=["title"])

# Insert data into the database
insert_songs(df1)
insert_songs(df2)

# Close connection
conn.close()

print("✅ Data inserted successfully into the database!")
