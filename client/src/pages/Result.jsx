import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { getAnotherSong } from '../services/api';

const Result = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const { caption } = location.state || {};
  const [currentSong, setCurrentSong] = useState(location.state?.song);
  const [previousSongs, setPreviousSongs] = useState([location.state?.song?.name || '']);

  useEffect(() => {
    if (!location.state || !caption || !currentSong) {
      navigate("/");
    }
  }, [location.state, caption, currentSong, navigate]);

  const handleGetAnotherSong = async () => {
    setIsLoading(true);
    try {
      const newSong = await getAnotherSong(caption, previousSongs);
      if (newSong && !newSong.error) {
        setCurrentSong(newSong);
        setPreviousSongs(prev => [...prev, newSong.name]);
      } else {
        alert('No more unique songs available. Try with a different image.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to get another song. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  if (!caption || !currentSong) {
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
        {isLoading ? (
          <div className="loading-spinner" />
        ) : (
          <>
            <p><strong>Title:</strong> {currentSong.name}</p>
            <p><strong>Artist:</strong> {currentSong.artist}</p>
            <div className="song-buttons">
              {currentSong.spotify_url && (
                <a 
                  href={currentSong.spotify_url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="spotify-link"
                >
                  Listen on Spotify
                </a>
              )}
              <button 
                className="another-song-button"
                onClick={handleGetAnotherSong}
                disabled={isLoading}
              >
                {isLoading ? 'Finding new song...' : 'Get Another Song'}
              </button>
            </div>
          </>
        )}
      </div>
      
      <button className="submit-button" onClick={() => navigate("/")}>
        Create Another
      </button>
    </div>
  );
};

export default Result;
