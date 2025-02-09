import pandas as pd

df1 = pd.read_csv("Best Songs on Spotify from 2000-2023.csv", on_bad_lines="skip", encoding="utf-8")
print(df1.head())  # Check if the data loads properly
df2 = pd.read_csv("billboard_24years_lyrics_spotify.csv")

# Rename columns to match schema
df1.rename(columns={'top genre': 'genre', 'bpm': 'bpm', 'dB': 'loudness'}, inplace=True)
df2.rename(columns={'song': 'title', 'band_singer': 'artist', 'tempo': 'bpm'}, inplace=True)

# Convert duration from ms to seconds
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

print("✅ Data cleaned and ready for insertion!")