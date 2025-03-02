"""Upload routes for handling image uploads."""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import uuid
import os
import datetime
from PIL import Image
from models import gemini_model
from database import collection
from utils import truncate_text
from config import UPLOAD_DIRECTORY
from constants import TEMPLATES_DIRECTORY, JPG_EXTENSION, BASE_URL, GEMINI_ANALYSIS_PROMPT
from routes.helpers import process_image_file, parse_metadata, generate_image_text_embedding


router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIRECTORY)


async def save_image(file: UploadFile, upload_dir: str) -> tuple[str, Image.Image]:
    """Save an uploaded image and return its filename and PIL object."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail=f"File {file.filename} is not an image.")
    
    contents = await file.read()
    try:
        image = process_image_file(contents)
        image_filename = f"{uuid.uuid4()}{JPG_EXTENSION}"
        image_path = os.path.join(upload_dir, image_filename)
        image.save(image_path)
        return image_filename, image
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {file.filename}")


async def generate_image_metadata(image: Image.Image, upload_time: str) -> tuple[str, str, dict]:
    """Generate description and metadata for an image using Gemini."""
    response = gemini_model.generate_content(
        [GEMINI_ANALYSIS_PROMPT.format(upload_time=upload_time), image],
        generation_config={"temperature": 0.5}
    )
    full_description = response.text
    truncated_description = truncate_text(full_description)
    metadata = parse_metadata(full_description, upload_time)
    return full_description, truncated_description, metadata


async def store_image_data(image_filename: str, image: Image.Image, file: UploadFile, full_description: str, 
                         truncated_description: str, metadata: dict, upload_time: str) -> str:
    """Store image data and embeddings in ChromaDB."""
    combined_embedding = generate_image_text_embedding(image, truncated_description)
    
    unique_id = str(uuid.uuid4())
    collection.add(
        ids=[unique_id],
        embeddings=[combined_embedding.tolist()],
        metadatas=[{
            "filename": file.filename,
            "image_url": f"/static/images/{image_filename}",
            "full_description": full_description,
            "dates": upload_time,
            **metadata
        }],
    )
    return unique_id


@router.post("/upload-images/")
async def upload_images(files: list[UploadFile] = File(...)):
    """Upload images and store their metadata."""
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    uploaded_images = []
    upload_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for file in files:
        image_filename, image = await save_image(file, UPLOAD_DIRECTORY)
        full_desc, trunc_desc, metadata = await generate_image_metadata(image, upload_time)
        await store_image_data(image_filename, image, file, full_desc, trunc_desc, metadata, upload_time)
        
        full_image_url = f"{BASE_URL}/static/images/{image_filename}"
        uploaded_images.append({
            "image_url": full_image_url,
            "full_description": full_desc,
            "dominant_colors": metadata["dominant_colors"].split(","),
            "uploaded_at": metadata["uploaded_at"]
        })

    return {
        "message": f"Successfully uploaded {len(uploaded_images)} image(s)",
        "uploaded_images": uploaded_images
    }
