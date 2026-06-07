"""
Quick retrieval test for demo video queries
"""
from vector_store import retrieve_relevant_chunks, create_collection
from embedding import get_embedding_model

# Initialize
model = get_embedding_model()
collection = create_collection('trine_faq', reset=False)

# Test queries for demo video
test_queries = [
    "When can CPT start at the earliest?",
    "What are the application materials required for Trine University?",
    "What is the minimum financial proof for Trine admission?",
    "What is the step-by-step CISI application process and timeline?",
]

print("=" * 80)
print("RETRIEVAL TEST FOR DEMO VIDEO QUERIES")
print("=" * 80)

for i, query in enumerate(test_queries, 1):
    print(f"\n{i}. Query: {query}")
    print("-" * 80)
    
    results = retrieve_relevant_chunks(collection, model, query, k=5)
    
    print("Top-5 Retrieved Sources:")
    for j, r in enumerate(results, 1):
        source = r['metadata']['source']
        dist = r.get('distance', 0)
        print(f"  [{j}] {source} (distance: {dist:.3f})")
    
    # Check if expected source is in top-5
    if i == 1:
        expected = "CPT问题.txt"
    elif i == 2 or i == 3:
        expected = "申请材料.txt"
    else:
        expected = "申请流程.txt"
    
    sources = [r['metadata']['source'] for r in results]
    if expected in sources:
        print(f"  ✅ SUCCESS: Expected source '{expected}' found at position {sources.index(expected)+1}")
    else:
        print(f"  ❌ FAILED: Expected source '{expected}' NOT in top-5")
        print(f"     Available sources: {', '.join(sources)}")

print("\n" + "=" * 80)
