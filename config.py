"""
Configuration Module for Trine University CISI FAQ Assistant

Centralizes all configuration parameters for the RAG pipeline.
Uses environment variables for sensitive data (API keys).
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ---------------------------------------------------------------------------
# LLM Configuration
# ---------------------------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama-3.3-70b-versatile"

# Validation
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in .env file. "
        "Please create a .env file with your Groq API key.\n"
        "Get your free API key from: https://console.groq.com/keys"
    )

# ---------------------------------------------------------------------------
# Embedding Model Configuration
# ---------------------------------------------------------------------------
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ---------------------------------------------------------------------------
# Vector Store Configuration
# ---------------------------------------------------------------------------
CHROMA_COLLECTION = "trine_faq"
CHROMA_PATH = "./chroma_db"

# ---------------------------------------------------------------------------
# Retrieval Configuration
# ---------------------------------------------------------------------------
N_RESULTS = 5  # Top-k results to retrieve

# ---------------------------------------------------------------------------
# Document Configuration
# ---------------------------------------------------------------------------
DOCS_PATH = "./doxs"

# ---------------------------------------------------------------------------
# Chunking Configuration
# ---------------------------------------------------------------------------
CHUNK_SIZE = 512      # tokens per chunk
CHUNK_OVERLAP = 100   # overlap between chunks

# ---------------------------------------------------------------------------
# Application Configuration
# ---------------------------------------------------------------------------
APP_HOST = "0.0.0.0"
APP_PORT = 7860
APP_TITLE = "Trine CISI FAQ Assistant"
APP_DESCRIPTION = "Ask questions about international student services at Trine University"
