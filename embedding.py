"""
Embedding Module for Trine University CISI FAQ Pipeline

Uses sentence-transformers all-MiniLM-L6-v2 model to embed text chunks.
Model runs locally with no API key required.
Produces 768-dimensional vectors suitable for similarity search.
"""

from sentence_transformers import SentenceTransformer
from typing import List, Dict
import numpy as np
from config import EMBEDDING_MODEL


def get_embedding_model(model_name: str = None) -> SentenceTransformer:
    """
    Load the sentence-transformers embedding model.
    
    Args:
        model_name: Name of the pre-trained model (default: from config)
    
    Returns:
        SentenceTransformer model instance
    """
    if model_name is None:
        model_name = EMBEDDING_MODEL
    
    print(f"Loading embedding model: {model_name}")
    model = SentenceTransformer(model_name)
    print(f"✓ Model loaded successfully (dimension: {model.get_sentence_embedding_dimension()})")
    return model


def embed_texts(model: SentenceTransformer, texts: List[str]) -> np.ndarray:
    """
    Embed a list of text strings into vectors.
    
    Args:
        model: Loaded SentenceTransformer model
        texts: List of text strings to embed
    
    Returns:
        Numpy array of embeddings (shape: [num_texts, embedding_dim])
    """
    if not texts:
        return np.array([])
    
    print(f"Embedding {len(texts)} texts...")
    embeddings = model.encode(texts, show_progress_bar=True)
    print(f"✓ Generated embeddings with shape: {embeddings.shape}")
    
    return embeddings


def embed_chunks(model: SentenceTransformer, chunks: List[Dict]) -> List[Dict]:
    """
    Embed all chunks and attach embeddings to chunk metadata.
    
    Args:
        model: Loaded SentenceTransformer model
        chunks: List of chunk dicts with 'text' key
    
    Returns:
        List of chunk dicts with added 'embedding' key
    """
    # Extract texts from chunks
    texts = [chunk['text'] for chunk in chunks]
    
    # Generate embeddings
    embeddings = embed_texts(model, texts)
    
    # Attach embeddings to chunks
    for i, chunk in enumerate(chunks):
        chunk['embedding'] = embeddings[i].tolist()
    
    print(f"✓ Embedded {len(chunks)} chunks")
    return chunks


if __name__ == '__main__':
    # Test embedding on sample texts
    print("=" * 80)
    print("Testing Embedding Module")
    print("=" * 80)
    
    # Load model
    model = get_embedding_model()
    
    # Sample texts
    sample_texts = [
        "CPT最早开始的日期是哪天？开学的第一天？",
        "Program Start Date与Class Start Date不同",
        "Trine的master项目是否接受学分转入？"
    ]
    
    # Embed texts
    embeddings = embed_texts(model, sample_texts)
    
    print("\n" + "=" * 80)
    print("EMBEDDING RESULTS:")
    print("=" * 80)
    print(f"Number of texts: {len(sample_texts)}")
    print(f"Embedding dimension: {embeddings.shape[1]}")
    print(f"Embedding shape: {embeddings.shape}")
    
    # Calculate cosine similarity between first two texts
    from numpy.linalg import norm
    sim_01 = np.dot(embeddings[0], embeddings[1]) / (norm(embeddings[0]) * norm(embeddings[1]))
    sim_02 = np.dot(embeddings[0], embeddings[2]) / (norm(embeddings[0]) * norm(embeddings[2]))
    
    print(f"\nCosine similarity (text 0 vs text 1): {sim_01:.4f}")
    print(f"Cosine similarity (text 0 vs text 2): {sim_02:.4f}")
    print("\nNote: Similar sentences should have similarity > 0.7")
