import sqlite3
import pandas as pd

# Database file
DB_FILE = "song_recommender.db"  # Ensure this matches your actual DB file

# CSV files
NEW_FILES = [
    "SpotifyAudioFeaturesApril2019.csv",
    "SpotifyAudioFeaturesNov2018.csv"
]

# Columns to use from the new datasets
COLUMNS_TO_USE = [
    "track_name", "artist_name", "bpm", "energy", "danceability",
    "loudness", "valence", "acousticness", "speechiness", "instrumentalness"
]

# Column renaming to match database schema
COLUMN_RENAME_MAP = {
    "track_name": "title",
    "artist_name": "artist",
    "tempo": "bpm"  # Ensure correct column mapping
}

def load_and_clean_data(file_path):
    """Load a CSV file, clean it, and return a dataframe"""
    try:
        df = pd.read_csv(file_path)

        # Keep only relevant columns (ignore missing ones)
        df = df[[col for col in COLUMNS_TO_USE if col in df.columns]]

        # Rename columns to match database schema
        df.rename(columns=COLUMN_RENAME_MAP, inplace=True)

        # Fill missing values explicitly with None for database insertion
        df = df.where(pd.notna(df), None)

        # Drop duplicates based on (title, artist)
        df.drop_duplicates(subset=["title", "artist"], inplace=True)

        print(f"✅ Loaded and cleaned {file_path}, {len(df)} songs ready for insertion.")
        return df

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return None


def insert_songs_to_db(df):
    """Insert cleaned data into the database."""
    conn = sqlite3.connect("song_recommender.db")
    cursor = conn.cursor()

    insert_query = '''
    INSERT INTO songs (title, artist, bpm, energy, danceability, loudness, valence, acousticness, speechiness, instrumentalness)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    for _, row in df.iterrows():
        try:
            values = [
                row.get("title"), row.get("artist"),
                row.get("bpm"), row.get("energy"),
                row.get("danceability"), row.get("loudness"),
                row.get("valence"), row.get("acousticness"),
                row.get("speechiness"), row.get("instrumentalness")
            ]

            # Handle missing values by replacing them with None
            values = [val if pd.notna(val) else None for val in values]

            cursor.execute(insert_query, values)
        except Exception as e:
            print(f"⚠️ Skipping row due to error: {e}")

    conn.commit()
    conn.close()
    print("✅ All new data successfully inserted!")


if __name__ == "__main__":
    for file in NEW_FILES:
        df = load_and_clean_data(file)
        if df is not None:
            insert_songs_to_db(df)

    print("🎵 All new data has been processed successfully!")
