"""
Centralized AI configuration.

This file is the single source of truth for AI providers,
models, retrieval settings, chunking and future AI components.
"""

# ==========================================================
# Active Providers
# ==========================================================

ANSWER_PROVIDER = "ollama"

EVALUATION_PROVIDER = "ollama"


# ==========================================================
# Provider Configurations
# ==========================================================

PROVIDERS = {

    # ------------------------------
    # Ollama
    # ------------------------------
    "ollama": {

        "answer": {
            "model": "llama3.1:8b",
            "temperature": 0.3,
        },

        "evaluation": {
            "model": "qwen2.5:3b",
            "temperature": 0.0,
        },
    },

    # ------------------------------
    # Groq
    # ------------------------------
    "groq": {

        "api_key_env": "GROQ_API_KEY",

        "answer": {
            "model": "llama-3.3-70b-versatile",
            "temperature": 0.3,
        },

        "evaluation": {
            "model": "llama-3.3-70b-versatile",
            "temperature": 0.0,
        },
    },

    # ------------------------------
    # Future Providers
    # ------------------------------
    # "openai": {},
    # "gemini": {},
    # "anthropic": {},
    # "azure_openai": {},
}

# ==========================================================
# Embedding
# ==========================================================

EMBEDDING = {
    "provider": "huggingface",
    "model": "sentence-transformers/all-MiniLM-L6-v2",
}

# ==========================================================
# Retrieval
# ==========================================================

RETRIEVAL = {
    "vector_db": "faiss",
    "strategy": "similarity",
    "top_k": 3,
    "similarity_threshold": 1.5,
}

# ==========================================================
# Chunking
# ==========================================================

CHUNKING = {
    "chunk_size": 300,
    "chunk_overlap": 50,
}

# ==========================================================
# Future AI Components
# ==========================================================

RERANKER = {
    "enabled": False,
    "provider": None,
    "model": None,
}

OCR = {
    "enabled": False,
    "provider": None,
    "model": None,
}

VISION = {
    "enabled": False,
    "provider": None,
    "model": None,
}