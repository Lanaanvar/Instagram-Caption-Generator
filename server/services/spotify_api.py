# services/spotify_api.py
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
from typing import List

load_dotenv()

# Get credentials from environment variables
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

def get_song_recommendation(caption: str, previous_songs: List[str] = None) -> dict:
    if previous_songs is None:
        previous_songs = []
    
    # Clean the caption and extract meaningful terms
    # Remove hashtag symbols but keep the words
    clean_caption = re.sub(r'#(\w+)', r'\1', caption.lower())
    
    # Remove special characters and extra spaces
    clean_caption = re.sub(r'[^\w\s]', ' ', clean_caption)
    
    # Get the most significant words (excluding common words)
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    significant_terms = [word for word in clean_caption.split() 
                        if word not in common_words and len(word) > 2]
    
    # Create search query from significant terms (limit to first 3 terms to avoid too specific searches)
    search_terms = ' '.join(significant_terms[:3])
    
    # If no significant terms found, use the original caption
    if not search_terms:
        search_terms = caption[:50]  # Limit length for API compatibility
    
    try:
        # Search for tracks using the processed caption
        results = sp.search(
            q=search_terms,
            limit=50,  # Increased limit for more options
            type="track"
        )
        
        if results["tracks"]["items"]:
            # Get random track from results
            import random
            tracks = results["tracks"]["items"]
            # Filter out previously played songs
            new_tracks = [t for t in tracks 
                         if t["name"] not in previous_songs 
                         and t["preview_url"]]
            
            if not new_tracks:
                # If no new tracks with preview_url, try without preview_url requirement
                new_tracks = [t for t in tracks 
                            if t["name"] not in previous_songs]
            
            if new_tracks:
                track = random.choice(new_tracks)
                return {
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "preview_url": track["preview_url"],
                    "spotify_url": track["external_urls"]["spotify"],
                    "album_image": track["album"]["images"][0]["url"] if track["album"]["images"] else None
                }
            
            # If no new tracks available, try fallback
    except Exception as e:
        print(f"Error in Spotify API: {str(e)}")
    
    # Fallback to genre-based search if caption search fails
    try:
        mood_based_results = sp.recommendations(
            seed_genres=['pop'],
            limit=1,
            target_energy=0.7,
            target_valence=0.7
        )
        
        if mood_based_results["tracks"]:
            track = mood_based_results["tracks"][0]
            return {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "preview_url": track["preview_url"],
                "spotify_url": track["external_urls"]["spotify"],
                "album_image": track["album"]["images"][0]["url"] if track["album"]["images"] else None
            }
    except Exception as e:
        print(f"Error in fallback recommendation: {str(e)}")
    
    return {"error": "No suitable song found"}