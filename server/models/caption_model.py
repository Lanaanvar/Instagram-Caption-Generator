import random
from typing import List, Tuple
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import logging
import google.generativeai as genai
import os
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

logger = logging.getLogger(__name__)

class InstagramCaptionGenerator:
    def __init__(self):
        # Initialize Gemini API key check
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            logger.warning("Gemini API key not found in environment variables")
        else:
            genai.configure(api_key=self.api_key)
            
        # Download required NLTK data
        self._initialize_nltk()
        
        # Configure Gemini model with updated version
        try:
            # Update to the new model version
            self.model = genai.GenerativeModel('gemini-1.5-pro')
            # Configure model settings
            self.model.temperature = 0.7  # Add some creativity while maintaining coherence
            self.model.top_p = 0.8
            self.model.top_k = 40
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {str(e)}")
            self.model = None

    def _initialize_nltk(self):
        """Initialize required NLTK resources"""
        required_resources = [
            'punkt',
            'averaged_perceptron_tagger'
        ]
        
        for resource in required_resources:
            try:
                nltk.data.find(f'tokenizers/{resource}')
                logger.info(f"NLTK resource {resource} already downloaded")
            except LookupError:
                try:
                    nltk.download(resource, quiet=True)
                    logger.info(f"Successfully downloaded NLTK resource: {resource}")
                except Exception as e:
                    logger.error(f"Error downloading NLTK resource {resource}: {str(e)}")
                    raise RuntimeError(f"Failed to initialize NLTK resource: {resource}")

    def _enhance_caption_with_ai(self, image_path: str) -> dict:
        """Generate creative caption and hashtags using Gemini Vision API with image analysis"""
        if not self.api_key or not self.model:
            raise ValueError("Gemini API key and model are required for caption generation")

        try:
            # Read and encode the image
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
                image_parts = [
                    {
                        "mime_type": "image/jpeg",
                        "data": base64.b64encode(image_data).decode('utf-8')
                    }
                ]

            prompt = """You are a social media expert crafting Instagram captions.
            Look at this image and create:

            1. A short, catchy Instagram caption that is:
               - Max 1-2 sentences
               - Casual and conversational
               - Includes 1-2 relevant emojis
               - Captures the vibe/mood rather than describing the image
               - Something a real person would write
               
            2. Add 3-4 relevant hashtags that are:
               - Trendy and actually used on Instagram
               - Specific to the content/mood
               - Not overly generic
               
            Format as:
            CAPTION: [short engaging caption]
            HASHTAGS: [hashtags]
            
            Remember: Keep it brief and natural, like a real Instagram post."""

            response = self.model.generate_content([prompt, image_parts[0]])
            
            if not response.text:
                raise ValueError("Gemini returned empty response")
            
            # Parse response to separate caption and hashtags
            response_text = response.text.strip()
            parts = response_text.split('HASHTAGS:')
            
            caption = parts[0].replace('CAPTION:', '').strip()
            hashtags = parts[1].strip() if len(parts) > 1 else ''
            
            return {
                "caption": caption,
                "hashtags": hashtags
            }

        except Exception as e:
            logger.error(f"AI caption generation failed: {str(e)}")
            raise RuntimeError(f"Failed to generate caption: {str(e)}")

    def generate_creative_caption(self, image_path: str) -> str:
        """Generate a creative Instagram caption from an image."""
        try:
            # Generate caption and hashtags using AI and image analysis
            result = self._enhance_caption_with_ai(image_path)
            
            # Combine caption and hashtags
            final_caption = f"{result['caption']}\n\n{result['hashtags']}"
            
            return final_caption
            
        except Exception as e:
            logger.error(f"Failed to generate caption: {str(e)}")
            raise RuntimeError(f"Failed to process image")
