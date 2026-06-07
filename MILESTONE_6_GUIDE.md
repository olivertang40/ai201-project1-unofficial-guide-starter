# Milestone 6 Demo Video Guide

##  Recording Instructions (3-5 minutes)

### Preparation
1. Start app: `python app.py`
2. Open browser: http://localhost:7860
3. Have README.md open in another tab
4. Test microphone

---

## Video Structure

### 0:00-0:30 - Introduction
- Show application title page
- Say: "This is the Trine CISI FAQ Assistant, a RAG system for international students"
- Mention: Uses Groq LLM and ChromaDB for retrieval

---

### 0:30-1:30 - Query 1: Success Case
**Type:** "When can CPT start at the earliest?"

**Show:**
- ✅ Answer appears with source citation
- ✅ Points to "CPT问题.txt"
- ✅ Retrieved sources panel visible

**Say:** "Successful retrieval - system found relevant CPT policy document and generated grounded response with source citation."

---

### 1:30-2:30 - Query 2: Success Case  
**Type:** "What is the minimum financial proof for Trine admission?"

**Why this query works better:** The phrase "financial proof" semantically matches "财力证明" in the documents better than generic "application materials", ensuring 申请材料.txt is retrieved (position #3 in top-5).

**Show:**
- ✅ Answer mentions $22,000 minimum requirement
- ✅ Lists other materials (resume, transcripts, diploma, personal statement, passport/visa)
- ✅ Cites "申请材料.txt" as source (visible in sources panel)

**Say:** "This query successfully retrieves the application materials document. The system shows the exact $22,000 financial proof requirement and lists all other required materials."

---

### 2:30-3:30 - Query 3: FAILURE CASE ️

**Option A - Out-of-Scope Query (Recommended):**
**Type:** "What do students say about Professor Smith's teaching style?"

**Expected Behavior:** System should refuse to answer because this information is NOT in the FAQ documents.

**Show:**
- ❌ Response: "I don't have enough information to answer this question."
- ⚠️ Warning note appears: "This response may not be based on retrieved document content."
- Sources panel shows retrieved docs, but none contain professor reviews

**Say:** "Here's an important failure case - or rather, a correct refusal. The system correctly identifies that professor reviews are NOT in our FAQ documents and refuses to answer. This demonstrates proper grounding enforcement. The system won't hallucinate information that isn't in the sources."

---

**Option B - Partial Retrieval Failure (Alternative):**
**Type:** "What are the specific requirements for OPT application after graduation?"

**Why it fails:** The documents focus on CPT (Curricular Practical Training) but have limited coverage of OPT (Optional Practical Training). The retrieval may return CPT-related chunks that don't fully answer OPT-specific questions.

**Show:**
- ️ Response mentions CPT policies but lacks OPT-specific details
- ❌ Missing: OPT application timeline, USCIS forms, post-completion rules
- Sources show CPT问题.txt but not comprehensive OPT guidance

**Say:** "This query partially fails because our documents focus on CPT work authorization, not OPT. The system retrieves related immigration content but can't provide complete OPT application steps. This shows a knowledge gap in our document collection - we'd need to add OPT-specific FAQs to fix this."

---

### 3:30-4:30 - Evaluation Walkthrough
- Open README.md
- Scroll to "Evaluation Report" section
- Show table with 5 questions

**Say:** "We tested 5 questions: 2 accurate, 2 partially accurate, 1 incomplete. Failure case analysis explains Question 5 failed due to chunk boundaries splitting procedural steps."

---

### 4:30-5:00 - Conclusion
- Show knowledge base panel
- Point out "Admission Materials (NOT CPT)" clarification

**Say:** "Overall, system demonstrates strong grounding - only answers from retrieved documents and cites sources. Main limitation is procedural detail extraction, documented for future improvement. Thank you."

---

## ✅ Checklist Before Recording

- [ ] App running on http://localhost:7860
- [ ] README.md open in browser/tab
- [ ] Microphone tested
- [ ] Quiet environment
- [ ] Cursor visible for highlighting

## 🎬 After Recording

1. Upload to YouTube (unlisted) or Vimeo
2. Get shareable link
3. Update README.md "Demo Video" section with actual link
4. Commit: `git add README.md && git commit -m "Add demo video link"`
5. Push: `git push origin main`

---

## 💡 Tips

- **Speak clearly** at moderate pace
- **Use mouse cursor** to highlight important parts
- **Pause briefly** between queries
- **Keep under 5 minutes**
- **Focus on showing**, not just telling

Good luck! 🎉
