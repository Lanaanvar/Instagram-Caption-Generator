from fastapi import APIRouter, UploadFile, HTTPException
from models.caption_model import InstagramCaptionGenerator
import tempfile
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/")
async def generate_instagram_caption(image: UploadFile) -> dict:
    """
    API endpoint for generating Instagram captions
    """
    if not image:
        raise HTTPException(status_code=400, detail="No image file provided")
        
    if not image.filename:
        raise HTTPException(status_code=400, detail="Invalid image file")

    temp_file_path = None
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            contents = await image.read()
            if not contents:
                raise HTTPException(status_code=400, detail="Empty image file")
            temp_file.write(contents)
            temp_file_path = temp_file.name

        logger.info(f"Processing image: {image.filename}")
        caption_generator = InstagramCaptionGenerator()
        caption = caption_generator.generate_creative_caption(temp_file_path)
        
        if not caption:
            raise HTTPException(status_code=500, detail="Failed to generate caption")
        
        return {"caption": caption}
    
    except Exception as e:
        logger.error(f"Error generating caption: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process image: {str(e)}"
        )
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception as e:
                logger.error(f"Error cleaning up temporary file: {str(e)}")