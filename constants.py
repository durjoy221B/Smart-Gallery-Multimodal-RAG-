"""Constants used throughout the AI Memory Bot project."""

# API and Model Names
GOOGLE_API_KEY_ENV = "GOOGLE_API_KEY"
GEMINI_MODEL_NAME = "gemini-2.0-flash"
CLIP_MODEL_NAME = "ViT-B/32"



# Device Options
CUDA_DEVICE = "cuda"
CPU_DEVICE = "cpu"



# Directory Paths
CHROMA_DB_PATH = "chroma_db"
UPLOAD_DIRECTORY = "static/images"
STATIC_DIRECTORY = "static"
TEMPLATES_DIRECTORY = "templates"



# Collection Configuration
COLLECTION_NAME = "image_descriptions"
HNSW_SPACE = "cosine"



# URL and Server Settings
BASE_URL = "http://127.0.0.1:8000"
HOST = "127.0.0.1"
PORT = 8000



# File Extensions
JPG_EXTENSION = ".jpg"



# Default Metadata Values
DEFAULT_TAGS = "tags"
DEFAULT_OBJECTS = "objects"
DEFAULT_AMBIENCE = "ambience"
DEFAULT_DOMINANT_COLORS = "#000000,#FFFFFF,#808080"
DEFAULT_FILENAME = "Unknown"
DEFAULT_DATES = "Unknown"
NO_TAGS = "None"
NO_OBJECTS = "None"
NO_AMBIENCE = "Not specified"



# Embedding Weights
ALPHA_WEIGHT = 0.6
BETA_WEIGHT = 0.4



# Search and Truncation Settings
MAX_WORDS = 30
SIMILARITY_THRESHOLD = 0.50
MAX_SEARCH_RESULTS = 5
INITIAL_QUERY_LIMIT = 10



# Prompt Templates
GEMINI_ANALYSIS_PROMPT = """
Analyze this image and provide concise, search-friendly metadata in the exact format below:
- Tags: Provide 3-8 short, specific keywords (e.g., "dog, park, sunny" instead of "cute dog in a sunny park").
- Objects: List 1-6 distinct objects visible in the image (e.g., "tree, car, person"), avoiding vague terms.
- Ambience: Write one short sentence (max 10 words) describing the mood or scene (e.g., "Calm evening by the lake").
- Dominant Colors: List 1-5 prominent colors in hex format (e.g., "#FF0000, #00FF00, #0000FF").
- Uploaded At: Use the provided timestamp {upload_time}.

Return the response in this format:
Tags: tag1, tag2, tag3,tag4, tag5
Objects: object1, object2, object3, object4, object5
Ambience: A not short mood or scene description within 30 to 60 words
Dominant Colors: #hex1, #hex2, #hex3, #hex4, #hex5
Uploaded At: {upload_time}
"""


INTENT_CLASSIFICATION_PROMPT = """
Classify the intent of this user query as 'conversational' or 'image_search':
- 'Conversational' queries seek general chat or answers (e.g., "How's your day?" or "Tell me a joke", "Who are you?"). 
  - If classified as 'conversational', adopt this persona: "I am your Conversational Memory Bot, a friendly AI here to chat about your photos and memories or assist with anything you'd like!"
- 'Image_search' queries aim to find or describe images (e.g., "Show me a dog" or "Find sunset photos").
- If the query is a short list of nouns (e.g., "dog, cat" or "beach"), treat it as 'image_search' unless it clearly seeks a conversation.

Query: "{query}"

Respond with exactly one word: 'conversational' or 'image_search'. If 'conversational', prefix your response with the persona statement: "I am your Conversational Memory Bot, a friendly AI here to chat about your photos and memories or assist with anything you'd like!"
"""

