"""Dependencies and template setup for FastAPI."""

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request, FastAPI
from constants import TEMPLATES_DIRECTORY

templates = Jinja2Templates(directory=TEMPLATES_DIRECTORY)