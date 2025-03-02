"""Model initialization for Gemini and CLIP."""

import google.generativeai as genai
import clip
from config import API_KEY, device
from constants import GEMINI_MODEL_NAME, CLIP_MODEL_NAME

# Configure Gemini
genai.configure(api_key=API_KEY)
gemini_model = genai.GenerativeModel(GEMINI_MODEL_NAME)

# Load CLIP model
clip_model, preprocess = clip.load(CLIP_MODEL_NAME, device=device)