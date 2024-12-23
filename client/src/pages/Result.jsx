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
      <h2>Your Results</h2>
      <p><strong>Caption:</strong> {caption}</p>
      <div className="song-recommendation">
        <h3>Song Recommendation:</h3>
        <p><strong>Title:</strong> {song.name}</p>
        <p><strong>Artist:</strong> {song.artist}</p>
        {song.spotify_url && (
          <a href={song.spotify_url} target="_blank" rel="noopener noreferrer">
            Listen on Spotify
          </a>
        )}
      </div>
      <button onClick={() => navigate("/")}>Upload Another Image</button>
    </div>
  );
};

export default Result;
