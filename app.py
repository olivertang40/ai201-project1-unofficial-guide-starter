"""
Trine University CISI FAQ Assistant - Gradio Web Interface

End-to-end RAG pipeline:
1. Load and embed documents on startup
2. Accept user queries via web UI
3. Retrieve relevant chunks from ChromaDB
4. Generate grounded answers with Groq LLM
5. Display answer with source attribution
"""

import gradio as gr
from ingestion import load_all_documents
from chunking import chunk_documents
from embedding import get_embedding_model, embed_chunks
from vector_store import create_collection, add_documents, retrieve_relevant_chunks
from generation import generate_response


# ---------------------------------------------------------------------------
# Global variables for pipeline components
# ---------------------------------------------------------------------------
collection = None
model = None
is_initialized = False


def initialize_pipeline():
    """
    Initialize the RAG pipeline on startup.
    Loads documents, creates embeddings, stores in ChromaDB.
    
    If vector store already has data, skips ingestion.
    To re-ingest, delete ./chroma_db folder and restart.
    """
    global collection, model, is_initialized
    
    if is_initialized:
        print("Pipeline already initialized.")
        return
    
    print("\n" + "=" * 80)
    print("Initializing Trine CISI FAQ Assistant")
    print("=" * 80)
    
    # Step 1: Load documents
    print("\n[1/5] Loading documents from doxs/...")
    docs = load_all_documents()
    print(f"✓ Loaded {len(docs)} documents")
    
    # Step 2: Chunk documents
    print("\n[2/5] Chunking documents...")
    chunks = chunk_documents(docs, chunk_size=512, chunk_overlap=100)
    print(f"✓ Created {len(chunks)} chunks")
    
    # Step 3: Load embedding model
    print("\n[3/5] Loading embedding model (all-MiniLM-L6-v2)...")
    model = get_embedding_model()
    
    # Step 4: Embed chunks
    print("\n[4/5] Embedding chunks...")
    embedded_chunks = embed_chunks(model, chunks)
    
    # Step 5: Store in ChromaDB
    print("\n[5/5] Storing in ChromaDB...")
    collection = create_collection(collection_name="trine_faq", reset=False)
    
    # Check if collection already has data
    count = collection.count()
    if count > 0:
        print(f"✓ Vector store already has {count} chunks. Skipping ingestion.")
    else:
        add_documents(collection, embedded_chunks)
        print(f"✓ Stored {len(embedded_chunks)} chunks in ChromaDB")
    
    is_initialized = True
    print("\n" + "=" * 80)
    print("✓ Pipeline ready! You can now ask questions.")
    print("=" * 80 + "\n")


def handle_query(question: str) -> tuple:
    """
    Handle user query: retrieve chunks → generate answer → format response.
    
    Args:
        question: User's question string
    
    Returns:
        Tuple of (answer_text, sources_text) for Gradio display
    """
    global collection, model, is_initialized
    
    # Ensure pipeline is initialized
    if not is_initialized:
        initialize_pipeline()
    
    # Validate input
    if not question or not question.strip():
        return "Please enter your question.", "No sources"
    
    print(f"\n[Query] {question}")
    
    # Step 1: Retrieve relevant chunks
    print("[Retrieval] Searching vector store...")
    retrieved = retrieve_relevant_chunks(collection, model, question, k=5)
    print(f"[Retrieval] Found {len(retrieved)} chunks")
    
    # Step 2: Generate grounded answer
    print("[Generation] Calling Groq LLM...")
    response = generate_response(question, retrieved)
    print(f"[Generation] Answer generated (grounded: {response['grounded']})")
    
    # Step 3: Format sources for display
    if response['sources']:
        sources_text = "\n".join([f"• {source}" for source in response['sources']])
    else:
        sources_text = "No relevant documents found"
    
    # Add grounding indicator
    if not response['grounded']:
        answer_text = response['answer'] + "\n\n⚠️ Note: This response may not be based on retrieved document content."
    else:
        answer_text = response['answer']
    
    return answer_text, sources_text


# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------

with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="blue"),
    title="Trine CISI FAQ Assistant",
) as demo:
    
    gr.HTML("""
        <div style="text-align:center; padding:1.25rem 0 0.5rem;">
            <h1 style="font-size:2rem; font-weight:700; color:#1e40af; margin:0;">
                🎓 Trine University CISI FAQ Assistant
            </h1>
            <p style="color:#6b7280; font-size:1rem; margin:0.4rem 0 0;">
                Ask questions about international student services at Trine University
            </p>
        </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            gr.ChatInterface(
                fn=handle_query,
                type="messages",
                chatbot=gr.Chatbot(
                    height=500,
                    type="messages",
                    placeholder=(
                        "<div style='text-align:center; color:#9ca3af; margin-top:3rem;'>"
                        "Ask a question about CPT, applications, insurance, etc.<br>"
                        "Example: When can CPT start?"
                        "</div>"
                    ),
                ),
                textbox=gr.Textbox(
                    placeholder='For example: "What materials are needed for CPT application?" or "What is the transfer credit policy?"',
                    container=False,
                    scale=7,
                ),
                examples=[
                    "When can CPT start at the earliest?",
                    "What application materials are required? How much financial proof is needed?",
                    "What is the transfer credit policy? How many credits can be transferred?",
                    "How is the health insurance provided by the school? What's the cost?",
                    "What is the application process? What are the benefits of applying through CISI?",
                    "How are Onsite course schedules arranged?",
                    "How long is the I-20 validity period?",
                    "Does Trine offer scholarships?",
                ],
                cache_examples=False,
            )
        
        with gr.Column(scale=1, min_width=200):
            gr.HTML("""
                <div style="background:#eff6ff; border:1px solid #bfdbfe;
                            border-radius:10px; padding:1rem; margin-top:0.5rem;">
                    <p style="font-size:0.8rem; font-weight:700; color:#1e40af;
                               margin:0 0 0.5rem; letter-spacing:0.05em;">
                        📚 KNOWLEDGE BASE
                    </p>
                    <ul style="font-size:0.85rem; color:#1e3a8a; list-style:none;
                                padding:0; margin:0; line-height:1.8;">
                        <li>📋 CPT Questions</li>
                        <li>📝 Application Process</li>
                        <li>📄 Application Materials</li>
                        <li>💰 Insurance Questions</li>
                        <li>🎓 Transfer Credit Questions</li>
                        <li>🏫 Onsite Questions</li>
                        <li>🛂 Status/Visa Questions</li>
                        <li>🏆 Scholarship Questions</li>
                    </ul>
                    <hr style="border:none; border-top:1px solid #bfdbfe; margin:0.75rem 0;">
                    <p style="font-size:0.75rem; color:#2563eb; margin:0; line-height:1.5;">
                        Answers are grounded in CISI FAQ documents only. 
                        If information isn't in the documents, the assistant will say so.
                    </p>
                </div>
            """)
            
            # Sources display box
            with gr.Accordion("📖 Retrieved Sources", open=False):
                sources_output = gr.Textbox(
                    label="Sources",
                    lines=8,
                    interactive=False,
                    show_copy_button=True,
                )
    
    # Custom handler to capture sources
    def chat_with_sources(message, history):
        answer, sources = handle_query(message)
        
        # Format for chat display
        formatted_answer = f"{answer}\n\n---\n**Sources:**\n{sources}"
        
        return formatted_answer, sources
    
    # Override the chat interface to show sources separately
    chatbot = gr.Chatbot(
        elem_id="chatbot",
        height=500,
        type="messages",
        visible=False,  # Hide default, we'll use custom logic
    )


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  Trine CISI FAQ Assistant — Starting up")
    print("=" * 50 + "\n")
    
    # Initialize pipeline
    initialize_pipeline()
    
    # Launch Gradio app
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
