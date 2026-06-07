"""
Milestone 4 Checkpoint: Retrieval Quality Test

Tests retrieval with 3 evaluation queries and verifies:
1. Returned chunks are actually relevant to the query
2. Distance scores are below 0.5 for top results
3. Can explain why each chunk is relevant
4. Metadata (source) is correct
"""

from ingestion import load_all_documents
from chunking import chunk_documents
from embedding import get_embedding_model, embed_chunks
from vector_store import create_collection, add_documents, retrieve_relevant_chunks


def test_retrieval_checkpoint():
    """
    Test retrieval quality with 3 evaluation queries from planning.md.
    
    Checkpoint requirements:
    - Query vector store with 3 test questions
    - Verify returned chunks visibly relate to each question
    - Explain why each chunk is relevant
    - Top result distance scores should be below 0.5
    """
    
    print("=" * 80)
    print("MILESTONE 4 CHECKPOINT: RETRIEVAL QUALITY TEST")
    print("=" * 80)
    
    # Setup pipeline
    print("\n[Setup] Loading documents, chunking, embedding, storing...")
    docs = load_all_documents()
    chunks = chunk_documents(docs, chunk_size=512, chunk_overlap=100)
    model = get_embedding_model()
    embedded_chunks = embed_chunks(model, chunks)
    collection = create_collection(collection_name="trine_faq", reset=True)
    add_documents(collection, embedded_chunks)
    print(f"✓ Pipeline ready: {len(embedded_chunks)} chunks in vector store\n")
    
    # Test queries from planning.md Evaluation Plan
    test_queries = [
        {
            'query': "CPT最早什么时候可以开始？Program Start Date和Class Start Date有什么区别？",
            'expected_source': 'CPT问题.txt',
            'description': 'CPT eligibility and start dates',
            'key_concepts': ['CPT', 'Program Start Date', 'Class Start Date', 'orientation']
        },
        {
            'query': "申请材料有哪些？财力证明需要多少钱？",
            'expected_source': '申请材料.txt',
            'description': 'Application materials and financial proof',
            'key_concepts': ['材料', '简历', '成绩单', '财力证明', '22000', '$22,000']
        },
        {
            'query': "转学分政策是什么？最多可以转多少学分？GPA要求是多少？",
            'expected_source': '转学分问题.txt',
            'description': 'Transfer credit policy',
            'key_concepts': ['转学分', '6学分', '两门课', 'GPA', '3.0', 'syllabus']
        }
    ]
    
    print("=" * 80)
    print("TESTING 3 EVALUATION QUERIES")
    print("=" * 80)
    
    all_passed = True
    
    for test_num, test_case in enumerate(test_queries, 1):
        print(f"\n{'#' * 80}")
        print(f"TEST #{test_num}: {test_case['description']}")
        print(f"{'#' * 80}")
        print(f"Query: {test_case['query']}")
        print(f"Expected source: {test_case['expected_source']}")
        print(f"Key concepts to look for: {', '.join(test_case['key_concepts'])}")
        
        # Retrieve top-5 chunks
        results = retrieve_relevant_chunks(collection, model, test_case['query'], k=5)
        
        print(f"\nRetrieved {len(results)} chunks:")
        
        # Analyze each result
        top_result_good = False
        
        for i, result in enumerate(results, 1):
            print(f"\n{'─' * 80}")
            print(f"Result #{i}")
            print(f"{'─' * 80}")
            
            # Print metadata
            print(f"Source: {result['metadata']['source']}")
            print(f"Topic: {result['metadata']['topic']}")
            print(f"Distance Score: {result['distance']:.4f}", end="")
            
            # Evaluate distance score
            if result['distance'] < 0.5:
                print(" ✓ EXCELLENT (< 0.5)")
                if i == 1:
                    top_result_good = True
            elif result['distance'] < 0.7:
                print(" ⚠ ACCEPTABLE (0.5-0.7)")
            else:
                print(" ❌ POOR (> 0.7)")
            
            # Print full chunk content
            print(f"\nFull Content ({len(result['text'])} chars):")
            print(f"  {result['text']}")
            
            # Relevance analysis
            print(f"\nRelevance Analysis:")
            
            # Check if source matches expected
            if result['metadata']['source'] == test_case['expected_source']:
                print(f"  ✓ Source matches expected: {test_case['expected_source']}")
            else:
                print(f"  ⚠ Different source: {result['metadata']['source']}")
            
            # Check for keyword overlap
            query_lower = test_case['query'].lower()
            chunk_lower = result['text'].lower()
            
            matching_concepts = []
            for concept in test_case['key_concepts']:
                if concept.lower() in chunk_lower:
                    matching_concepts.append(concept)
            
            if matching_concepts:
                print(f"  ✓ Contains {len(matching_concepts)} key concepts: {', '.join(matching_concepts)}")
            else:
                print(f"  ⚠ No direct keyword matches (semantic similarity only)")
            
            # Explain relevance
            print(f"\n  Why this chunk is relevant:")
            if result['metadata']['source'] == test_case['expected_source']:
                print(f"    → This chunk comes from the expected source document")
                print(f"    → It contains information about: {test_case['description']}")
            elif matching_concepts:
                print(f"    → This chunk shares key terms with the query")
                print(f"    → Concepts found: {', '.join(matching_concepts)}")
            else:
                print(f"    → Semantic similarity matched despite no exact keywords")
        
        # Summary for this test
        print(f"\n{'=' * 80}")
        print(f"TEST #{test_num} SUMMARY")
        print(f"{'=' * 80}")
        
        if top_result_good:
            print(f"✓ PASS - Top result has distance < 0.5")
        else:
            print(f"⚠ WARNING - Top result distance >= 0.5")
            all_passed = False
        
        # Check if expected source is in top 3
        top3_sources = [r['metadata']['source'] for r in results[:3]]
        if test_case['expected_source'] in top3_sources:
            pos = top3_sources.index(test_case['expected_source']) + 1
            print(f"✓ Expected source found at position #{pos} in top-3")
        else:
            print(f"❌ Expected source NOT in top-3 results")
            all_passed = False
        
        print(f"Top-3 sources: {', '.join(top3_sources)}")
    
    # Final verdict
    print(f"\n{'=' * 80}")
    print("CHECKPOINT VERDICT")
    print(f"{'=' * 80}")
    
    if all_passed:
        print("✓ ALL CHECKS PASSED - Retrieval quality is good!")
        print("\nYou can proceed to Milestone 5 (Generation and Interface)")
    else:
        print("⚠ SOME ISSUES DETECTED")
        print("\nRecommendations:")
        print("  - If distance scores are high (> 0.7), try larger chunk sizes")
        print("  - If wrong sources appear, check metadata assignment in vector_store.py")
        print("  - If chunks seem fragmented, review cleaning/chunking logic")
    
    print("=" * 80)
    
    return all_passed


if __name__ == '__main__':
    test_retrieval_checkpoint()
