import requests

def search_deezer(song_name):
    """Search for a song on Deezer and return details."""
    url = f"https://api.deezer.com/search?q={song_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            track = data["data"][0]  # Get the first search result
            song_info = {
                "Title": track["title"],
                "Artist": track["artist"]["name"],
                "Album": track["album"]["title"],
                "Duration (s)": track["duration"],
                "Deezer URL": track["link"],
                "Preview URL": track["preview"]  # 30-second audio preview
            }
            return song_info
        else:
            print("❌ No song found.")
            return None
    else:
        print("❌ Error fetching data from Deezer:", response.json())
        return None

if __name__ == "__main__":
    song_name = input("🎵 Enter a song name: ")
    result = search_deezer(song_name)

    if result:
        print("\n🎶 Song Details:")
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print("❌ No data found.")
