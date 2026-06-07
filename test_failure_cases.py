"""
Test potential failure cases for demo video
"""
from vector_store import retrieve_relevant_chunks, create_collection
from embedding import get_embedding_model

# Initialize
model = get_embedding_model()
collection = create_collection('trine_faq', reset=False)

# Test queries that might fail
test_queries = [
    # Query about specific professor (likely not in docs)
    "What do students say about Professor Smith's teaching style?",
    
    # Query about campus facilities (might not be covered)
    "Where is the best place to study on campus after hours?",
    
    # Query mixing concepts (CPT + scholarship)
    "Can I use CPT earnings to pay for tuition and get scholarships at the same time?",
    
    # Very specific procedural detail
    "What is the exact format of the support letter template for financial proof?",
]

print("=" * 80)
print("TESTING POTENTIAL FAILURE CASES")
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
    
    # Check distances - if all > 1.5, likely poor match
    avg_dist = sum(r.get('distance', 0) for r in results) / len(results)
    if avg_dist > 1.5:
        print(f"  ⚠️ WARNING: High average distance ({avg_dist:.3f}) - likely poor semantic match")
    else:
        print(f"  ️ Average distance: {avg_dist:.3f}")

print("\n" + "=" * 80)
