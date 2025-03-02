"""Utility functions for image and text processing."""

from typing import List
import numpy as np
import torch
from PIL import Image
from models import clip_model, preprocess
import clip
from config import device
from constants import MAX_WORDS

def process_image_for_clip(image: Image.Image) -> torch.Tensor:
    """Process an image for input to the CLIP model.

    Args:
        image (Image.Image): The input PIL image.

    Returns:
        torch.Tensor: Processed image tensor ready for CLIP.
    """
    image = preprocess(image).unsqueeze(0).to(device)
    return image

def generate_text_embedding(text: str) -> List[float]:
    """Generate a normalized text embedding using CLIP.

    Args:
        text (str): The input text to embed, truncated to 77 characters if longer.

    Returns:
        List[float]: A normalized CLIP text embedding as a list of floats.
    """
    text_token = clip.tokenize([text[:77]]) 
    with torch.no_grad():
        embedding = clip_model.encode_text(text_token.to(device))
        embedding /= embedding.norm(dim=-1, keepdim=True)
        return embedding.cpu().numpy()[0].tolist()

def generate_image_embedding(image: Image.Image) -> List[float]:
    """Generate a normalized image embedding using CLIP.

    Args:
        image (Image.Image): The input PIL image.

    Returns:
        List[float]: Normalized embedding as a list of floats.
    """
    image_tensor = process_image_for_clip(image)
    with torch.no_grad():
        embedding = clip_model.encode_image(image_tensor)
        embedding /= embedding.norm(dim=-1, keepdim=True)
        return embedding.cpu().numpy()[0].tolist()

def truncate_text(text: str, max_words: int = MAX_WORDS) -> str:
    """Truncate text to a specified number of words.

    Args:
        text (str): The input text to truncate.
        max_words (int): Maximum number of words to keep (default from constants).

    Returns:
        str: Truncated text.
    """
    return ' '.join(text.split()[:max_words]) if text else ""