"""Gallery routes for displaying and deleting images."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from database import collection
import os
from config import UPLOAD_DIRECTORY
from constants import TEMPLATES_DIRECTORY, BASE_URL
from routes.helpers import format_image_data

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIRECTORY)

@router.get("/gallery/", response_class=HTMLResponse)
async def display_gallery(request):
    """Render the gallery HTML page."""
    return templates.TemplateResponse("gallery.html", {"request": request})

@router.get("/gallery/get-images/")
async def get_gallery_images():
    """Retrieve all images from the database, sorted by upload date."""
    try:
        results = collection.get(include=["metadatas"])
        # If no metadata or IDs, return an empty list instead of raising an error
        if not results.get("metadatas") or not results.get("ids"):
            return JSONResponse(content={"images": []})

        images = [format_image_data(metadata, results["ids"][i], BASE_URL) 
                 for i, metadata in enumerate(results["metadatas"]) if "image_url" in metadata]
        images.sort(key=lambda x: x["metadata"]["dates"], reverse=True)
        return JSONResponse(content={"images": images})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving gallery images: {str(e)}")

@router.delete("/gallery/delete-image/{image_id}")
async def delete_gallery_image(image_id: str):
    """Delete an image from the gallery by its ID."""
    try:
        result = collection.get(ids=[image_id], include=["metadatas"])
        if not result["ids"] or image_id not in result["ids"]:
            raise HTTPException(status_code=404, detail="Image not found in the database.")

        metadata = result["metadatas"][0]
        image_path = os.path.join(UPLOAD_DIRECTORY, metadata["image_url"].split("/")[-1])
        collection.delete(ids=[image_id])
        if os.path.exists(image_path):
            os.remove(image_path)

        return JSONResponse(content={"message": f"Image {image_id} deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting image: {str(e)}")