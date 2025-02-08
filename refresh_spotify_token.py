import os
import requests
import time
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")

def refresh_spotify_token():
    """Refreshes the Spotify access token using the refresh token."""
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        response_data = response.json()
        access_token = response_data["access_token"]

        # Update the .env file with the new access token
        update_env_file(access_token)

        print("✅ Spotify access token refreshed!")
        print("🔑 New Access Token:", access_token)
    else:
        print("Error refreshing token:", response.json())

def update_env_file(access_token):
    """Updates the .env file with the new access token."""
    with open(".env", "r") as file:
        lines = file.readlines()

    with open(".env", "w") as file:
        for line in lines:
            if line.startswith("SPOTIFY_ACCESS_TOKEN="):
                file.write(f"SPOTIFY_ACCESS_TOKEN={access_token}\n")
            else:
                file.write(line)

# Run the token refresh process
if __name__ == "__main__":
    refresh_spotify_token()
