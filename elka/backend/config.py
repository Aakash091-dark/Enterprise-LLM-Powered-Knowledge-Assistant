import os
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
LLAMA_MODEL_ID = "meta-llama/Llama-3.1-8B"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

VECTOR_STORE_PATH = "data/vector_store/index.faiss"
VECTOR_SOURCES_PATH = "data/vector_store/sources.pkl"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
