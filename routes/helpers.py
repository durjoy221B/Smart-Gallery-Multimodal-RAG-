"""Helper functions for route handling in the AI Memory Bot."""
import io
import numpy as np
from typing import List, Dict, Any
from PIL import Image
from utils import generate_text_embedding, generate_image_embedding
from constants import (ALPHA_WEIGHT, BETA_WEIGHT, DEFAULT_TAGS, DEFAULT_OBJECTS, 
                      DEFAULT_AMBIENCE, DEFAULT_DOMINANT_COLORS, NO_TAGS, NO_OBJECTS, NO_AMBIENCE)


def combine_embeddings(image_embedding: np.ndarray, text_embedding: np.ndarray) -> np.ndarray:
    """Combine image and text embeddings with weighted averaging."""
    combined = (ALPHA_WEIGHT * image_embedding + BETA_WEIGHT * text_embedding)
    return combined / np.linalg.norm(combined)


def parse_metadata(full_description: str, default_upload_time: str) -> Dict[str, str]:
    """Parse metadata from Gemini's description text."""
    tags, objects, ambience, dominant_colors, uploaded_at = (
        DEFAULT_TAGS, DEFAULT_OBJECTS, DEFAULT_AMBIENCE, DEFAULT_DOMINANT_COLORS, default_upload_time
    )
    for line in full_description.split("\n"):
        if line.startswith("Tags:"):
            tags = line.replace("Tags: ", "").strip()
        elif line.startswith("Objects:"):
            objects = line.replace("Objects: ", "").strip()
        elif line.startswith("Ambience:"):
            ambience = line.replace("Ambience: ", "").strip()
        elif line.startswith("Dominant Colors:"):
            dominant_colors = line.replace("Dominant Colors: ", "").strip()
        elif line.startswith("Uploaded At:"):
            uploaded_at = line.replace("Uploaded At: ", "").strip()
    return {
        "tags": tags,
        "objects": objects,
        "ambience": ambience,
        "dominant_colors": dominant_colors,
        "uploaded_at": uploaded_at
    }


def process_image_file(contents: bytes) -> Image.Image:
    """Process uploaded image file into a PIL Image object."""
    image = Image.open(io.BytesIO(contents))
    return image.convert("RGB") if image.mode != "RGB" else image


def normalize_embedding(embedding: List[float]) -> np.ndarray:
    """Normalize an embedding vector."""
    embedding_array = np.array(embedding)
    norm = np.linalg.norm(embedding_array)
    return embedding_array / norm if norm != 0 else embedding_array


def format_image_data(metadata: Dict[str, Any], image_id: str = None, base_url: str = None) -> Dict[str, Any]:
    """Format image metadata into a consistent response structure."""
    base_url = base_url or "http://127.0.0.1:8000"
    return {
        "id": image_id,
        "image_url": base_url + metadata["image_url"] if "image_url" in metadata else None,
        "metadata": {
            "filename": metadata.get("filename", "Unknown"),
            "dates": metadata.get("dates", "Unknown"),
            "tags": metadata.get("tags", NO_TAGS),
            "objects": metadata.get("objects", NO_OBJECTS),
            "ambience": metadata.get("ambience", NO_AMBIENCE),
            "dominant_colors": metadata.get("dominant_colors", DEFAULT_DOMINANT_COLORS)
        }
    }


def generate_image_text_embedding(image: Image.Image, text: str) -> np.ndarray:
    """Generate and combine embeddings for an image and text."""
    image_embedding = normalize_embedding(generate_image_embedding(image))
    text_embedding = normalize_embedding(generate_text_embedding(text))
    return combine_embeddings(image_embedding, text_embedding)


def generate_single_embedding(image: Image.Image = None, text: str = None) -> np.ndarray:
    """Generate an embedding for either an image or text."""
    if image is not None:
        return normalize_embedding(generate_image_embedding(image))
    if text is not None:
        return normalize_embedding(generate_text_embedding(text))
    return None