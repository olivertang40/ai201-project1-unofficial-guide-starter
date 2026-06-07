"""
Milestone 6: Evaluation Test Script

This script runs all 5 evaluation questions from planning.md and records results.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Import pipeline components
from ingestion import load_all_documents
from chunking import chunk_documents
from embedding import get_embedding_model, embed_chunks
from vector_store import create_collection, retrieve_relevant_chunks
from generation import generate_response
from config import (
    CHROMA_COLLECTION,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


def initialize_pipeline():
    """Initialize the RAG pipeline."""
    print("=" * 80)
    print("Initializing RAG Pipeline for Evaluation")
    print("=" * 80)
    
    # Load documents
    print("\n[1/5] Loading documents...")
    docs = load_all_documents()
    print(f"✓ Loaded {len(docs)} documents")
    
    # Chunk documents
    print("\n[2/5] Chunking documents...")
    chunks = chunk_documents(docs, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    print(f"✓ Created {len(chunks)} chunks")
    
    # Load embedding model
    print("\n[3/5] Loading embedding model...")
    model = get_embedding_model()
    print("✓ Model loaded")
    
    # Embed chunks
    print("\n[4/5] Embedding chunks...")
    embedded_chunks = embed_chunks(model, chunks)
    print(f"✓ Embedded {len(embedded_chunks)} chunks")
    
    # Store in ChromaDB
    print("\n[5/5] Storing in ChromaDB...")
    collection = create_collection(collection_name=CHROMA_COLLECTION, reset=True)
    from vector_store import add_documents
    add_documents(collection, embedded_chunks)
    print(f"✓ Stored {len(embedded_chunks)} chunks")
    
    print("\n" + "=" * 80)
    print("Pipeline Ready!")
    print("=" * 80 + "\n")
    
    return collection, model


def run_evaluation_question(collection, model, question_num, question, expected_answer):
    """Run a single evaluation question and return results."""
    print(f"\n{'='*80}")
    print(f"QUESTION #{question_num}")
    print(f"{'='*80}")
    print(f"\nQuestion: {question}")
    print(f"\nExpected Answer:")
    print(expected_answer)
    print("-" * 80)
    
    # Retrieve relevant chunks
    retrieved = retrieve_relevant_chunks(collection, model, question, k=5)
    print(f"\nRetrieved {len(retrieved)} chunks:")
    for i, chunk in enumerate(retrieved, 1):
        source = chunk['metadata'].get('source', 'Unknown')
        print(f"  [{i}] {source}")
    
    # Generate response
    print("\nGenerating response...")
    response = generate_response(question, retrieved)
    
    print("\n" + "-" * 80)
    print("ACTUAL RESPONSE:")
    print("-" * 80)
    print(response['answer'])
    print("\n" + "-" * 80)
    print(f"SOURCES: {response['sources']}")
    print(f"GROUNDED: {response['grounded']}")
    print("-" * 80)
    
    # Return structured result
    return {
        'question': question,
        'expected': expected_answer,
        'actual': response['answer'],
        'sources': response['sources'],
        'grounded': response['grounded']
    }


def main():
    """Run all evaluation questions."""
    # Initialize pipeline
    collection, model = initialize_pipeline()
    
    # Define 5 evaluation questions from planning.md
    evaluation_questions = [
        {
            'num': 1,
            'question': "What are the CPT eligibility requirements and earliest start date at Trine University?",
            'expected': """Key facts that must be included: 
(1) Program Start Date differs from Class Start Date - CPT can begin on Program Start Date (orientation date), not Class Start Date. Example: Fall 2022 had Program Start Date 8/8/2022 and Class Start Date 8/22/2022. 
(2) CPT can be applied anytime during semester except last 30 days. 
(3) Break periods do NOT affect CPT usage. 
(4) Only Experiential track requires CPT work. 
(5) If student loses job, must contact DSO immediately to pause CPT and drop course (grade shows as W, doesn't affect GPA)."""
        },
        {
            'num': 2,
            'question': "What are the application materials required for Trine University and what is the minimum financial proof amount?",
            'expected': """Must mention ALL of these: 
(1) Resume - no specific format required, just list academic and work experience. 
(2) Transcripts - must be authenticated and translated if from China. 
(3) Diploma. 
(4) Personal Statement - approximately 350 words, explain why Trine and chosen major, DO NOT mention H1B or Day 1 CPT. 
(5) Passport and visa copies - expired visa is OK. 
(6) Financial proof - minimum $22,000 required. If financial documents are not in student's own name, additional support letter is needed."""
        },
        {
            'num': 3,
            'question': "What is the transfer credit policy at Trine University and when can students apply for it?",
            'expected': """Critical requirements: 
(1) Maximum 6 credits (equivalent to two courses) can be transferred. 
(2) Transferred courses must be master's level and similar to Trine courses. 
(3) Student must achieve 3.0+ GPA in first semester at Trine BEFORE applying for transfer credits. 
(4) Application happens AFTER first semester ends. 
(5) Must submit original school transcripts and syllabus. 
(6) Important: During first semester course selection, communicate with academic advisor to avoid taking courses you hope to waive later."""
        },
        {
            'num': 4,
            'question': "What are the health insurance requirements for F-1 international students at Trine and can students use their own insurance?",
            'expected': """Mandatory facts: 
(1) ALL F-1 visa students MUST have health insurance through Trine University. 
(2) Cost is approximately $1,300 per year. 
(3) Plan is PPO type with United Health Care. 
(4) Waivers are ONLY provided for sponsored students (government sponsor or employer sponsorship). 
(5) Individual and private insurance plans purchased by students DO NOT qualify for waiver. 
(6) Dental and vision insurance are NOT included but can be added for extra fee."""
        },
        {
            'num': 5,
            'question': "What is the step-by-step application process for Trine University through CISI and how long does admission take?",
            'expected': """Must include these exact steps: 
(1) Register account on Trine website. 
(2) Fill personal information. 
(3) Select "apply through CISI" to waive application fee - choose International Agent "CISI & info@cisi-edu.org". 
(4) Upload application materials. 
(5) Email admission officer sharmasrijana@trine.edu and copy trine@cisi-edu.org with template including reference number. 
Timeline: CISI contacts admission every Tuesday and Friday. Fastest admission decision can be received in just 12 hours."""
        }
    ]
    
    # Run all questions
    results = []
    for q in evaluation_questions:
        result = run_evaluation_question(
            collection, model,
            q['num'],
            q['question'],
            q['expected']
        )
        results.append(result)
        
        # Ask user to judge accuracy
        print("\n" + "=" * 80)
        print("ACCURACY JUDGMENT REQUIRED")
        print("=" * 80)
        print("\nPlease review the response above and judge its accuracy:")
        print("  - ACCURATE: Response includes all key facts from expected answer")
        print("  - PARTIALLY ACCURATE: Response includes some but not all key facts")
        print("  - INACCURATE: Response is missing most key facts or contains errors")
        print("\n(Note: This judgment will be recorded in README.md)")
        input("\nPress Enter to continue to next question...")
    
    # Summary
    print("\n" + "=" * 80)
    print("EVALUATION COMPLETE")
    print("=" * 80)
    print(f"\nTotal questions tested: {len(results)}")
    print("\nResults saved. Please record accuracy judgments in README.md")
    print("=" * 80)


if __name__ == "__main__":
    main()
