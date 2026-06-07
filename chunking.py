"""
Document Chunking Module for Trine University CISI FAQ Pipeline

Splits documents into chunks using LangChain's RecursiveCharacterTextSplitter
with configuration from config.py:
- chunk_size: 512 tokens (from config)
- chunk_overlap: 100 tokens (from config)
- Special handling for Chinese text preservation
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict
import tiktoken
from config import CHUNK_SIZE, CHUNK_OVERLAP


def get_tokenizer():
    """
    Get tiktoken encoder for token counting.
    Uses cl100k_base encoding (similar to GPT-4).
    
    Returns:
        Tiktoken encoder instance
    """
    return tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    """
    Count the number of tokens in a text string.
    
    Args:
        text: Input text
    
    Returns:
        Number of tokens
    """
    tokenizer = get_tokenizer()
    return len(tokenizer.encode(text))


def chunk_documents(documents: List[Dict], 
                   chunk_size: int = None, 
                   chunk_overlap: int = None) -> List[Dict]:
    """
    Split documents into chunks using RecursiveCharacterTextSplitter.
    
    Configuration matches planning.md specifications:
    - 512 token chunk size (default from config)
    - 100 token overlap (default from config)
    - Preserves Chinese characters and Q&A structure
    
    Args:
        documents: List of document dicts with 'text', 'source', 'topic' keys
        chunk_size: Size of each chunk in tokens (default: from config)
        chunk_overlap: Overlap between chunks in tokens (default: from config)
    
    Returns:
        List of chunk dicts with metadata
    """
    # Use config defaults if not specified
    if chunk_size is None:
        chunk_size = CHUNK_SIZE
    if chunk_overlap is None:
        chunk_overlap = CHUNK_OVERLAP
    
    print(f"\nChunking documents (size={chunk_size}, overlap={chunk_overlap})...")
    
    all_chunks = []
    
    for doc_idx, doc in enumerate(documents, 1):
        text = doc['text']
        source = doc['source']
        topic = doc['topic']
        
        # Create splitter with token-based splitting
        tokenizer = get_tokenizer()
        
        def token_length(text):
            return len(tokenizer.encode(text))
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=token_length,
            separators=["\n\n", "\n", "。", "？", "！", ".", "?", "!", " ", ""]
        )
        
        # Split document
        split_texts = splitter.split_text(text)
        
        # Create chunk dicts with metadata
        for chunk_idx, chunk_text in enumerate(split_texts):
            # Clean chunk text
            chunk_text = chunk_text.strip()
            
            # Skip empty chunks
            if not chunk_text:
                continue
            
            chunk = {
                'text': chunk_text,
                'source': source,
                'topic': topic,
                'chunk_index': chunk_idx,
                'total_chunks': len(split_texts),
                'token_count': count_tokens(chunk_text)
            }
            
            all_chunks.append(chunk)
        
        print(f"  Document {doc_idx}/{len(documents)}: {source} → {len(split_texts)} chunks")
    
    print(f"\nTotal chunks created: {len(all_chunks)}")
    return all_chunks


def inspect_chunks(chunks: List[Dict], n_samples: int = 5) -> None:
    """
    Print sample chunks for quality inspection.
    
    Args:
        chunks: List of chunk dicts
        n_samples: Number of samples to print (default: 5)
    """
    import random
    
    print("\n" + "=" * 80)
    print(f"INSPECTING {n_samples} RANDOM CHUNKS")
    print("=" * 80)
    
    # Select random samples
    if len(chunks) <= n_samples:
        samples = chunks
    else:
        samples = random.sample(chunks, n_samples)
    
    for i, chunk in enumerate(samples, 1):
        print(f"\n{'─' * 80}")
        print(f"Sample {i}:")
        print(f"{'─' * 80}")
        print(f"Source: {chunk['source']}")
        print(f"Topic: {chunk['topic']}")
        print(f"Chunk Index: {chunk['chunk_index']}/{chunk['total_chunks'] - 1}")
        print(f"Token Count: {chunk['token_count']}")
        print(f"\nContent:\n{chunk['text']}")


def validate_chunks(chunks: List[Dict]) -> Dict:
    """
    Validate chunk quality and detect common issues.
    
    Args:
        chunks: List of chunk dicts
    
    Returns:
        Validation report dict
    """
    report = {
        'total_chunks': len(chunks),
        'empty_chunks': 0,
        'html_artifacts': 0,
        'too_short': 0,
        'too_long': 0,
        'avg_token_count': 0,
        'issues': []
    }
    
    if not chunks:
        report['issues'].append("No chunks to validate!")
        return report
    
    total_tokens = 0
    
    for chunk in chunks:
        text = chunk['text']
        token_count = chunk.get('token_count', count_tokens(text))
        
        # Check for empty chunks
        if not text or len(text.strip()) == 0:
            report['empty_chunks'] += 1
            report['issues'].append(f"Empty chunk found from {chunk['source']}")
        
        # Check for HTML artifacts
        html_patterns = ['<div', '<span', '&amp;', '&nbsp;', '&lt;', '&gt;']
        if any(pattern in text for pattern in html_patterns):
            report['html_artifacts'] += 1
            report['issues'].append(f"HTML artifact in chunk from {chunk['source']}")
        
        # Check token count
        if token_count < 50:
            report['too_short'] += 1
        elif token_count > 600:
            report['too_long'] += 1
        
        total_tokens += token_count
    
    # Calculate average
    report['avg_token_count'] = total_tokens / len(chunks) if chunks else 0
    
    # Add warnings
    if report['total_chunks'] < 50:
        report['issues'].append(
            f"WARNING: Only {report['total_chunks']} chunks total (< 50). "
            f"Chunks may be too large for precise retrieval."
        )
    elif report['total_chunks'] > 2000:
        report['issues'].append(
            f"WARNING: {report['total_chunks']} chunks total (> 2000). "
            f"Chunks may be too small, carrying insufficient semantic signal."
        )
    
    if report['empty_chunks'] > 0:
        report['issues'].append(
            f"Found {report['empty_chunks']} empty chunks. "
            f"Add len(chunk) > 0 filter or check document loading."
        )
    
    if report['html_artifacts'] > 0:
        report['issues'].append(
            f"Found {report['html_artifacts']} chunks with HTML artifacts. "
            f"Improve cleaning before chunking."
        )
    
    if report['too_short'] > len(chunks) * 0.1:
        report['issues'].append(
            f"{report['too_short']} chunks are very short (< 50 tokens). "
            f"Consider larger chunk sizes."
        )
    
    return report


if __name__ == '__main__':
    # Test chunking on sample documents
    from ingestion import load_all_documents
    
    print("=" * 80)
    print("Testing Chunking Module")
    print("=" * 80)
    
    # Load documents
    docs = load_all_documents()
    
    # Chunk documents
    chunks = chunk_documents(docs)
    
    # Inspect samples
    inspect_chunks(chunks, n_samples=5)
    
    # Validate quality
    print("\n" + "=" * 80)
    print("VALIDATION REPORT")
    print("=" * 80)
    
    report = validate_chunks(chunks)
    
    print(f"\nTotal Chunks: {report['total_chunks']}")
    print(f"Average Token Count: {report['avg_token_count']:.1f}")
    print(f"Empty Chunks: {report['empty_chunks']}")
    print(f"HTML Artifacts: {report['html_artifacts']}")
    print(f"Too Short (<50): {report['too_short']}")
    print(f"Too Long (>600): {report['too_long']}")
    
    if report['issues']:
        print(f"\nIssues Found:")
        for issue in report['issues']:
            print(f"  ⚠ {issue}")
    else:
        print("\n✓ No issues detected!")
