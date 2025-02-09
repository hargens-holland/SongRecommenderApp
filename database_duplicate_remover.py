import sqlite3
import pandas as pd


def remove_duplicates():
    print("Connecting to database...")
    conn = sqlite3.connect("../song_recommender.db")

    # First, let's count total songs before cleanup
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM songs")
    initial_count = cursor.fetchone()[0]
    print(f"Initial song count: {initial_count}")

    # Load all songs into DataFrame
    print("\nLoading songs...")
    df = pd.read_sql_query("SELECT * FROM songs", conn)

    # Find duplicates based on title and artist
    print("\nFinding duplicates...")
    duplicates = df[df.duplicated(subset=['title', 'artist'], keep=False)]
    duplicate_count = len(duplicates)

    if duplicate_count > 0:
        print(f"\nFound {duplicate_count} duplicate entries")
        print("\nExample duplicates:")
        # Group duplicates and show first few examples
        duplicate_groups = duplicates.groupby(['title', 'artist'])
        for (title, artist), group in list(duplicate_groups)[:5]:
            print(f"\n{title} by {artist} appears {len(group)} times:")
            print(group[['id', 'title', 'artist']].to_string())

        # Keep only the first occurrence of each song
        print("\nRemoving duplicates...")
        df_clean = df.drop_duplicates(subset=['title', 'artist'], keep='first')

        # Replace original table with deduplicated version
        print("Replacing original table with deduplicated version...")
        # First create temporary table
        df_clean.to_sql('songs_temp', conn, index=False, if_exists='replace')

        # Drop original table and rename temp table
        cursor.execute("DROP TABLE songs")
        cursor.execute("ALTER TABLE songs_temp RENAME TO songs")
        conn.commit()

        # Verify the new table
        cursor.execute("SELECT COUNT(*) FROM songs")
        new_count = cursor.fetchone()[0]
        print(f"\nOriginal song count: {initial_count}")
        print(f"New song count: {new_count}")
        print(f"Removed {initial_count - new_count} duplicate entries")
        print("\nDatabase updated successfully!")
    else:
        print("No duplicates found!")

    conn.close()
    print("\nProcess completed!")


if __name__ == "__main__":
    remove_duplicates()