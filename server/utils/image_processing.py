from PIL import Image

def preprocess_image(image_path: str) -> Image:
    image = Image.open(image_path).convert("RGB")
    # Resize or normalize the image if required
    return image
