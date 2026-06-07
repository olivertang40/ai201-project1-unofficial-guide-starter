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

### 2:30-3:30 - Query 3: FAILURE CASE ⚠️
**Type:** "What is the step-by-step CISI application process and timeline?"

**Show:**
- ❌ Response missing email addresses
- ❌ No Tuesday/Friday schedule
- ❌ No 12-hour timeline mention

**Say:** "Here's a failure case. System retrieved correct document (申请流程.txt) but failed to extract specific details like email addresses and timelines. This happened because information was split across chunk boundaries during preprocessing. To fix: use smaller chunks with more overlap for procedural documents."

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
