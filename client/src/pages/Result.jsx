import React, { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const Result = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { caption, song } = location.state || {};

  useEffect(() => {
    if (!location.state || !caption || !song) {
      navigate("/");
    }
  }, [location.state, caption, song, navigate]);

  if (!caption || !song) {
    return null;
  }

  return (
    <div className="result-container">
      <h2>Your Perfect Instagram Post</h2>
      <div className="caption-section">
        <h3>📸 Caption</h3>
        <p>{caption}</p>
      </div>
      
      <div className="song-recommendation">
        <h3>🎵 Perfect Song Match</h3>
        <p><strong>Title:</strong> {song.name}</p>
        <p><strong>Artist:</strong> {song.artist}</p>
        {song.spotify_url && (
          <a 
            href={song.spotify_url} 
            target="_blank" 
            rel="noopener noreferrer"
            className="spotify-link"
          >
            Listen on Spotify
          </a>
        )}
      </div>
      
      <button className="submit-button" onClick={() => navigate("/")}>
        Create Another
      </button>
    </div>
  );
};

export default Result;
