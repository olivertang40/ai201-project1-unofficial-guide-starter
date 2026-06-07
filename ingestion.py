"""
Document Ingestion Module for Trine University CISI FAQ Pipeline

Loads documents from local text files in doxs/ directory (UTF-8 encoded Chinese FAQ files).

All source content is pre-collected in doxs/ directory - no web scraping required.
Returns cleaned text strings with metadata for downstream chunking.
"""

import os
from typing import List, Dict
from config import DOCS_PATH


def load_text_file(filepath: str, encoding: str = 'utf-8') -> str:
    """
    Load a text file with specified encoding (default UTF-8 for Chinese text).
    
    Args:
        filepath: Path to the text file
        encoding: File encoding (default 'utf-8' for Chinese characters)
    
    Returns:
        Cleaned text content as string
    """
    with open(filepath, 'r', encoding=encoding) as f:
        text = f.read()
    return text.strip()


def clean_text(text: str) -> str:
    """
    Clean raw text by removing HTML entities and unnecessary whitespace.
    
    Removes:
    - HTML entities (&nbsp;, &amp;, &lt;, &gt;, etc.)
    - Multiple consecutive blank lines
    - Leading/trailing whitespace
    
    Keeps:
    - Actual content (questions, answers, descriptions)
    - Single line breaks for readability
    
    Args:
        text: Raw text content
    
    Returns:
        Cleaned text string
    """
    import re
    
    # Replace common HTML entities
    html_entities = {
        '&nbsp;': ' ',
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&#39;': "'",
        '&mdash;': '—',
        '&ndash;': '–',
        '&hellip;': '…',
    }
    
    for entity, replacement in html_entities.items():
        text = text.replace(entity, replacement)
    
    # Remove multiple consecutive blank lines (keep max 2)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Strip leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    # Final cleanup
    text = text.strip()
    
    return text


def load_all_documents(doxs_dir: str = None) -> List[Dict]:
    """
    Load all documents from the doxs directory.
    
    Args:
        doxs_dir: Path to documents directory (default: from config)
    
    Returns:
        List of document dicts with keys:
            - 'text': Cleaned text content
            - 'source': Filename
            - 'topic': Topic category (derived from filename)
    """
    if doxs_dir is None:
        doxs_dir = DOCS_PATH
    
    if not os.path.exists(doxs_dir):
        raise FileNotFoundError(f"Documents directory not found: {doxs_dir}")
    
    documents = []
    
    # Get all .txt files
    txt_files = [f for f in os.listdir(doxs_dir) if f.endswith('.txt')]
    
    if not txt_files:
        raise ValueError(f"No .txt files found in {doxs_dir}")
    
    print(f"\nLoading {len(txt_files)} documents from {doxs_dir}/...")
    
    for filename in sorted(txt_files):
        filepath = os.path.join(doxs_dir, filename)
        
        try:
            # Load raw text
            raw_text = load_text_file(filepath, encoding='utf-8')
            
            # Clean text
            cleaned_text = clean_text(raw_text)
            
            # Extract topic from filename (remove .txt extension)
            topic = filename.replace('.txt', '')
            
            # Create document dict
            doc = {
                'text': cleaned_text,
                'source': filename,
                'topic': topic
            }
            
            documents.append(doc)
            print(f"  [OK] Loaded {filename} ({len(cleaned_text)} characters)")
            
        except Exception as e:
            print(f"  [ERROR] Failed to load {filename}: {str(e)}")
    
    print(f"\nTotal documents loaded: {len(documents)}")
    return documents


if __name__ == '__main__':
    # Test ingestion
    print("=" * 80)
    print("Testing Document Ingestion")
    print("=" * 80)
    
    docs = load_all_documents()
    
    print("\n" + "=" * 80)
    print("SAMPLE DOCUMENT PREVIEW")
    print("=" * 80)
    
    if docs:
        sample = docs[0]
        print(f"\nSource: {sample['source']}")
        print(f"Topic: {sample['topic']}")
        print(f"Length: {len(sample['text'])} characters")
        print(f"\nPreview:\n{sample['text'][:500]}...")
