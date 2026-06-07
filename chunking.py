"""
Document Chunking Module for Trine University CISI FAQ Pipeline

Splits documents into chunks using LangChain's RecursiveCharacterTextSplitter
with configuration from planning.md:
- chunk_size: 512 tokens
- chunk_overlap: 100 tokens
- Special handling for Chinese text preservation
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict
import tiktoken


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
                   chunk_size: int = 512, 
                   chunk_overlap: int = 100) -> List[Dict]:
    """
    Split documents into chunks using RecursiveCharacterTextSplitter.
    
    Configuration matches planning.md specifications:
    - 512 token chunk size
    - 100 token overlap
    - Preserves Chinese characters and Q&A structure
    
    Args:
        documents: List of document dicts with 'source', 'topic', 'text' keys
        chunk_size: Target chunk size in tokens (default 512)
        chunk_overlap: Overlap between chunks in tokens (default 100)
    
    Returns:
        List of chunk dicts with keys:
            - 'text': chunk content
            - 'source': original source filename
            - 'topic': topic category
            - 'chunk_index': index within document
            - 'total_chunks': total chunks from this document
    """
    # Initialize the text splitter with token-based splitting
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    
    all_chunks = []
    
    for doc_idx, document in enumerate(documents):
        print(f"\nChunking document {doc_idx + 1}/{len(documents)}: {document['source']}")
        
        # Split the document into chunks
        chunks = text_splitter.split_text(document['text'])
        
        # Filter out empty chunks
        chunks = [chunk for chunk in chunks if chunk.strip()]
        
        print(f"  Created {len(chunks)} chunks")
        
        # Add metadata to each chunk
        for chunk_idx, chunk_text in enumerate(chunks):
            chunk = {
                'text': chunk_text,
                'source': document['source'],
                'topic': document['topic'],
                'chunk_index': chunk_idx,
                'total_chunks': len(chunks),
                'token_count': count_tokens(chunk_text)
            }
            all_chunks.append(chunk)
    
    print(f"\nTotal chunks created: {len(all_chunks)}")
    return all_chunks


def inspect_chunks(chunks: List[Dict], num_samples: int = 5):
    """
    Print sample chunks for manual inspection.
    
    Checks for:
    - Readability and coherence
    - Self-contained meaning
    - HTML artifacts
    - Appropriate chunk size
    
    Args:
        chunks: List of chunk dictionaries
        num_samples: Number of random chunks to display (default 5)
    """
    import random
    
    print("\n" + "=" * 80)
    print(f"CHUNK INSPECTION - {num_samples} Random Samples")
    print("=" * 80)
    
    # Select random samples
    if len(chunks) <= num_samples:
        samples = chunks
    else:
        samples = random.sample(chunks, num_samples)
    
    for i, chunk in enumerate(samples, 1):
        print(f"\n{'─' * 80}")
        print(f"Sample {i}/{num_samples}")
        print(f"{'─' * 80}")
        print(f"Source: {chunk['source']}")
        print(f"Topic: {chunk['topic']}")
        print(f"Chunk Index: {chunk['chunk_index']}/{chunk['total_chunks'] - 1}")
        print(f"Token Count: {chunk['token_count']}")
        print(f"\nContent Preview:")
        print(f"{'─' * 40}")
        
        # Show first 300 characters
        preview_length = min(300, len(chunk['text']))
        print(chunk['text'][:preview_length])
        
        if len(chunk['text']) > preview_length:
            print("...")
        
        # Check for potential issues
        issues = []
        if len(chunk['text'].strip()) == 0:
            issues.append("⚠ EMPTY CHUNK")
        if '&amp;' in chunk['text'] or '&lt;' in chunk['text'] or '&nbsp;' in chunk['text']:
            issues.append("⚠ HTML ENTITIES DETECTED")
        if chunk['token_count'] < 50:
            issues.append("⚠ VERY SHORT CHUNK (< 50 tokens)")
        if chunk['token_count'] > 600:
            issues.append("⚠ VERY LONG CHUNK (> 600 tokens)")
        
        if issues:
            print(f"\nIssues: {' | '.join(issues)}")
        else:
            print(f"\n✓ Chunk looks good")
    
    print("\n" + "=" * 80)


def validate_chunks(chunks: List[Dict]) -> Dict:
    """
    Validate chunk quality and provide statistics.
    
    Args:
        chunks: List of chunk dictionaries
    
    Returns:
        Dictionary with validation statistics
    """
    if not chunks:
        return {"error": "No chunks to validate"}
    
    token_counts = [chunk['token_count'] for chunk in chunks]
    
    stats = {
        'total_chunks': len(chunks),
        'total_documents': len(set(chunk['source'] for chunk in chunks)),
        'avg_tokens': sum(token_counts) / len(token_counts),
        'min_tokens': min(token_counts),
        'max_tokens': max(token_counts),
        'empty_chunks': sum(1 for chunk in chunks if not chunk['text'].strip()),
        'html_artifacts': sum(1 for chunk in chunks if any(entity in chunk['text'] for entity in ['&amp;', '&lt;', '&nbsp;'])),
        'too_short': sum(1 for count in token_counts if count < 50),
        'too_long': sum(1 for count in token_counts if count > 600),
    }
    
    return stats


if __name__ == '__main__':
    # Test the chunking pipeline
    from ingestion import load_all_documents
    
    print("=" * 80)
    print("Testing Document Chunking Pipeline")
    print("=" * 80)
    
    # Load documents
    print("\nStep 1: Loading documents...")
    documents = load_all_documents()
    
    # Chunk documents
    print("\nStep 2: Chunking documents...")
    chunks = chunk_documents(documents, chunk_size=512, chunk_overlap=100)
    
    # Inspect sample chunks
    print("\nStep 3: Inspecting chunks...")
    inspect_chunks(chunks, num_samples=5)
    
    # Validate chunks
    print("\nStep 4: Validating chunk quality...")
    stats = validate_chunks(chunks)
    
    print("\n" + "=" * 80)
    print("CHUNK VALIDATION STATISTICS")
    print("=" * 80)
    print(f"Total chunks: {stats['total_chunks']}")
    print(f"Total documents: {stats['total_documents']}")
    print(f"Average tokens per chunk: {stats['avg_tokens']:.1f}")
    print(f"Min tokens: {stats['min_tokens']}")
    print(f"Max tokens: {stats['max_tokens']}")
    print(f"Empty chunks: {stats['empty_chunks']}")
    print(f"HTML artifacts: {stats['html_artifacts']}")
    print(f"Too short (<50 tokens): {stats['too_short']}")
    print(f"Too long (>600 tokens): {stats['too_long']}")
    
    # Quality check
    print("\n" + "=" * 80)
    print("QUALITY CHECK")
    print("=" * 80)
    
    if stats['total_chunks'] < 50:
        print("⚠ WARNING: Fewer than 50 chunks - chunks may be too large")
    elif stats['total_chunks'] > 2000:
        print("⚠ WARNING: More than 2000 chunks - chunks may be too small")
    else:
        print(f"✓ Chunk count ({stats['total_chunks']}) is in acceptable range (50-2000)")
    
    if stats['empty_chunks'] > 0:
        print(f"⚠ WARNING: Found {stats['empty_chunks']} empty chunks")
    else:
        print("✓ No empty chunks")
    
    if stats['html_artifacts'] > 0:
        print(f"⚠ WARNING: Found {stats['html_artifacts']} chunks with HTML artifacts")
    else:
        print("✓ No HTML artifacts detected")
    
    if stats['too_short'] > 0:
        print(f"⚠ WARNING: {stats['too_short']} chunks are very short (<50 tokens)")
    
    if stats['too_long'] > 0:
        print(f"⚠ WARNING: {stats['too_long']} chunks are very long (>600 tokens)")
    
    if stats['avg_tokens'] < 200:
        print(f"⚠ WARNING: Average chunk size ({stats['avg_tokens']:.0f}) is quite small")
    elif stats['avg_tokens'] > 550:
        print(f"⚠ WARNING: Average chunk size ({stats['avg_tokens']:.0f}) is quite large")
    else:
        print(f"✓ Average chunk size ({stats['avg_tokens']:.0f} tokens) is reasonable")
