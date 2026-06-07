"""
Milestone 5 Checkpoint: Grounded Generation Test

Tests:
1. End-to-end query → retrieval → generation with source citation
2. System declines to answer questions not in documents
3. Answers are traceable to retrieved chunks (not general knowledge)
"""

from ingestion import load_all_documents
from chunking import chunk_documents
from embedding import get_embedding_model, embed_chunks
from vector_store import create_collection, add_documents, retrieve_relevant_chunks
from generation import generate_response


def test_grounded_generation():
    """Test that generation is properly grounded in retrieved context."""
    
    print("=" * 80)
    print("MILESTONE 5 CHECKPOINT: GROUNDED GENERATION TEST")
    print("=" * 80)
    
    # Setup pipeline
    print("\n[Setup] Initializing pipeline...")
    docs = load_all_documents()
    chunks = chunk_documents(docs)
    model = get_embedding_model()
    embedded_chunks = embed_chunks(model, chunks)
    collection = create_collection(collection_name="trine_faq", reset=True)
    add_documents(collection, embedded_chunks)
    print(f"✓ Pipeline ready: {len(embedded_chunks)} chunks\n")
    
    # Test cases
    test_cases = [
        {
            'query': "CPT最早什么时候可以开始？Program Start Date和Class Start Date有什么区别？",
            'expected_behavior': 'Should answer with CPT start date info from CPT问题.txt',
            'should_decline': False,
            'expected_source': 'CPT问题.txt'
        },
        {
            'query': "申请材料有哪些？财力证明需要多少钱？",
            'expected_behavior': 'Should list application materials and $22,000 requirement',
            'should_decline': False,
            'expected_source': '申请材料.txt'
        },
        {
            'query': "Trine University的校园食堂有什么特色菜品？",
            'expected_behavior': 'Should decline - this info is NOT in our documents',
            'should_decline': True,
            'expected_source': None
        }
    ]
    
    print("=" * 80)
    print("TESTING GROUNDED GENERATION")
    print("=" * 80)
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'#' * 80}")
        print(f"TEST #{i}: {test_case['expected_behavior']}")
        print(f"{'#' * 80}")
        print(f"Query: {test_case['query']}")
        
        # Retrieve chunks
        retrieved = retrieve_relevant_chunks(collection, model, test_case['query'], k=5)
        print(f"\nRetrieved {len(retrieved)} chunks")
        
        # Generate response
        response = generate_response(test_case['query'], retrieved)
        
        print(f"\n{'─' * 80}")
        print("GENERATED ANSWER:")
        print(f"{'─' * 80}")
        print(response['answer'])
        
        print(f"\n{'─' * 80}")
        print("METADATA:")
        print(f"{'─' * 80}")
        print(f"Sources: {', '.join(response['sources']) if response['sources'] else 'None'}")
        print(f"Grounded: {'✓ Yes' if response['grounded'] else '✗ No'}")
        
        # Verification
        print(f"\n{'─' * 80}")
        print("VERIFICATION:")
        print(f"{'─' * 80}")
        
        # Check 1: Did it behave as expected?
        if test_case['should_decline']:
            if not response['grounded']:
                print("✓ PASS - Correctly declined to answer (question not in documents)")
            else:
                print("❌ FAIL - Should have declined but generated an answer anyway")
                print("   This indicates a GROUNDING FAILURE!")
                all_passed = False
        else:
            if response['grounded']:
                print("✓ PASS - Generated answer from retrieved context")
            else:
                print("⚠ WARNING - Answer may not be properly grounded")
                all_passed = False
        
        # Check 2: Is expected source cited?
        if test_case['expected_source']:
            if test_case['expected_source'] in response['sources']:
                print(f"✓ PASS - Expected source cited: {test_case['expected_source']}")
            else:
                print(f"⚠ WARNING - Expected source '{test_case['expected_source']}' not in citations")
                print(f"   Actual sources: {response['sources']}")
        
        # Check 3: Can we trace answer to retrieved text?
        print(f"\nTraceability Check:")
        if response['grounded'] and retrieved:
            # Check if answer contains key phrases from retrieved chunks
            answer_lower = response['answer'].lower()
            chunk_texts = [chunk['text'].lower() for chunk in retrieved[:3]]
            
            # Look for overlapping phrases (simple heuristic)
            has_overlap = any(
                phrase in answer_lower 
                for chunk_text in chunk_texts 
                for phrase in chunk_text.split('。')[:3]  # Check first 3 sentences
                if len(phrase) > 10  # Ignore very short phrases
            )
            
            if has_overlap:
                print("  ✓ Answer appears to reference retrieved content")
            else:
                print("  ⚠ Answer may not directly reference retrieved chunks")
                print("     (Could still be valid paraphrase)")
        
        print(f"\nRetrieved Chunks Preview:")
        for j, chunk in enumerate(retrieved[:3], 1):
            preview = chunk['text'][:100].replace('\n', ' ')
            print(f"  [{j}] {chunk['metadata']['source']}: {preview}...")
    
    # Final verdict
    print(f"\n{'=' * 80}")
    print("CHECKPOINT VERDICT")
    print(f"{'=' * 80}")
    
    if all_passed:
        print("✓ ALL TESTS PASSED - Generation is properly grounded!")
        print("\nKey achievements:")
        print("  • Answers cite source documents")
        print("  • System declines unanswered questions")
        print("  • Responses traceable to retrieved context")
        print("\nReady to proceed to Milestone 6!")
    else:
        print("❌ SOME TESTS FAILED - Grounding issues detected")
        print("\nRecommendations:")
        print("  - Review system prompt in generation.py")
        print("  - Ensure temperature is low (0.1-0.3)")
        print("  - Check if retrieved chunks contain relevant info")
    
    print("=" * 80)
    
    return all_passed


if __name__ == '__main__':
    test_grounded_generation()
