"""Configuration settings for the AI Memory Bot project."""

import os
import torch
from dotenv import load_dotenv
from constants import GOOGLE_API_KEY_ENV, CUDA_DEVICE, CPU_DEVICE, CHROMA_DB_PATH, UPLOAD_DIRECTORY

load_dotenv()

# Gemini Configuration
API_KEY = os.getenv(GOOGLE_API_KEY_ENV)
if not API_KEY:
    raise RuntimeError("Google Gemini API Key not set.")

# Device configuration
device = CUDA_DEVICE if torch.cuda.is_available() else CPU_DEVICE

# ChromaDB Configuration
CHROMA_DB_PATH = CHROMA_DB_PATH

# File Storage
UPLOAD_DIRECTORY = UPLOAD_DIRECTORY
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)