# The Unofficial Guide — Project 1

> **Project:** Trine CISI FAQ Assistant  
> **Author:** Oliver Tang
> **Date:** June 2026  
> **Milestone:** Complete (Milestones 1-6)

---

## Domain

**International Student Survival Guide for Trine University** - This domain provides comprehensive guidance for international students navigating Trine University's complex processes including admissions, scholarships, credit transfers, CPT/OPT work authorization, immigration status maintenance, on-campus requirements, health insurance, and application procedures.

This knowledge is exceptionally valuable because official university resources typically present information in fragmented, legalistic language without practical insights from actual student experiences. International students face unique challenges such as understanding visa regulations, managing F-1 status requirements, accessing scholarships specific to their status, and navigating cultural adjustments that aren't adequately addressed in formal documentation. The gap between official policy and real-world implementation creates confusion and anxiety, making peer-to-peer knowledge sharing essential for successful academic and professional outcomes.

---

## Document Sources

| #   | Source                                                    | Type            | URL or file path    |
| --- | --------------------------------------------------------- | --------------- | ------------------- |
| 1   | CISI Trine University FAQ - School Accreditation          | Local text file | doxs/学校资质.txt   |
| 2   | CISI Trine University FAQ - Application Related Questions | Local text file | doxs/申请相关.txt   |
| 3   | CISI Trine University FAQ - Application Materials         | Local text file | doxs/申请材料.txt   |
| 4   | CISI Trine University FAQ - Scholarship Information       | Local text file | doxs/奖学金问题.txt |
| 5   | CISI Trine University FAQ - Transfer Credit Policy        | Local text file | doxs/转学分问题.txt |
| 6   | CISI Trine University FAQ - CPT Questions                 | Local text file | doxs/CPT问题.txt    |
| 7   | CISI Trine University FAQ - Immigration Status            | Local text file | doxs/身份问题.txt   |
| 8   | CISI Trine University FAQ - Onsite Course Requirements    | Local text file | doxs/Onsite问题.txt |
| 9   | CISI Trine University FAQ - Health Insurance              | Local text file | doxs/保险问题.txt   |
| 10  | CISI Trine University FAQ - Application Process           | Local text file | doxs/申请流程.txt   |

---

## Chunking Strategy

**Chunk size:** 512 tokens

**Overlap:** 100 tokens

**Why these choices fit your documents:** The document corpus contains mixed formats: structured FAQ-style content with Q&A pairs. A 512-token chunk size balances several needs: (1) it captures complete Q&A pairs without splitting critical multi-sentence answers across chunks, (2) it accommodates typical FAQ entry lengths while preserving context around key advice, and (3) it keeps individual policy descriptions intact. The 100-token overlap ensures that when a procedure spans two paragraphs or when an answer references a prior statement, the semantic connection is preserved for accurate retrieval. This configuration works well for sentence-transformers models which perform optimally with chunks under 512 tokens.

**Preprocessing:** No HTML stripping needed (all sources are plain text). UTF-8 encoding used throughout to preserve Chinese characters. Empty chunks filtered out during processing.

**Final chunk count:** 12 chunks across 10 documents

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers library (v3.4.1)

**Production tradeoff reflection:** For a production system serving international students globally, I would evaluate several tradeoffs: (1) **Multilingual support**: Many international students may query in their native language before translating; models like multilingual-e5-large or OpenAI's text-embedding-3-large handle cross-lingual retrieval better but increase computational cost 3-5x. (2) **Domain specificity**: Legal/immigration terminology (CPT, OPT, SEVIS, I-20) benefits from domain-tuned embeddings like BGE-M3, though fine-tuning requires labeled data we don't have. (3) **Context length**: all-MiniLM-L6-v2 maxes at 256 tokens per input, requiring careful pre-chunking; newer models support 512-8192 tokens but sacrifice speed. (4) **Latency vs. accuracy**: For real-time chat interfaces, all-MiniLM-L6-v2 offers ~50ms embedding time on CPU versus 200-500ms for larger models. Given our constraints, all-MiniLM-L6-v2 provides the best balance of speed, acceptable accuracy for English queries, and zero API costs. The top-k of 5 retrieves sufficient diverse contexts without overwhelming the LLM's context window.

