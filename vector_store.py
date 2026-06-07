"""
Vector Store Module for Trine University CISI FAQ Pipeline

Uses ChromaDB to store and retrieve chunk embeddings with metadata.
Supports persistent storage and cosine similarity search.
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import os


def create_collection(collection_name: str = "trine_faq", 
                     reset: bool = False) -> chromadb.Collection:
    """
    Create or get a ChromaDB collection with HNSW index.
    
    Args:
        collection_name: Name of the collection (default: "trine_faq")
        reset: If True, delete existing collection and recreate
    
    Returns:
        ChromaDB Collection instance
    """
    # Initialize persistent client
    client = chromadb.PersistentClient(
        path="./chroma_db",
        settings=Settings(
            anonymized_telemetry=False,
            allow_reset=True
        )
    )
    
    # Reset if requested
    if reset:
        try:
            client.delete_collection(collection_name)
            print(f"Deleted existing collection: {collection_name}")
        except Exception:
            pass
    
    # Get or create collection
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"description": "Trine University CISI FAQ chunks"}
    )
    
    print(f"✓ Collection '{collection_name}' ready")
    return collection


def add_documents(collection: chromadb.Collection, chunks: List[Dict]) -> None:
    """
    Add embedded chunks to ChromaDB collection with metadata.
    
    Args:
        collection: ChromaDB collection instance
        chunks: List of chunk dicts with keys:
            - 'text': chunk content
            - 'embedding': embedding vector (list)
            - 'source': source filename
            - 'topic': topic category
            - 'chunk_index': position in document
            - 'total_chunks': total chunks from this document
    """
    if not chunks:
        print("⚠ No chunks to add")
        return
    
    # Prepare data for ChromaDB
    ids = []
    documents = []
    embeddings = []
    metadatas = []
    
    for i, chunk in enumerate(chunks):
        # Create unique ID
        chunk_id = f"{chunk['source']}_{chunk['chunk_index']}"
        
        ids.append(chunk_id)
        documents.append(chunk['text'])
        embeddings.append(chunk['embedding'])
        
        # Metadata for attribution
        metadata = {
            'source': chunk['source'],
            'topic': chunk['topic'],
            'chunk_index': chunk['chunk_index'],
            'total_chunks': chunk['total_chunks'],
            'token_count': chunk.get('token_count', 0)
        }
        metadatas.append(metadata)
    
    # Add to collection
    print(f"Adding {len(chunks)} chunks to ChromaDB...")
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )
    print(f"✓ Successfully added {len(chunks)} chunks")


def search_collection(collection: chromadb.Collection, 
                     query_embedding: List[float], 
                     k: int = 5) -> List[Dict]:
    """
    Search for top-k most similar chunks using cosine similarity.
    
    Args:
        collection: ChromaDB collection instance
        query_embedding: Query embedding vector
        k: Number of results to return (default: 5)
    
    Returns:
        List of result dicts with keys:
            - 'id': chunk ID
            - 'text': chunk content
            - 'metadata': chunk metadata
            - 'distance': cosine distance (lower is more similar)
    """
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=['documents', 'metadatas', 'distances']
    )
    
    # Format results
    formatted_results = []
    for i in range(len(results['ids'][0])):
        formatted_results.append({
            'id': results['ids'][0][i],
            'text': results['documents'][0][i],
            'metadata': results['metadatas'][0][i],
            'distance': results['distances'][0][i]
        })
    
    return formatted_results


def retrieve_relevant_chunks(collection: chromadb.Collection,
                            model,
                            query_text: str,
                            k: int = 5) -> List[Dict]:
    """
    Complete retrieval pipeline: embed query and search collection.
    
    Args:
        collection: ChromaDB collection instance
        model: SentenceTransformer embedding model
        query_text: User query string
        k: Number of results to return (default: 5)
    
    Returns:
        List of relevant chunk dicts with metadata
    """
    # Embed the query
    query_embedding = model.encode(query_text).tolist()
    
    # Search collection
    results = search_collection(collection, query_embedding, k=k)
    
    return results


if __name__ == '__main__':
    # Test vector store operations
    from embedding import get_embedding_model
    
    print("=" * 80)
    print("Testing Vector Store Module")
    print("=" * 80)
    
    # Load embedding model
    model = get_embedding_model()
    
    # Create collection (reset for testing)
    collection = create_collection(reset=True)
    
    # Sample chunks
    sample_chunks = [
        {
            'text': 'CPT最早开始的日期是哪天？开学的第一天？答：首先要了解Program Start Date与Class Start Date不同',
            'embedding': model.encode('CPT最早开始的日期是哪天？开学的第一天？答：首先要了解Program Start Date与Class Start Date不同').tolist(),
            'source': 'CPT问题.txt',
            'topic': 'CPT问题',
            'chunk_index': 0,
            'total_chunks': 2,
            'token_count': 100
        },
        {
            'text': 'Trine的master项目是否接受学分转入？需要满足什么要求？答：至多转入6学分',
            'embedding': model.encode('Trine的master项目是否接受学分转入？需要满足什么要求？答：至多转入6学分').tolist(),
            'source': '转学分问题.txt',
            'topic': '转学分问题',
            'chunk_index': 0,
            'total_chunks': 1,
            'token_count': 80
        },
        {
            'text': '学校提供的医疗保险怎么样？答：全年保险费约为1300美元，PPO',
            'embedding': model.encode('学校提供的医疗保险怎么样？答：全年保险费约为1300美元，PPO').tolist(),
            'source': '保险问题.txt',
            'topic': '保险问题',
            'chunk_index': 0,
            'total_chunks': 1,
            'token_count': 60
        }
    ]
    
    # Add documents
    add_documents(collection, sample_chunks)
    
    # Test retrieval
    print("\n" + "=" * 80)
    print("TESTING RETRIEVAL")
    print("=" * 80)
    
    test_queries = [
        "CPT什么时候可以开始？",
        "可以转多少学分？",
        "医疗保险费用是多少？"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 80)
        
        results = retrieve_relevant_chunks(collection, model, query, k=2)
        
        for i, result in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"  Source: {result['metadata']['source']}")
            print(f"  Topic: {result['metadata']['topic']}")
            print(f"  Distance: {result['distance']:.4f}")
            print(f"  Text preview: {result['text'][:80]}...")
