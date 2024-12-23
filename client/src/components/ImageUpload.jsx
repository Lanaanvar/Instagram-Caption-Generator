import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { generateCaptionAndSong } from "../services/api";

const ImageUpload = () => {
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) return alert("Please upload an image!");
    setLoading(true);

    try {
      const data = await generateCaptionAndSong(image);
      console.log("API Response:", data); // Debug log
      setLoading(false);
      navigate("/result", { state: { caption: data.caption, song: data.song } });
    } catch (error) {
      setLoading(false);
      alert("Error generating caption and song. Please try again.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="upload-form">
      <input
        type="file"
        accept="image/*"
        onChange={handleImageChange}
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? "Generating..." : "Submit"}
      </button>
    </form>
  );
};

export default ImageUpload;