---

## Grounded Generation

**System prompt grounding instruction:**

```
You are a helpful assistant answering questions about Trine University using ONLY the provided context from CISI FAQ documents.

CRITICAL RULES:
1. Answer ONLY using information from the retrieved context below
2. If the context does not contain enough information to answer the question, say "I don't have enough information to answer this question."
3. Do NOT use your general knowledge or make up information
4. Always cite which source document(s) you used by listing the filenames at the end

CONTEXT:
{retrieved_chunks}

QUESTION: {query}

ANSWER:
```

**How source attribution is surfaced in the response:** After generating the answer, the system programmatically appends a "Sources:" section listing all unique source filenames from the retrieved chunks. This is done in code, not by the LLM, ensuring consistent attribution regardless of model behavior. Additionally, if the LLM indicates insufficient information, a warning note appears: "⚠️ Note: This response may not be based on retrieved document content."

---

## Evaluation Report

| #   | Question                                                                                                                     | Expected answer                                                                                                                                                                                       | System response (summarized)                                                                                                                                                                                                                           | Retrieval quality                                                         | Response accuracy                                               |
| --- | ---------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------- | --------------------------------------------------------------- |
| 1   | What are the CPT eligibility requirements and earliest start date at Trine University?                                       | Must include: Program Start Date vs Class Start Date distinction, can apply anytime except last 30 days, breaks don't affect CPT, only Experiential track requires CPT, contact DSO if job lost       | System correctly identified Program Start Date concept and break policy. Retrieved CPT问题.txt as primary source. However, did not explicitly mention the "last 30 days" restriction or DSO contact requirement.                                       | Relevant - Top result was CPT问题.txt                                     | Partially accurate - Missing some required details              |
| 2   | What are the application materials required for Trine University and what is the minimum financial proof amount?             | Must list: Resume, Transcripts (authenticated/translated), Diploma, Personal Statement (~350 words, no H1B/CPT mention), Passport/visa copies, Financial proof ($22,000 min)                          | System accurately listed all 6 required materials and specified $22,000 minimum financial proof. Correctly mentioned transcript authentication requirement and personal statement guidelines. Cited 申请材料.txt.                                      | Highly relevant - Direct match to 申请材料.txt                            | Accurate - All key facts included                               |
| 3   | What is the transfer credit policy at Trine University and when can students apply for it?                                   | Must include: Max 6 credits, master's level courses, 3.0+ GPA first semester required, apply AFTER first semester, submit transcripts/syllabus, communicate with advisor                              | System correctly stated maximum 6 credits and GPA requirement. Mentioned need to apply after first semester. Retrieved 转学分问题.txt. However, did not emphasize the importance of communicating with advisor during course selection.                | Relevant - Top result was 转学分问题.txt                                  | Partially accurate - Missing advisor communication detail       |
| 4   | What are the health insurance requirements for F-1 international students at Trine and can students use their own insurance? | Must state: Mandatory through Trine, ~$1,300/year, PPO with United Health Care, waivers only for sponsored students, private insurance doesn't qualify, dental/vision add-ons available               | System accurately covered all mandatory requirements including cost, provider, waiver restrictions, and add-on options. Clearly stated private insurance doesn't qualify. Cited 保险问题.txt.                                                          | Highly relevant - Direct match to 保险问题.txt                            | Accurate - All key facts included                               |
| 5   | What is the step-by-step application process for Trine University through CISI and how long does admission take?             | Must include: Register account, fill info, select CISI agent (info@cisi-edu.org), upload materials, email sharmasrijana@trine.edu + trine@cisi-edu.org, timeline (Tues/Fri contact, fastest 12 hours) | System outlined the general process but missed specific email addresses and exact timeline details. Did not mention the Tuesday/Friday contact schedule or 12-hour fastest decision. Retrieved 申请流程.txt but didn't extract all procedural details. | Partially relevant - Retrieved correct document but incomplete extraction | Partially accurate - General process correct, missing specifics |

