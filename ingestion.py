"""
Document Ingestion Module for Trine University CISI FAQ Pipeline

Loads documents from local text files in doxs/ directory (UTF-8 encoded Chinese FAQ files).

All source content is pre-collected in doxs/ directory - no web scraping required.
Returns cleaned text strings with metadata for downstream chunking.
"""

import os
from typing import List, Dict


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
    Clean text by removing HTML entities, extra whitespace, and artifacts.
    
    Args:
        text: Raw text content
    
    Returns:
        Cleaned text ready for chunking
    """
    # Replace common HTML entities
    replacements = {
        '&nbsp;': ' ',
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&#39;': "'",
        '&quot;': '"',
    }
    
    for entity, replacement in replacements.items():
        text = text.replace(entity, replacement)
    
    # Remove multiple consecutive blank lines
    while '\n\n\n' in text:
        text = text.replace('\n\n\n', '\n\n')
    
    return text.strip()


def load_all_documents(doxs_dir: str = 'doxs') -> List[Dict]:
    """
    Load all documents from doxs/ directory.
    
    All 10 topic files are pre-collected and stored locally:
    - 学校资质.txt (School Accreditation)
    - 申请相关.txt (Application Related)
    - 申请材料.txt (Application Materials)
    - 奖学金问题.txt (Scholarship Questions)
    - 转学分问题.txt (Transfer Credit Questions)
    - CPT问题.txt (CPT Questions)
    - 身份问题.txt (Immigration Status Questions)
    - Onsite问题.txt (Onsite Course Questions)
    - 保险问题.txt (Insurance Questions)
    - 申请流程.txt (Application Process)
    
    Args:
        doxs_dir: Path to directory containing topic text files
    
    Returns:
        List of dictionaries with keys:
            - 'source': source filename
            - 'topic': topic category
            - 'text': cleaned text content
    """
    documents = []
    
    # Load all text files from doxs/ directory
    if os.path.exists(doxs_dir):
        for filename in sorted(os.listdir(doxs_dir)):
            if filename.endswith('.txt'):
                filepath = os.path.join(doxs_dir, filename)
                topic_name = filename.replace('.txt', '')
                
                print(f"Loading: {filename}")
                raw_text = load_text_file(filepath)
                cleaned_text = clean_text(raw_text)
                
                documents.append({
                    'source': filename,
                    'topic': topic_name,
                    'text': cleaned_text
                })
                print(f"  [OK] Loaded {len(cleaned_text)} characters")
    else:
        print(f"[WARN] Directory '{doxs_dir}' not found!")
    
    print(f"\nTotal documents loaded: {len(documents)}")
    return documents


if __name__ == '__main__':
    # Test the ingestion pipeline
    print("=" * 80)
    print("Testing Document Ingestion Pipeline")
    print("=" * 80)
    
    docs = load_all_documents()
    
    print("\n" + "=" * 80)
    print("Sample Document Preview (first 500 chars):")
    print("=" * 80)
    if docs:
        sample_doc = docs[0]
        print(f"\nSource: {sample_doc['source']}")
        print(f"Topic: {sample_doc['topic']}")
        print(f"Length: {len(sample_doc['text'])} characters")
        print("\nPreview:")
        print(sample_doc['text'][:500])
