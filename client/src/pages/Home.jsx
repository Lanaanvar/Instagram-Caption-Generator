import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { generateCaptionAndSong } from '../services/api';

const Home = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setIsLoading(true);
    try {
      const result = await generateCaptionAndSong(file);
      
      // Navigate to result page with both caption and song data
      navigate('/result', {
        state: {
          caption: result.caption,
          song: result.song
        }
      });
    } catch (error) {
      console.error('Error:', error);
      // Handle error appropriately
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="home-container">
      <h1>Generate Captions and Songs for Instagram</h1>
      <p>Upload an image to get started!</p>
      <input 
        type="file" 
        accept="image/*" 
        onChange={handleImageUpload}
        disabled={isLoading}
      />
      {isLoading && <p>Processing...</p>}
    </div>
  );
};

export default Home;