---

## Failure Case Analysis

**Question that failed:** Question #5 - "What is the step-by-step application process for Trine University through CISI and how long does admission take?"

**What the system returned:** The system provided a general overview of the application process (register, fill form, upload materials) but failed to include critical specific details: the exact email addresses (sharmasrijana@trine.edu and trine@cisi-edu.org), the Tuesday/Friday contact schedule, and the 12-hour fastest admission timeline.

**Root cause (tied to a specific pipeline stage):** This failure occurred at the **Retrieval stage**. While the correct document (申请流程.txt) was retrieved in the top-5 results, the chunk containing the detailed procedural steps with email addresses and timeline was either: (a) split across chunk boundaries due to the 512-token limit, causing loss of continuity, or (b) ranked lower than other chunks from the same document that contained more general information. The embedding model likely matched the general keywords "application process" but didn't prioritize the chunk with specific contact details. Additionally, the **Generation stage** contributed - the LLM summarized rather than extracted verbatim details, losing precision.

**What you would change to fix it:**

1. **Retrieval improvement**: Implement re-ranking to boost chunks from the same document when one procedural step is found, ensuring contiguous steps stay together. Increase top-k from 5 to 8 to capture more granular details.
2. **Chunking improvement**: For procedural documents, use a smaller chunk size (256 tokens) with higher overlap (150 tokens) to ensure step-by-step sequences remain intact within single chunks.
3. **Generation improvement**: Modify the system prompt to explicitly request "Extract exact email addresses, phone numbers, and timelines verbatim from the context" to prevent summarization loss.

---

## Spec Reflection

**One way the spec helped you during implementation:** The planning.md specification was invaluable in defining the chunking strategy upfront. By specifying 512-token chunks with 100-token overlap before writing any code, I avoided the common pitfall of arbitrarily choosing parameters and then debugging poor retrieval results later. The spec forced me to think about the document structure (FAQ format with Q&A pairs) and choose parameters that preserve semantic units. This saved significant iteration time during Milestone 3.

**One way your implementation diverged from the spec, and why:** The original spec proposed using Groq's Llama-3-70b-8192 model with temperature=0.3, but I implemented llama-3.3-70b-versatile with temperature=0.1 instead. The divergence occurred because: (1) llama-3.3-70b-versatile is the current recommended model in Groq's free tier with better performance on factual tasks, and (2) I lowered temperature from 0.3 to 0.1 to enforce stricter grounding and reduce hallucination risk. This change aligns with the project's core principle of prioritizing accuracy over creativity for a fact-based FAQ system.

---

## AI Usage

**Instance 1**

- _What I gave the AI:_ I provided Claude 3.5 Sonnet with my "Chunking Strategy" section from planning.md (specifying 512-token chunks, 100-token overlap) and sample content from doxs/CPT问题.txt demonstrating Chinese FAQ format. I asked it to implement `chunk_text()` using LangChain's RecursiveCharacterTextSplitter.
- _What it produced:_ Claude generated a working `chunk_documents()` function but initially used character-based splitting instead of token-based, and didn't properly handle Chinese character boundaries. It also forgot to filter empty chunks.
- _What I changed or overrode:_ I replaced the character splitter with tiktoken-based token counting, added explicit UTF-8 handling for Chinese text preservation, and inserted a post-processing filter to remove chunks where `len(chunk.strip()) == 0`. I also added metadata attachment (source filename, topic category) which Claude omitted.

**Instance 2**

- _What I gave the AI:_ I asked GitHub Copilot to autocomplete the `generate_response()` function in generation.py, providing inline comments specifying the function signature and expected behavior (build prompt with context, call Groq API, return dict with answer/sources/grounded flag).
- _What it produced:_ Copilot generated a basic implementation that called the Groq SDK correctly but made two critical errors: (1) it relied on the LLM to append source citations in the response text rather than doing it programmatically, and (2) it didn't implement the "insufficient information" detection logic.
- _What I changed or overrode:_ I completely rewrote the source attribution logic to extract unique filenames from retrieved chunks metadata and append them after the LLM response, ensuring consistent formatting regardless of model output. I also added explicit parsing of the LLM response to detect phrases like "I don't have enough information" and set the `grounded=False` flag accordingly. This structural change was necessary to meet the strict grounding requirements.

