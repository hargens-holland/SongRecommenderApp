import os
os.environ["DYLD_LIBRARY_PATH"] = "/usr/local/opt/openssl@3/lib"
import kagglehub

# Download the latest version of the Spotify dataset
path = kagglehub.dataset_download("tomigelo/spotify-audio-features")

print("✅ Dataset downloaded at:", path)