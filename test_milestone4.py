"""
Milestone 4 Integration Test: Full Pipeline from Ingestion to Retrieval

Tests:
1. Load documents from doxs/
2. Chunk documents
3. Embed chunks with all-MiniLM-L6-v2
4. Store in ChromaDB with metadata
5. Test retrieval with sample queries
6. Verify results are relevant
"""

from ingestion import load_all_documents
from chunking import chunk_documents
from embedding import get_embedding_model, embed_chunks
from vector_store import create_collection, add_documents, retrieve_relevant_chunks


def test_milestone4():
    """Run complete Milestone 4 pipeline test."""
    
    print("=" * 80)
    print("MILESTONE 4: EMBEDDING AND RETRIEVAL PIPELINE TEST")
    print("=" * 80)
    
    # Step 1: Load documents
    print("\n[Step 1] Loading documents...")
    docs = load_all_documents()
    print(f"✓ Loaded {len(docs)} documents")
    
    # Step 2: Chunk documents
    print("\n[Step 2] Chunking documents...")
    chunks = chunk_documents(docs, chunk_size=512, chunk_overlap=100)
    print(f"✓ Created {len(chunks)} chunks")
    
    # Step 3: Load embedding model
    print("\n[Step 3] Loading embedding model...")
    model = get_embedding_model()
    
    # Step 4: Embed chunks
    print("\n[Step 4] Embedding chunks...")
    embedded_chunks = embed_chunks(model, chunks)
    print(f"✓ Embedded {len(embedded_chunks)} chunks")
    
    # Step 5: Create ChromaDB collection
    print("\n[Step 5] Creating ChromaDB collection...")
    collection = create_collection(collection_name="trine_faq", reset=True)
    
    # Step 6: Add documents to vector store
    print("\n[Step 6] Adding chunks to ChromaDB...")
    add_documents(collection, embedded_chunks)
    print(f"✓ Stored {len(embedded_chunks)} chunks in ChromaDB")
    
    # Step 7: Test retrieval with evaluation questions
    print("\n" + "=" * 80)
    print("[Step 7] TESTING RETRIEVAL WITH EVALUATION QUESTIONS")
    print("=" * 80)
    
    # Test queries from planning.md Evaluation Plan
    test_queries = [
        ("CPT eligibility and start date", "CPT最早什么时候可以开始？"),
        ("Application materials", "申请材料有哪些？需要多少财力证明？"),
        ("Transfer credit policy", "转学分政策是什么？最多可以转多少学分？"),
        ("Health insurance", "医疗保险要求是什么？费用多少？"),
        ("Application process", "申请流程是怎样的？通过CISI申请有什么好处？")
    ]
    
    for topic, query in test_queries:
        print(f"\n{'─' * 80}")
        print(f"Topic: {topic}")
        print(f"Query: {query}")
        print(f"{'─' * 80}")
        
        # Retrieve top-5 results
        results = retrieve_relevant_chunks(collection, model, query, k=5)
        
        print(f"\nTop {len(results)} Results:")
        for i, result in enumerate(results, 1):
            print(f"\n  Result {i}:")
            print(f"    Source: {result['metadata']['source']}")
            print(f"    Topic: {result['metadata']['topic']}")
            print(f"    Distance: {result['distance']:.4f} (lower = more similar)")
            
            # Show text preview
            text_preview = result['text'][:150].replace('\n', ' ')
            print(f"    Preview: {text_preview}...")
        
        # Check if results are from relevant sources
        relevant_sources = [r['metadata']['source'] for r in results[:3]]
        print(f"\n  Top 3 sources: {', '.join(relevant_sources)}")
    
    # Step 8: Verify retrieval quality
    print("\n" + "=" * 80)
    print("RETRIEVAL QUALITY VERIFICATION")
    print("=" * 80)
    
    # Test specific known facts
    verification_tests = [
        {
            'query': 'CPT Program Start Date',
            'expected_source': 'CPT问题.txt',
            'description': 'Should retrieve CPT start date information'
        },
        {
            'query': 'financial proof $22000',
            'expected_source': '申请材料.txt',
            'description': 'Should retrieve financial proof requirements'
        },
        {
            'query': 'transfer credit 6 credits GPA 3.0',
            'expected_source': '转学分问题.txt',
            'description': 'Should retrieve transfer credit policy'
        }
    ]
    
    print("\nVerification Tests:")
    passed = 0
    total = len(verification_tests)
    
    for test in verification_tests:
        print(f"\nTest: {test['description']}")
        print(f"  Query: {test['query']}")
        
        results = retrieve_relevant_chunks(collection, model, test['query'], k=3)
        top_source = results[0]['metadata']['source'] if results else None
        
        if top_source == test['expected_source']:
            print(f"  ✓ PASS - Top result from expected source: {top_source}")
            passed += 1
        else:
            print(f"  ⚠ PARTIAL - Top result: {top_source}, Expected: {test['expected_source']}")
            # Check if expected source is in top 3
            sources_in_top3 = [r['metadata']['source'] for r in results[:3]]
            if test['expected_source'] in sources_in_top3:
                print(f"           But expected source found in top 3 results")
                passed += 0.5
    
    print(f"\n{'=' * 80}")
    print(f"VERIFICATION RESULT: {passed}/{total} tests passed")
    print(f"{'=' * 80}")
    
    if passed >= total * 0.8:
        print("✓ RETRIEVAL QUALITY IS GOOD - Ready for Milestone 5!")
    else:
        print("⚠ Some retrieval issues detected - review before proceeding")
    
    print("\n" + "=" * 80)
    print("MILESTONE 4 COMPLETE")
    print("=" * 80)
    print(f"Total chunks in vector store: {len(embedded_chunks)}")
    print(f"Collection name: trine_faq")
    print(f"Embedding model: all-MiniLM-L6-v2")
    print(f"Retrieval method: Cosine similarity (top-k=5)")
    print("=" * 80)


if __name__ == '__main__':
    test_milestone4()
