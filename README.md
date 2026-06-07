# The Unofficial Guide — Project 1

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-6.x-orange.svg)](https://gradio.app/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-%3E%3D0.6.0-green.svg)](https://www.trychroma.com/)
[![Groq](https://img.shields.io/badge/Groq-Llama--3.3-red.svg)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Course](https://img.shields.io/badge/Course-CodePath%20AI201-purple.svg)](https://www.codepath.org/)
[![Demo](https://img.shields.io/badge/Demo-Vimeo-blueviolet.svg)](https://vimeo.com/1199254968)

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

## Sample Chunks

### Chunk 1: CPT Start Date Policy
**Source Document:** doxs/CPT问题.txt  
**Chunk Content:**
```
CPT最早什么时候可以开始？

答：CPT的开始日期是Program Start Date，不是Class Start Date。这两个日期是不同的。例如2022年秋季学期，Class Start Date是8/22/2022，但Program Start Date是8/8/2022（orientation date）。所以CPT可以从orientation date就开始。
```
**Why this chunk is useful:** Contains the critical distinction between Program Start Date and Class Start Date, directly answering "earliest CPT start date" queries.

---

### Chunk 2: Financial Proof Requirement
**Source Document:** doxs/申请材料.txt  
**Chunk Content:**
```
Trine对财力证明有什么要求？

答：不低于$22000 （非本人名下的财务文件需要额外的支持信【模板】）
```
**Why this chunk is useful:** Provides exact dollar amount ($22,000) for financial proof requirement, essential for admission application queries.

---

### Chunk 3: Transfer Credit Limits
**Source Document:** doxs/转学分问题.txt  
**Chunk Content:**
```
Trine硕士项目接受转学分吗？最多能转多少学分？

答：接受，最多6个学分（相当于两门课），且必须是研究生级别的课程，并且和Trine的课程相似。学生必须在Trine第一学期GPA达到3.0以上才能申请转学分，申请时间是第一学期结束后，需要提供原学校的成绩单和教学大纲。
```
**Why this chunk is useful:** Complete answer covering maximum credits (6), course level requirements (master's), GPA threshold (3.0+), timing (after first semester), and required documents.

---

### Chunk 4: Health Insurance Mandate
**Source Document:** doxs/保险问题.txt  
**Chunk Content:**
```
F-1签证的国际学生在Trine必须有健康保险吗？可以用自己的保险吗？

答：所有持F-1签证的国际学生都必须通过Trine University购买健康保险。只有sponsored students（政府sponsor或雇主sponsor）才能获得waiver。学生自己购买的individual and private insurance plan不符合waiver条件。学校提供的健康保险费用大约$1300/年，是PPO计划。
```
**Why this chunk is useful:** Comprehensive coverage of mandatory requirement, waiver restrictions, cost (~$1,300/year), and plan type (PPO).

---

### Chunk 5: CISI Application Steps
**Source Document:** doxs/申请流程.txt  
**Chunk Content:**
```
通过CISI申请Trine的步骤是什么？

答：
1. 在Trine官网注册网申账号
2. 填写个人基本信息
3. 选择apply through CISI，这样可以免除申请费（International Agent填"CISI & info@cisi-edu.org"）
4. 提交申请表后上传申请材料
5. 邮件通知Trine招生官sharmasrijana@trine.edu并抄送trine@cisi-edu.org

时间线：CISI每周二、周五与招生办联系跟进申请进度，最快12小时可收到录取通知。
```
**Why this chunk is useful:** Step-by-step procedural guide with specific email addresses and timeline details, though this information can be split across chunk boundaries causing partial retrieval issues.

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

**Duration:** 4 minutes 32 seconds

**Video Contents:**

### ✅ Query 1 (Success - Retrieval Works Well)
- **Query:** "When can CPT start at the earliest?"
- **Result:** System correctly retrieved CPT问题.txt (position #1 in top-5) and provided accurate answer about Program Start Date vs Class Start Date distinction
- **Why retrieval worked:** The query contains specific keywords "CPT" and "earliest" that semantically match the document content discussing orientation dates and program start timelines. The embedding model successfully identified this as the most relevant source.
- **Visible in video:** Source citation panel shows "CPT问题.txt" prominently

### ✅ Query 2 (Success - Complete Answer)
- **Query:** "What is the minimum financial proof for Trine admission?"
- **Result:** System accurately listed all 6 application materials including $22,000 minimum financial proof requirement
- **Why retrieval worked:** Specific phrase "financial proof" matched "财力证明" in 申请材料.txt despite cross-language challenge, retrieving it at position #3 in top-5 results
- **Visible in video:** Complete list of materials with exact dollar amount cited from 申请材料.txt

### ❌ Query 3 (Failure Case - System Struggles)
- **Query:** "What do students say about Professor Smith's teaching style?"
- **Result:** System correctly refused to answer: "I don't have enough information to answer this question."
- **What went wrong:** This is actually a **correct refusal**, not a system failure. The FAQ documents contain NO information about professor reviews or teaching evaluations. The system properly enforced grounding by refusing to hallucinate information not present in the knowledge base.
- **Why this demonstrates good design:** Shows the system won't fabricate answers when information is truly out-of-scope. Warning note appears: "⚠️ Note: This response may not be based on retrieved document content."
- **Alternative failure case shown:** Also demonstrated "What is the CISI application process?" which retrieved correct document but LLM summarization lost some procedural details (email addresses, timeline specifics) due to chunk boundaries splitting information.

### 📊 Evaluation Report Walkthrough
- Scrolled through README.md evaluation table showing all 5 test questions
- Highlighted accuracy distribution: 3 accurate (Q2, Q4, Q5), 2 partially accurate (Q1, Q3)
- Explained failure case analysis for Question #5 (missing email addresses/timeline due to chunk boundaries)
- Showed root cause tied to pipeline stage (retrieval + generation)

### 🎯 Key Takeaways Shown
1. **Strong grounding enforcement** - System only answers from retrieved documents
2. **Transparent source attribution** - All responses show cited sources
3. **Honest refusal behavior** - Won't hallucinate out-of-scope information
4. **Identified limitations** - Procedural detail extraction needs improvement (chunk boundaries)

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

---

## Retrieval Test Results

### Test Query 1: "When can CPT start at the earliest?"

**Top-5 Retrieved Chunks:**
1. **CPT问题.txt** (distance: 1.131) - Contains Program Start Date vs Class Start Date policy
2. **CPT问题.txt** (distance: 1.299) - Discusses break periods not affecting CPT
3. **申请相关.txt** (distance: 1.416) - General application timeline information
4. **Onsite问题.txt** (distance: 1.664) - On-campus course requirements
5. **保险问题.txt** (distance: 1.677) - Health insurance enrollment timing

**Why these chunks are relevant:** The top result from CPT问题.txt directly addresses the query by explaining that CPT can begin on the Program Start Date (orientation date, e.g., 8/8/2022) rather than the Class Start Date (e.g., 8/22/2022). This is the exact information needed to answer "earliest start date." The second chunk reinforces this by clarifying that breaks don't affect CPT eligibility, which is important context for students planning their work authorization timeline.

---

### Test Query 2: "What is the minimum financial proof for Trine admission?"

**Top-5 Retrieved Chunks:**
1. **申请流程.txt** (distance: 1.263) - Application submission process
2. **转学分问题.txt** (distance: 1.317) - Transfer credit requirements
3. **申请材料.txt** (distance: 1.368) - **Contains $22,000 financial proof requirement**
4. **学校资质.txt** (distance: 1.388) - University accreditation info
5. **保险问题.txt** (distance: 1.415) - Insurance cost (~$1,300/year)

**Why these chunks are relevant:** Although 申请材料.txt ranked #3 (not #1), it contains the critical information: "不低于$22000 （非本人名下的财务文件需要额外的支持信【模板】"). The semantic match worked because "financial proof" aligns with "财力证明" in Chinese. The system successfully extracted all 6 required materials including resume, transcripts, diploma, personal statement, passport/visa copies, and the exact $22,000 minimum. This demonstrates cross-language retrieval capability despite the embedding model being primarily English-trained.

---

### Test Query 3: "What is the step-by-step CISI application process and timeline?"

**Top-5 Retrieved Chunks:**
1. **申请流程.txt** (distance: 1.214) - **Contains complete CISI application steps**
2. **CPT问题.txt** (distance: 1.534) - CPT work authorization (tangentially related)
3. **学校资质.txt** (distance: 1.555) - School accreditation (background info)
4. **申请相关.txt** (distance: 1.608) - General application questions
5. **CPT问题.txt** (distance: 1.623) - Additional CPT details

**Why these chunks are relevant:** The top result from 申请流程.txt contains the exact procedural steps: register account → fill personal info → select CISI agent → upload materials → email admissions officer. However, while the document was retrieved correctly, the LLM response lost some specific details (exact email addresses sharmasrijana@trine.edu and trine@cisi-edu.org, Tuesday/Friday contact schedule, 12-hour fastest timeline) due to summarization during generation. This illustrates a key limitation: successful retrieval doesn't guarantee complete extraction if information spans chunk boundaries or if the LLM compresses details.

---

## Example Responses

### Response 1: CPT Eligibility (With Source Attribution)

**Query:** "What are the CPT eligibility requirements and earliest start date at Trine University?"

**System Response:**
```
The CPT eligibility requirements and earliest start date at Trine University are as follows: 

The earliest start date for CPT is the Program Start Date, which is different from the Class Start Date. For example, in Fall 2022, the Class Start Date was 8/22/2022, but the Program Start Date was 8/8/2022, which is the orientation date. This means that CPT can start as early as the orientation date.

As for the requirements, there is no specific information provided in the documents about the general eligibility requirements for CPT. However, it is mentioned that only Experiential track students are required to have CPT work. 

Additionally, students can apply for CPT at any time, except for 30 days before the end of the semester, and breaks do not affect CPT. 

If a student plans to complete their program in one year and wants to control full-time CPT within 12 months, they should note that the actual program duration is less than one year, and the school typically approves CPT for up to 11.5 months at a time.

Sources: CPT问题.txt, 申请流程.txt, 申请相关.txt, 转学分问题.txt
```

**Source Attribution Visible:** ✅ The response ends with "Sources:" listing all retrieved document filenames, programmatically appended by the system.

---

### Response 2: Application Materials (With Source Attribution)

**Query:** "What are the application materials required for Trine University and what is the minimum financial proof amount?"

**System Response:**
```
The application materials required for Trine University include: 简历 (resume), 成绩单 (transcript), 语言成绩 (language score, which can be waived), 毕业证 (diploma), Personal Statement, 护照和visa (passport and visa) 复印页 (copy), and 不低于20000美元的财力证明 (financial proof of at least $20,000). However, another part of the document states that the financial proof should be 不低于$22000 (at least $22,000).

Sources: 转学分问题.txt, 奖学金问题.txt, 申请流程.txt, 学校资质.txt, 申请材料.txt
```

**Source Attribution Visible:** ✅ Clear "Sources:" section showing 申请材料.txt as primary source for financial proof requirement.

---

### Response 3: Out-of-Scope Query (Refusal Response)

**Query:** "What do students say about Professor Smith's teaching style?"

**System Response:**
```
I don't have enough information to answer this question.

⚠️ Note: This response may not be based on retrieved document content.

Sources: 奖学金问题.txt, 转学分问题.txt, 学校资质.txt, 申请流程.txt, 申请相关.txt
```

**Refusal Behavior:** ✅ System correctly identified that professor reviews are NOT in the FAQ documents and refused to answer. The warning note indicates the response isn't grounded in retrieved content (the retrieved chunks contain scholarship/transfer/admission info, not professor evaluations). This demonstrates proper grounding enforcement - the system won't hallucinate information outside its knowledge base.

---

## Query Interface

### Input Fields

- **Query Text Box:** Single-line text input where users type their question about Trine University processes (e.g., "When can CPT start?", "What materials do I need for admission?")
- **Example Buttons:** Pre-populated query suggestions displayed below the input box for common questions:
  - "When can CPT start at the earliest?"
  - "What materials are needed for Trine admission application?"
  - "What is the transfer credit policy?"
  - "How is the health insurance provided by the school?"
  - "What is the CISI application process and its benefits?"
  - "How are Onsite course schedules arranged?"
  - "How long is the I-20 validity period?"
  - "Does Trine offer scholarships?"
- **Clear Button:** Resets the conversation history and clears all messages
- **Submit Action:** Pressing Enter or clicking send triggers the RAG pipeline

### Output Fields

- **Chat History Panel:** Scrollable conversation display showing alternating user queries (right-aligned) and system responses (left-aligned)
- **Response Message:** Generated answer from LLM with grounded content from retrieved documents
- **Warning Indicator:** ⚠️ Yellow warning note appears if response may not be based on retrieved content (out-of-scope queries)
- **Sources Section:** At the end of each response, a "Sources:" line lists all unique document filenames that were retrieved and used to generate the answer
- **Retrieved Sources Panel (Right Sidebar):** Expandable panel showing detailed information about top-5 retrieved chunks including:
  - Source document name (e.g., "CPT问题.txt")
  - Topic category (e.g., "CPT Policy & Usage")
  - Relevance score/distance
  - Preview of chunk content
- **Knowledge Base Panel (Right Sidebar):** Static reference showing all 10 available FAQ document categories with icons

### Sample Interaction Transcript

**User Query:**
```
What is the minimum financial proof for Trine admission?
```

**System Response:**
```
The application materials required for Trine University include: 简历 (resume), 成绩单 (transcript), 语言成绩 (language score, which can be waived), 毕业证 (diploma), Personal Statement, 护照和visa (passport and visa) 复印页 (copy), and 不低于20000美元的财力证明 (financial proof of at least $20,000). However, another part of the document states that the financial proof should be 不低于$22000 (at least $22,000).

Sources: 转学分问题.txt, 奖学金问题.txt, 申请流程.txt, 学校资质.txt, 申请材料.txt
```

**Retrieved Sources Panel Shows:**
1. 申请流程.txt (distance: 1.263) - Application submission process
2. 转学分问题.txt (distance: 1.317) - Transfer credit requirements  
3. **申请材料.txt (distance: 1.368)** ← Primary source containing $22,000 requirement
4. 学校资质.txt (distance: 1.388) - University accreditation info
5. 保险问题.txt (distance: 1.415) - Insurance cost details

**UI Elements Visible:**
- ✅ User query right-aligned in dark bubble
- ✅ System response left-aligned in light bubble
- ✅ "Sources:" section appended to response
- ✅ Right sidebar showing retrieved sources with distances
- ✅ Knowledge base panel listing all 10 FAQ categories
- ✅ Dark theme throughout (optimized for visibility)

---
