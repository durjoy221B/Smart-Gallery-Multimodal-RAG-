"""Chat routes for conversational and image search queries."""

import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from PIL import Image
from models import gemini_model
from database import collection
from utils import truncate_text
from constants import (BASE_URL, INTENT_CLASSIFICATION_PROMPT, SIMILARITY_THRESHOLD, 
                      MAX_SEARCH_RESULTS, INITIAL_QUERY_LIMIT)
from routes.helpers import (process_image_file, generate_single_embedding, generate_image_text_embedding, 
                          parse_metadata, format_image_data)

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def classify_query_intent(query: str) -> str:
    """Classify query intent as conversational or image_search."""
    intent_prompt = INTENT_CLASSIFICATION_PROMPT.format(query=query)
    try:
        response = gemini_model.generate_content(intent_prompt)
        return "conversational" if "conversational" in response.text.strip().lower() else "image_search"
    except Exception as e:
        logger.error(f"Error classifying intent: {str(e)}, defaulting to image_search.")
        return "image_search"


def generate_search_description(results: list) -> str:
    """Generate a natural language summary of search results."""
    if not results or "message" in results[0]:
        return f"No images found with similarity above {SIMILARITY_THRESHOLD}."
    
    combined_metadata = "\n".join(
        f"Image {i+1}: Tags: {res['metadata']['tags']}, Objects: {res['metadata']['objects']}, "
        f"Ambience: {res['metadata']['ambience']}, Dominant Colors: {res['metadata']['dominant_colors']}"
        for i, res in enumerate(results)
    )
    prompt = f"""
    Generate a concise, natural language description (2-3 sentences) summarizing the following group of images based on their metadata:
    {combined_metadata}
    """
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error generating description: {str(e)}")
        return "Unable to generate a combined description due to processing error."
    

async def image_search(embedding) -> dict:
    """Search for similar images based on an embedding."""
    try:
        results = collection.query(
            query_embeddings=[embedding.tolist()],
            n_results=INITIAL_QUERY_LIMIT,
            include=["metadatas", "distances"]
        )
        if not results["ids"] or not results["ids"][0]:
            return {"results": [{"message": "No images found in the database."}], 
                    "combined_description": "No images found to describe."}

        formatted_results = []
        for i, meta in enumerate(results["metadatas"][0]):
            if "image_url" in meta:
                cosine_similarity = 1 - results["distances"][0][i]
                if cosine_similarity > SIMILARITY_THRESHOLD:
                    full_desc = meta.get("full_description", "")
                    metadata = parse_metadata(full_desc, meta.get("dates", "Unknown"))
                    formatted_results.append({
                        "id": results["ids"][0][i],
                        **format_image_data({**meta, **metadata}, results["ids"][0][i], BASE_URL),
                        "similarity_score": cosine_similarity
                    })

        formatted_results = sorted(formatted_results, key=lambda x: x["similarity_score"], reverse=True)[:MAX_SEARCH_RESULTS]
        combined_description = generate_search_description(formatted_results)
        return {"results": formatted_results or [{"message": f"No images above {SIMILARITY_THRESHOLD} similarity."}], 
                "combined_description": combined_description}
    except Exception as e:
        logger.error(f"Error in image search: {str(e)}")
        return {"results": [{"message": f"Search error: {str(e)}"}], "combined_description": "Error occurred during search."}


@router.post("/search/")
async def search(file: UploadFile = File(None), query: str = Form(None)):
    """Handle search requests with text, image, or both."""
    if not file and not query:
        raise HTTPException(status_code=400, detail="Please provide either an image or text query.")

    response_data = {"query_type": "unknown"}

    if file and query:
        contents = await file.read()
        image = process_image_file(contents)
        truncated = truncate_text(query)
        embedding = generate_image_text_embedding(image, truncated)
        response_data["query_type"] = "combined"
        response_data["image_search_results"] = await image_search(embedding)
    elif file:
        contents = await file.read()
        image = process_image_file(contents)
        embedding = generate_single_embedding(image=image)
        response_data["query_type"] = "image"
        response_data["image_search_results"] = await image_search(embedding)
    elif query:
        intent = classify_query_intent(query)
        response_data["query_type"] = intent
        if intent == "conversational":
            response = gemini_model.generate_content(query)
            response_data["conversation_response"] = response.text
        else:
            truncated = truncate_text(query)
            embedding = generate_single_embedding(text=truncated)
            response_data["image_search_results"] = await image_search(embedding)
    
    return response_data