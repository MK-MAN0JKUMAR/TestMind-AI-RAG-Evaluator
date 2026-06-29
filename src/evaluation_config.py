"""
Centralized AI configuration.

This file is the single source of truth for all AI providers,
models, temperatures and future AI components.
"""

# ==========================================================
# Answer Generation
# ==========================================================

ANSWER = {
    "provider": "ollama",
    "model": "llama3.1:8b",
    "temperature": 0.3,
}

# ==========================================================
# Evaluation (Judge LLM)
# ==========================================================

EVALUATION = {
    "provider": "ollama",
    "model": "qwen2.5:3b",
    "temperature": 0.0,
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


