# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

**International Student Survival Guide for Trine University** - This domain provides comprehensive guidance for international students navigating Trine University's complex processes including admissions, scholarships, credit transfers, CPT/OPT work authorization, immigration status maintenance, on-campus requirements, health insurance, and application procedures. This knowledge is exceptionally valuable because official university resources typically present information in fragmented, legalistic language without practical insights from actual student experiences. International students face unique challenges such as understanding visa regulations, managing F-1 status requirements, accessing scholarships specific to their status, and navigating cultural adjustments that aren't adequately addressed in formal documentation. The gap between official policy and real-world implementation creates confusion and anxiety, making peer-to-peer knowledge sharing essential for successful academic and professional outcomes.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | CISI Trine University FAQ - School Accreditation | Official accreditation information including HLC, SEVP, and Chinese Ministry of Education recognition | https://www.cisi-edu.org/trine-university-application-popular-questions-authoritative-interpretation-of-the-university/ |
| 2 | CISI Trine University FAQ - Application Related Questions | Comprehensive Q&A about offer acceptance, campus differences, transfer policies, timeline recommendations, and program structure | doxs/申请相关.txt |
| 3 | CISI Trine University FAQ - Application Materials | Detailed requirements for transcripts, financial proof ($22,000 minimum), resume, personal statement (350 words), and document authentication | doxs/申请材料.txt |
| 4 | CISI Trine University FAQ - Scholarship Information | Graduate scholarship policies and availability | doxs/奖学金问题.txt |
| 5 | CISI Trine University FAQ - Transfer Credit Policy | Credit transfer limits (max 6 credits), GPA requirements (3.0+), timing, and course equivalency guidelines | doxs/转学分问题.txt |
| 6 | CISI Trine University FAQ - CPT Questions | Complete CPT guidance including start dates, work authorization timing, full-time vs part-time rules, RFE handling, and job loss procedures | doxs/CPT问题.txt |
| 7 | CISI Trine University FAQ - Immigration Status | I-20 validity periods, RFE support materials, approval rates (<10% RFE rate), and documentation requirements | doxs/身份问题.txt |
| 8 | CISI Trine University FAQ - Onsite Course Requirements | Onsite schedule (Saturdays/Sundays 8am-5pm), attendance policies, course selection flexibility, and advisor communication | doxs/Onsite问题.txt |
| 9 | CISI Trine University FAQ - Health Insurance | Mandatory insurance through United Health Care (~$1,300/year PPO), waiver restrictions, dental/vision add-ons | doxs/保险问题.txt |
| 10 | CISI Trine University FAQ - Application Process | Step-by-step application workflow, CISI agent selection, email templates, admission timeline (as fast as 12 hours) | doxs/申请流程.txt |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 512 tokens

**Overlap:** 100 tokens

**Reasoning:** The document corpus contains mixed formats: policy documents with structured procedural steps (ISSS guidelines, SEVP regulations), FAQ-style content (admissions requirements, scholarship criteria), and unstructured student testimonials (Reddit posts, Facebook discussions). A 512-token chunk size balances several needs: (1) it captures complete procedural steps in policy documents without splitting critical multi-sentence instructions across chunks, (2) it accommodates typical Reddit post lengths while preserving context around key advice, and (3) it keeps individual scholarship or requirement descriptions intact. The 100-token overlap ensures that when a procedure spans two paragraphs or when a student testimonial references a prior statement, the semantic connection is preserved for accurate retrieval. This configuration works well for sentence-transformers models which perform optimally with chunks under 512 tokens.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers library

**Top-k:** 5

