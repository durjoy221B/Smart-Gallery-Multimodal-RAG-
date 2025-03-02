"""Page routing for the AI Memory Bot web interface."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from dependencies import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page.

    Args:
        request (Request): The FastAPI request object.

    Returns:
        TemplateResponse: Rendered home.html template.
    """
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    """Render the upload page.

    Args:
        request (Request): The FastAPI request object.

    Returns:
        TemplateResponse: Rendered upload.html template.
    """
    return templates.TemplateResponse("upload.html", {"request": request})


@router.get("/gallery", response_class=HTMLResponse)
async def gallery_page(request: Request):
    """Render the gallery page.

    Args:
        request (Request): The FastAPI request object.

    Returns:
        TemplateResponse: Rendered gallery.html template.
    """
    return templates.TemplateResponse("gallery.html", {"request": request})


@router.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    """Render the chat page.

    Args:
        request (Request): The FastAPI request object.

    Returns:
        TemplateResponse: Rendered chat.html template.
    """
    return templates.TemplateResponse("chat.html", {"request": request})