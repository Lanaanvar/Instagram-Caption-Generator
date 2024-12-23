import axios from "axios";

const BASE_URL = "http://localhost:8000"; // Replace with your backend URL

export const generateCaptionAndSong = async (imageFile) => {
  const formData = new FormData();
  formData.append("image", imageFile);

  try {
    // First get the caption
    const captionResponse = await axios.post(`${BASE_URL}/api/caption`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    // Then get the song recommendation using the caption
    const songResponse = await axios.post(`${BASE_URL}/api/song`, {
      caption: captionResponse.data.caption
    });

    return {
      caption: captionResponse.data.caption,
      song: songResponse.data  // The song data now comes directly from the response
    };
  } catch (error) {
    console.error("Error generating caption and song:", error);
    throw error;
  }
};