**Production tradeoff reflection:** For a production system serving international students globally, I would evaluate several tradeoffs: (1) **Multilingual support**: Many international students may query in their native language before translating; models like multilingual-e5-large or OpenAI's text-embedding-3-large handle cross-lingual retrieval better but increase computational cost 3-5x. (2) **Domain specificity**: Legal/immigration terminology (CPT, OPT, SEVIS, I-20) benefits from domain-tuned embeddings like BGE-M3, though fine-tuning requires labeled data we don't have. (3) **Context length**: all-MiniLM-L6-v2 maxes at 256 tokens per input, requiring careful pre-chunking; newer models support 512-8192 tokens but sacrifice speed. (4) **Latency vs. accuracy**: For real-time chat interfaces, all-MiniLM-L6-v2 offers ~50ms embedding time on CPU versus 200-500ms for larger models. Given our constraints, all-MiniLM-L6-v2 provides the best balance of speed, acceptable accuracy for English queries, and zero API costs. The top-k of 5 retrieves sufficient diverse contexts without overwhelming the LLM's context window, though I'd increase to 8-10 if implementing re-ranking.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What are the CPT eligibility requirements and earliest start date at Trine University? | Key facts that must be included: (1) Program Start Date differs from Class Start Date - CPT can begin on Program Start Date (orientation date), not Class Start Date. Example: Fall 2022 had Program Start Date 8/8/2022 and Class Start Date 8/22/2022. (2) CPT can be applied anytime during semester except last 30 days. (3) Break periods do NOT affect CPT usage. (4) Only Experiential track requires CPT work. (5) If student loses job, must contact DSO immediately to pause CPT and drop course (grade shows as W, doesn't affect GPA). |
| 2 | What are the application materials required for Trine University and what is the minimum financial proof amount? | Must mention ALL of these: (1) Resume - no specific format required, just list academic and work experience. (2) Transcripts - must be authenticated and translated if from China. (3) Diploma. (4) Personal Statement - approximately 350 words, explain why Trine and chosen major, DO NOT mention H1B or Day 1 CPT. (5) Passport and visa copies - expired visa is OK. (6) Financial proof - minimum $22,000 required. If financial documents are not in student's own name, additional support letter is needed. |
| 3 | What is the transfer credit policy at Trine University and when can students apply for it? | Critical requirements: (1) Maximum 6 credits (equivalent to two courses) can be transferred. (2) Transferred courses must be master's level and similar to Trine courses. (3) Student must achieve 3.0+ GPA in first semester at Trine BEFORE applying for transfer credits. (4) Application happens AFTER first semester ends. (5) Must submit original school transcripts and syllabus. (6) Important: During first semester course selection, communicate with academic advisor to avoid taking courses you hope to waive later. |
| 4 | What are the health insurance requirements for F-1 international students at Trine and can students use their own insurance? | Mandatory facts: (1) ALL F-1 visa students MUST have health insurance through Trine University. (2) Cost is approximately $1,300 per year. (3) Plan is PPO type with United Health Care. (4) Waivers are ONLY provided for sponsored students (government sponsor or employer sponsorship). (5) Individual and private insurance plans purchased by students DO NOT qualify for waiver. (6) Dental and vision insurance are NOT included but can be added for extra fee. |
| 5 | What is the step-by-step application process for Trine University through CISI and how long does admission take? | Must include these exact steps: (1) Register account on Trine website. (2) Fill personal information. (3) Select "apply through CISI" to waive application fee - choose International Agent "CISI & info@cisi-edu.org". (4) Upload application materials. (5) Email admission officer sharmasrijana@trine.edu and copy trine@cisi-edu.org with template including reference number. Timeline: CISI contacts admission every Tuesday and Friday. Fastest admission decision can be received in just 12 hours. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Conflicting or outdated information across sources**: Official university policies change frequently (especially immigration-related rules tied to federal regulations), while student forums contain anecdotal experiences that may reference outdated procedures. For example, CPT processing times mentioned in Reddit posts from 2022 may no longer be accurate if ISSS streamlined their workflow in 2024. The system might retrieve contradictory advice without clear temporal markers, leading to confusion. Mitigation: Prioritize official sources in retrieval ranking, include publication/update dates in metadata, and instruct the LLM to flag discrepancies and recommend verifying with ISSS directly.

2. **Fragmented procedural knowledge across multiple chunks**: Critical multi-step processes like "applying for OPT" involve sequential actions spread across different documents (SEVP regulations, ISSS checklist, student testimonials about timeline). A single chunk may capture only one step (e.g., "submit I-765 form") without the prerequisite steps (obtain recommendation letter from advisor, verify eligibility, pay USCIS fee). If retrieval returns non-contiguous chunks, the generated response may present an incomplete or incorrectly ordered procedure. Mitigation: Use metadata tagging to link related procedural chunks, implement re-ranking to prioritize chunks from the same document when one procedural step is found, and design prompts to explicitly request step-by-step sequences with warnings about consulting official checklists.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```
graph TD
    subgraph S1["Stage 1: Document Ingestion"]
        A1["CISI Website<br/>BeautifulSoup4"] 
        A2["doxs/ Topic Files<br/>UTF-8 Text Reader"]
        A3["Python requests<br/>HTTP Downloads"]
    end
    
    subgraph S2["Stage 2: Chunking"]
        B1["LangChain<br/>RecursiveCharacterTextSplitter"]
        B2["Configuration:<br/>chunk_size=512 tokens<br/>chunk_overlap=100 tokens"]
        B3["Chinese Text<br/>Preservation Logic"]
    end
    
    subgraph S3["Stage 3: Embedding + Vector Store"]
        C1["sentence-transformers<br/>all-MiniLM-L6-v2"]
        C2["Embedding Output:<br/>768-dim vectors"]
        C3["ChromaDB<br/>Persistent Collection<br/>HNSW Index"]
    end
    
    subgraph S4["Stage 4: Retrieval"]
        D1["User Query<br/>Text Input"]
        D2["Query Embedding<br/>same model"]
        D3["ChromaDB<br/>similarity_search<br/>metric=cosine"]
        D4["Top-k=5<br/>Relevant Chunks<br/>with Metadata"]
    end
    
    subgraph S5["Stage 5: Generation"]
        E1["Prompt Builder<br/>System Prompt + Context"]
        E2["Groq API<br/>Llama-3-70b-8192<br/>temperature=0.3"]
        E3["Grounded Response<br/>with Source Citations"]
    end
    
    A1 --> INGEST["Ingest & Clean<br/>Text Strings"]
    A2 --> INGEST
    A3 --> INGEST
    
    INGEST --> B1
    B1 --> B2
    B2 --> B3
    B3 --> CHUNKS["Chunked Documents<br/>List[dict]"]
    
    CHUNKS --> C1
    C1 --> C2
    C2 --> C3
    
    D1 --> D2
    D2 --> D3
    C3 --> D3
    D3 --> D4
    
    D4 --> E1
    E1 --> E2
    E2 --> E3
    
    style S1 fill:#e1f5ff
    style S2 fill:#fff4e1
    style S3 fill:#e8f5e9
    style S4 fill:#fce4ec
    style S5 fill:#f3e5f5
```

**Pipeline Flow Explanation:**

1. **Document Ingestion**: Reads 10 sources (1 CISI webpage via BeautifulSoup4, 9 Chinese text files from `doxs/` directory using UTF-8 encoding) and outputs cleaned text strings with metadata (source name, topic category).

2. **Chunking**: Uses LangChain's RecursiveCharacterTextSplitter configured for 512-token chunks with 100-token overlap. Special handling ensures Chinese characters aren't split mid-word and Q&A pairs stay together when possible.

3. **Embedding + Vector Store**: Each chunk is embedded using sentence-transformers' all-MiniLM-L6-v2 model (producing 768-dimensional vectors). Vectors are stored in ChromaDB persistent collection with HNSW index for fast similarity search, along with metadata (source file, topic, chunk index).

4. **Retrieval**: User query is embedded using the same model, then ChromaDB performs cosine similarity search to retrieve top-5 most relevant chunks with their source metadata.

5. **Generation**: Retrieved chunks are formatted into a system prompt with source citations. Groq API (Llama-3-70b-8192) generates a grounded response at temperature=0.3 for factual consistency, citing which FAQ topics provided the information.

**Technology Stack Summary:**
- **Ingestion**: `beautifulsoup4`, `requests`, Python built-in `open()` with `encoding='utf-8'`
- **Chunking**: `langchain-text-splitters` (RecursiveCharacterTextSplitter), `tiktoken` for token counting
- **Embedding**: `sentence-transformers==3.4.1` (all-MiniLM-L6-v2)
- **Vector Store**: `chromadb>=0.6.0` (persistent client with HNSW index)
- **Retrieval**: ChromaDB `collection.similarity_search(query_embedding, k=5)`
- **Generation**: `groq==0.15.0` SDK (Llama-3-70b-8192 model, temperature=0.3, max_tokens=500)

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

I will use **Claude 3.5 Sonnet** to implement the ingestion and chunking modules. I'll provide it with: (1) the "Documents" table listing all 10 sources (1 URL + 9 local text files in doxs/ directory), (2) the "Chunking Strategy" section specifying 512-token chunks with 100-token overlap, and (3) sample content from doxs/CPT问题.txt and doxs/申请材料.txt to demonstrate Chinese FAQ format. I expect Claude to produce: `ingestion.py` with functions `load_text_file(filepath)` for reading Chinese text files and `scrape_webpage(url)` for the CISI accreditation page, both returning cleaned text strings with proper UTF-8 encoding handling. Plus `chunking.py` with `chunk_text(text, chunk_size=512, overlap=100)` using LangChain's RecursiveCharacterTextSplitter configured for token-based splitting that preserves Chinese characters properly. I'll verify the output by: running the chunking function on doxs/CPT问题.txt (approximately 2000 tokens) and confirming it produces 4-5 chunks with proper overlap (checking that the last 100 tokens of chunk N match the first 100 tokens of chunk N+1), ensuring Chinese characters are not split mid-word, and verifying that Q&A pairs remain intact within chunks where possible.

**Milestone 4 — Embedding and retrieval:**

I will use **GitHub Copilot** (with GPT-4 backend) paired with manual testing to build the embedding and vector store components. I'll provide Copilot with: (1) the "Retrieval Approach" section specifying all-MiniLM-L6-v2 and top-k=5, (2) the Architecture diagram showing ChromaDB integration, and (3) inline comments in the code specifying function signatures like `embed_texts(texts: List[str]) -> np.ndarray` and `store_embeddings(chunks: List[dict], embeddings: np.ndarray, collection_name: str)`. I expect Copilot to autocomplete: `embedding.py` with `get_embedding_model()` returning the sentence-transformers model and `embed_batch(texts)` producing normalized embeddings, plus `vector_store.py` with `create_collection(name)` initializing ChromaDB, `add_documents(collection, chunks, embeddings)` storing vectors with metadata, and `search_collection(collection, query_embedding, k=5)` retrieving relevant chunks. I'll verify correctness by: embedding 3 known-similar sentences (e.g., "CPT requires one year of study", "You must complete two semesters before CPT eligibility", "One academic year is prerequisite for CPT") and confirming they have cosine similarity >0.8, then inserting 50 test chunks and querying with "scholarship GPA requirements" to check that the top-5 results include the scholarship policy document.

**Milestone 5 — Generation and interface:**

I will use **ChatGPT-4o** to develop the generation pipeline and simple web interface. I'll provide it with: (1) the "Evaluation Plan" table with 5 test questions and expected answers, (2) the "Anticipated Challenges" section highlighting the need for source attribution and handling conflicting information, (3) the Architecture diagram showing Groq API integration, and (4) a sample retrieved context block with 5 chunks. I expect ChatGPT to produce: `generation.py` with `build_prompt(query, retrieved_chunks)` constructing a system prompt that includes retrieved context with source citations, `generate_answer(prompt, model="llama3-70b")` calling Groq API with temperature=0.3 and max_tokens=500, and `app.py` implementing a Streamlit interface with text input, submit button, and formatted response display showing answer plus cited sources. I'll verify quality by: running all 5 evaluation questions through the system and checking that responses match expected answers within 80% semantic similarity (using BLEU score or manual grading), confirming that each response cites at least 2 sources, and testing edge cases like "What is CPT?" (should return general definition) versus "How do I apply for CPT at Trine?" (should return specific procedural steps with ISSS contact info).
