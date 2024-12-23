# Instagram Caption Generator

This web application generates a suitable caption and song recommendations for an uploaded image. The user uploads an image, and the application generates a caption using a pre-trained model (BLIP) and recommends a song based on the caption using the Spotify API.

## Features
- **Image Captioning**: Using the BLIP (Bootstrapping Language-Image Pre-training) model, the application generates captions for images.
- **Song Recommendation**: Based on the generated caption, the application fetches suitable song recommendations via the Spotify API.

## Tech Stack
- **Backend**: FastAPI
- **Image Captioning Model**: BLIP (via Hugging Face Transformers)
- **Song Recommendation**: Spotify Web API (via Spotipy)
- **Image Processing**: Pillow
- **Server**: Uvicorn

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
```