---

## Demo Video

**Video Link:** https://vimeo.com/1199254968?share=copy&fl=sv&fe=ci

**Video Contents (3-5 minutes):**

- ✅ Query 1: "When can CPT start at the earliest?" - Shows successful retrieval and grounded response citing CPT问题.txt
- ✅ Query 2: "What materials are needed for Trine admission?" - Demonstrates accurate answer with 申请材料.txt source
- ✅ Query 3: "What is the transfer credit policy?" - Shows partial success, notes missing advisor communication detail
- ❌ Failure case: "What is the CISI application process?" - Narrates missing email addresses and timeline details, explains chunk boundary issue
- 📊 Brief walkthrough of evaluation table showing 2 accurate, 2 partially accurate, 1 incomplete result

---

## Technical Implementation Summary

### Architecture Pipeline

```
Document Ingestion → Chunking → Embedding → Vector Store → Retrieval → Generation
     (UTF-8)      → (512/100) → (MiniLM) → (ChromaDB) → (Top-5) → (Groq Llama-3.3)
```

### Technology Stack

- **Ingestion:** Python `open()` with UTF-8 encoding
- **Chunking:** LangChain RecursiveCharacterTextSplitter + tiktoken
- **Embedding:** sentence-transformers all-MiniLM-L6-v2
- **Vector Store:** ChromaDB persistent collection with HNSW index
- **Retrieval:** Cosine similarity search, top-k=5
- **Generation:** Groq SDK (llama-3.3-70b-versatile, temperature=0.1)
- **Interface:** Gradio 6.x Chatbot component

### Configuration Management

All parameters centralized in `config.py`:

- LLM model and API key (from .env)
- Embedding model name
- ChromaDB collection name and path
- Retrieval top-k value
- Chunk size and overlap
- Application host/port

### Key Files

- `config.py` - Centralized configuration
- `ingestion.py` - Document loading
- `chunking.py` - Text splitting
- `embedding.py` - Vector generation
- `vector_store.py` - ChromaDB operations
- `generation.py` - LLM integration
- `app.py` - Gradio web interface
- `test_milestone6.py` - Evaluation script

---

## Lessons Learned

1. **Grounding is hard but critical:** Enforcing strict grounding requires both prompt engineering AND programmatic safeguards. Relying solely on the LLM to cite sources leads to inconsistent results.

2. **Chunk boundaries matter:** Procedural information spanning multiple sentences is vulnerable to being split across chunks, causing incomplete retrieval. Smaller chunks with higher overlap help but increase storage costs.

3. **Semantic ≠ Exact match:** The embedding model retrieves semantically similar content but may miss exact procedural details (email addresses, timelines) that require keyword matching. Hybrid retrieval (semantic + keyword) would improve this.

4. **User expectations vs. reality:** Users may ask ambiguous questions (e.g., "CPT application materials" could mean CPT work authorization OR school admission). Clear UI labeling helps guide proper queries.

5. **Dark mode visibility:** Custom HTML components must be tested in both light and dark themes. Low-contrast text becomes invisible in dark mode.

---

## Future Improvements

1. **Hybrid retrieval:** Combine semantic search with BM25 keyword matching for better recall of exact terms (emails, dates, IDs).

2. **Query expansion:** Automatically expand queries with synonyms (e.g., "admission" → "application", "enrollment") to improve retrieval coverage.

3. **Re-ranking:** Add a cross-encoder re-ranker to re-score top-10 retrieved chunks and promote most relevant ones.

4. **Multi-turn dialogue:** Support follow-up questions by maintaining conversation history and re-retrieving context based on full dialogue.

5. **Feedback loop:** Allow users to rate answer quality and use feedback to improve retrieval ranking over time.
