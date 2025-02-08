import requests
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import kagglehub

# Load the dataset (modify path as needed)
path = kagglehub.dataset_download("tomigelo/spotify-audio-features")
songs_df = pd.read_csv(path)

def search_song(song_name):
    """Searches Deezer for a song and returns track info."""
    url = f"https://api.deezer.com/search?q={song_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            track = data["data"][0]
            track_info = {
                "Song Name": track["title"],
                "Artist": track["artist"]["name"],
                "Deezer ID": track["id"],
                "Deezer URL": track["link"],
                "Preview URL": track["preview"]  # 30-second audio preview
            }
            print("🔍 Found Song:", track_info)
            return track_info
        else:
            print("❌ No songs found for:", song_name)
            return None
    else:
        print("❌ Error searching song:", response.json())
        return None

def get_song_details(deezer_id):
    """Fetches detailed song information from Deezer."""
    url = f"https://api.deezer.com/track/{deezer_id}"
    response = requests.get(url)

    if response.status_code == 200:
        song_data = response.json()
        song_info = {
            "Song Name": song_data["title"],
            "Artist": song_data["artist"]["name"],
            "Album": song_data["album"]["title"],
            "Duration (s)": song_data["duration"],
            "Release Date": song_data["release_date"],
            "Genre": song_data.get("genre_id", "Unknown"),
            "Deezer URL": song_data["link"],
            "Preview URL": song_data["preview"]
        }
        print("🎵 Detailed Song Info:", song_info)
        return song_info
    else:
        print("❌ Error getting song details:", response.json())
        return None

def search_similar_songs(artist_name):
    """Finds similar songs based on the artist's name."""
    url = f"https://api.deezer.com/search?q=artist:'{artist_name}'"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            similar_songs = [
                {
                    "Song Name": track["title"],
                    "Artist": track["artist"]["name"],
                    "Deezer URL": track["link"],
                    "Preview URL": track["preview"]
                }
                for track in data["data"][:5]
            ]
            print("🎶 Similar Songs Found:", similar_songs)
            return similar_songs
        else:
            print("❌ No similar songs found.")
            return None
    else:
        print("❌ Error searching for similar songs:", response.json())
        return None


def recommend_songs(song_name):
    """Finds song recommendations based on artist and genre."""

    # Step 1: Search for the song
    song = search_song(song_name)
    if not song:
        print("❌ Could not find the song.")
        return None

    # Step 2: Get song details (to extract genre)
    details = get_song_details(song["Deezer ID"])
    if not details:
        print("❌ Could not get song details.")
        return None

    artist_name = song["Artist"]
    genre_id = details["Genre"]

    print(f"🎵 Recommending songs based on '{song_name}' by {artist_name} (Genre ID: {genre_id})")

    # Step 3: Get similar songs based on artist
    similar_songs = search_similar_songs(artist_name)

    # Step 4: Get other songs in the same genre (if available)
    genre_songs = []
    if genre_id != "Unknown":
        url = f"https://api.deezer.com/genre/{genre_id}/artists"
        response = requests.get(url)

        if response.status_code == 200:
            genre_data = response.json()
            if "data" in genre_data:
                genre_artists = [artist["name"] for artist in genre_data["data"][:3]]  # Top 3 artists in genre
                for artist in genre_artists:
                    genre_songs.extend(search_similar_songs(artist))

    # Step 5: Combine and remove duplicates
    recommended_songs = {song["Deezer URL"]: song for song in (similar_songs + genre_songs)}.values()

    print("🎶 Final Recommendations:")
    return list(recommended_songs)[:5]  # Return top 5 recommendations


def recommend_songs_from_dataset(song_name, top_n=5):
    """Recommends songs based on tempo, energy, and danceability."""

    # Search for the song in the dataset
    song_row = songs_df[songs_df["title"].str.lower() == song_name.lower()]
    if song_row.empty:
        print("❌ Song not found in dataset.")
        return None

    # Extract features
    song_features = song_row[["tempo", "energy", "danceability"]].values

    # Compute similarity to all other songs
    song_matrix = songs_df[["tempo", "energy", "danceability"]].values
    similarities = cosine_similarity(song_features, song_matrix)

    # Get the most similar songs
    similar_indices = np.argsort(similarities[0])[::-1][1:top_n + 1]
    recommended_songs = songs_df.iloc[similar_indices][["title", "artist"]]

    print("🎶 AI-Based Recommendations:")
    return recommended_songs.to_dict(orient="records")

# Example Usage
if __name__ == "__main__":
    print("🔍 Searching for 'Blinding Lights'...")
    song = search_song("Blinding Lights")
    if song:
        print("🎵 Getting song details...")
        details = get_song_details(song["Deezer ID"])
        print("🎶 Song Details:", details)

        print("🔄 Finding similar songs...")
        similar = search_similar_songs(song["Artist"])
        print("🎵 Recommended Songs:", similar)
