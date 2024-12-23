# routes/song.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.spotify_api import get_song_recommendation

router = APIRouter()

# Define request body model
class CaptionRequest(BaseModel):
    caption: str

@router.post("/")
async def recommend_song(request: CaptionRequest):
    try:
        # Get song recommendation based on caption
        song = get_song_recommendation(request.caption)
        
        # If there's an error in the song response
        if "error" in song:
            raise HTTPException(status_code=404, detail=song["error"])
            
        return song  # Return song directly without wrapping it in another object
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))