import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { generateCaptionAndSong } from '../services/api';

const Home = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleImageSelect = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
  };

  const handleSubmit = async () => {
    if (!selectedFile) return;

    setIsLoading(true);
    try {
      const result = await generateCaptionAndSong(selectedFile);
      navigate('/result', {
        state: {
          caption: result.caption,
          song: result.song
        }
      });
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while processing your image. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="home-container">
      <h1>Instagram Caption & Song Generator</h1>
      <p>Upload your photo and get a perfect caption with a matching song recommendation!</p>
      
      <div className="file-input-container">
        <label className="custom-file-input">
          {selectedFile ? 'Change Image' : 'Choose Image'}
          <input
            type="file"
            accept="image/*"
            onChange={handleImageSelect}
            style={{ display: 'none' }}
            disabled={isLoading}
          />
        </label>
        {selectedFile && <p>Selected: {selectedFile.name}</p>}
      </div>

      {isLoading ? (
        <div className="loading-spinner" />
      ) : (
        <button
          className="submit-button"
          onClick={handleSubmit}
          disabled={!selectedFile || isLoading}
        >
          Generate Caption & Song
        </button>
      )}
    </div>
  );
};

export default Home;
