# services/spotify_api.py
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

# Get credentials from environment variables
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

def get_song_recommendation(caption: str) -> dict:
    # Analyze caption and find suitable genre or mood
    keywords = {
        "happy": "pop",
        "joy": "pop",
        "sad": "chill",
        "lonely": "chill",
        "energy": "rock",
        "excited": "dance"
    }
    
    # Default genre if no matching keywords
    genre = "pop"
    
    # Find matching genre based on caption keywords
    for keyword, matched_genre in keywords.items():
        if keyword in caption.lower():
            genre = matched_genre
            break

    # Get recommendations from Spotify
    results = sp.search(q=f"genre:{genre}", limit=1, type="track")
    
    if results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        return {
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "preview_url": track["preview_url"],
            "spotify_url": track["external_urls"]["spotify"]
        }
    
    return {"error": "No suitable song found"}