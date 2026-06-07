"""
Generation Module for Trine University CISI FAQ Pipeline

Uses Groq's llama-3.3-70b-versatile model to generate grounded answers
from retrieved context. Implements strict grounding to prevent hallucination.
"""

from groq import Groq
from typing import List, Dict
from config import GROQ_API_KEY, LLM_MODEL


# Initialize Groq client
_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query: str, retrieved_chunks: List[Dict]) -> Dict:
    """
    Generate a grounded answer from retrieved chunks.
    
    STRICT GROUNDING CONSTRAINTS:
    - Answer ONLY from retrieved context, NOT from general knowledge
    - Cite sources programmatically (not left to LLM)
    - Decline to answer if context is insufficient
    - Never infer, extrapolate, or fill gaps
    
    Args:
        query: User's question
        retrieved_chunks: List of dicts with keys:
            - 'text': chunk content
            - 'metadata': dict with 'source', 'topic', etc.
            - 'distance': similarity score
    
    Returns:
        Dict with keys:
            - 'answer': Generated response string
            - 'sources': List of source document names
            - 'grounded': Boolean indicating if answer is from context
    """
    
    # Handle no results case
    if not retrieved_chunks:
        return {
            'answer': "Sorry, I couldn't find information related to your question in the documents. Please try rephrasing your question, or confirm whether your question is covered by the CISI FAQ.",
            'sources': [],
            'grounded': False
        }
    
    # Extract unique sources for attribution
    sources = list(set([chunk['metadata']['source'] for chunk in retrieved_chunks]))
    
    # Build system prompt with STRICT grounding instructions
    system_prompt = """You are the Trine University CISI International Student FAQ Assistant.

【ABSOLUTE CONSTRAINTS】
1. You can ONLY use the provided retrieved context to answer questions
2. NEVER use your training knowledge or common sense to answer
3. If there is insufficient information in the retrieved context, you MUST clearly state "I don't have enough information to answer this question"
4. Do not infer, speculate, or fill in information gaps
5. Do not explain what rules "might mean" or "logically should be"
6. Do not provide suggestions, strategies, or personal opinions

【ANSWER FORMAT REQUIREMENTS】
1. Directly quote or closely paraphrase the retrieved content
2. Source citations will be added automatically by the program (you don't need to add them)
3. If multiple sources have conflicting information, clearly point out the differences
4. Keep responses concise, accurate, and faithful to the original text

【PROHIBITED BEHAVIORS】
- Do not say "based on my knowledge" or "generally speaking"
- Do not add reasoning like "this makes sense because..."
- Do not assume user intent or provide additional advice
- Do not create non-existent information

Remember: Your only task is to extract answers from the provided text. If the text doesn't contain an answer, honestly say so."""
    
    # Format retrieved chunks as context
    formatted_chunks = []
    for i, chunk in enumerate(retrieved_chunks, start=1):
        source = chunk['metadata']['source']
        topic = chunk['metadata']['topic']
        distance = chunk.get('distance', 0)
        
        formatted_chunk = (
            f"[{i}] Source: {source} (Topic: {topic}, Relevance: {distance:.3f})\n"
            f"{chunk['text']}"
        )
        formatted_chunks.append(formatted_chunk)
    
    # Build user message with query and context
    context_block = "\n\n".join(formatted_chunks)
    user_message = f"""Question: {query}

---
Relevant Document Content:
---

{context_block}

Please answer the question using ONLY the document content above. If the documents don't contain sufficient information, please say "I don't have enough information to answer this question"."""
    
    # Make API call to Groq
    try:
        response = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.1,  # Low temperature for factual responses
            max_tokens=500,
        )
        
        answer = response.choices[0].message.content.strip()
        
        # Check if model declined to answer
        declined_phrases = [
            "我没有足够的信息",
            "没有足够的信息",
            "无法回答",
            "找不到相关信息",
            "I don't have enough information",
            "cannot answer",
            "not enough information",
            "insufficient information"
        ]
        
        is_declined = any(phrase.lower() in answer.lower() for phrase in declined_phrases)
        
        return {
            'answer': answer,
            'sources': sources,
            'grounded': not is_declined and len(sources) > 0
        }
        
    except Exception as e:
        return {
            'answer': f"Error generating answer: {str(e)}",
            'sources': sources,
            'grounded': False
        }


if __name__ == '__main__':
    # Test generation module
    from ingestion import load_all_documents
    from chunking import chunk_documents
    from embedding import get_embedding_model, embed_chunks
    from vector_store import create_collection, add_documents, retrieve_relevant_chunks
    
    print("=" * 80)
    print("Testing Generation Module")
    print("=" * 80)
    
    # Setup pipeline
    print("\n[Setup] Loading and embedding documents...")
    docs = load_all_documents()
    chunks = chunk_documents(docs)
    model = get_embedding_model()
    embedded_chunks = embed_chunks(model, chunks)
    collection = create_collection(reset=True)
    add_documents(collection, embedded_chunks)
    
    # Test queries
    test_queries = [
        "When can CPT start at the earliest?",
        "What application materials are required?",
        "This question has no answer in the documents"  # Should trigger decline
    ]
    
    for query in test_queries:
        print(f"\n{'=' * 80}")
        print(f"Query: {query}")
        print(f"{'=' * 80}")
        
        # Retrieve chunks
        results = retrieve_relevant_chunks(collection, model, query, k=3)
        
        # Generate response
        response = generate_response(query, results)
        
        print(f"\nAnswer:")
        print(response['answer'])
        print(f"\nSources: {', '.join(response['sources'])}")
        print(f"Grounded: {'✓ Yes' if response['grounded'] else '✗ No'}")
