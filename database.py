"""Database initialization and configuration for ChromaDB."""

import chromadb
from config import CHROMA_DB_PATH
from constants import COLLECTION_NAME, HNSW_SPACE

chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": HNSW_SPACE}
)