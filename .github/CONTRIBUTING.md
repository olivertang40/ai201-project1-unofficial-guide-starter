# Contributing to Trine CISI FAQ Assistant

Thank you for your interest in this project! This is a course project for CodePath AI201, but we welcome feedback and suggestions.

## 📋 Project Overview

This RAG (Retrieval-Augmented Generation) system helps international students navigate Trine University processes by providing grounded answers from 10 FAQ documents covering:
- Admissions & application materials
- CPT/OPT work authorization
- Scholarships & financial aid
- Transfer credit policy
- Health insurance requirements
- Immigration status maintenance
- On-campus course requirements

## 🛠️ Technology Stack

- **Python 3.9+** - Backend language
- **Gradio 6.x** - Web interface
- **ChromaDB** - Vector database
- **sentence-transformers** - Embedding model (all-MiniLM-L6-v2)
- **Groq SDK** - LLM API (llama-3.3-70b-versatile)
- **LangChain** - Text processing utilities

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- Groq API key (free tier at [groq.com](https://console.groq.com/))

### Installation

```bash
# Clone repository
git clone https://github.com/olivertang40/ai201-project1-unofficial-guide-starter.git
cd ai201-project1-unofficial-guide-starter

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Run application
python app.py
```

Application will be available at `http://localhost:7860`

##  Project Structure

```
├── app.py                 # Gradio web interface
├── config.py              # Centralized configuration
├── ingestion.py           # Document loading
├── chunking.py            # Text splitting (512 tokens, 100 overlap)
├── embedding.py           # Vector generation
├── vector_store.py        # ChromaDB operations
├── generation.py          # LLM integration with grounding
├── requirements.txt       # Dependencies
├── .env.example           # Environment template
├── planning.md            # Architecture documentation
├── README.md              # Complete project docs
└── doxs/                  # 10 FAQ documents (UTF-8)
```

## 🧪 Testing

Run automated evaluation:

```bash
python test_milestone6.py
```

This tests all 5 evaluation questions and generates a compliance report.

## 📝 Documentation

- **[README.md](../README.md)** - Complete project documentation
- **[planning.md](../planning.md)** - Architecture & implementation plan
- **[Demo Video](https://vimeo.com/1199254968)** - System walkthrough

## 🐛 Reporting Issues

If you find bugs or have suggestions:

1. Check if the issue already exists in [Issues](https://github.com/olivertang40/ai201-project1-unofficial-guide-starter/issues)
2. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable

## 💡 Feature Requests

We welcome feature requests! Please create an issue with:
- Description of the feature
- Use case and benefits
- Potential implementation approach

## 🔧 Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and single-purpose

### Configuration
- All parameters centralized in `config.py`
- Sensitive data (API keys) in `.env` file only
- Never commit `.env` to version control

### Testing
- Test retrieval quality before committing changes
- Verify grounding enforcement (no hallucination)
- Check source attribution in responses

## 🎯 Current Limitations & Future Improvements

### Known Limitations
1. **Cross-language matching**: English queries may not perfectly match Chinese documents
2. **Procedural detail extraction**: Long step-by-step processes can lose details due to chunk boundaries
3. **No conversational memory**: Each query treated independently

### Suggested Enhancements
- [ ] Hybrid search (BM25 + semantic)
- [ ] Multi-turn dialogue support
- [ ] Metadata filtering UI
- [ ] Chunking strategy comparison
- [ ] Query expansion with synonyms
- [ ] Re-ranking with cross-encoder

## 📊 Evaluation Metrics

Current performance:
- **Accuracy:** 3/5 questions fully accurate (60%)
- **Partial Accuracy:** 2/5 questions partially accurate (40%)
- **Grounding:** ✅ Strict refusal for out-of-scope queries
- **Source Attribution:** ✅ All responses cite sources

See [README.md](../README.md) for detailed evaluation report.

## 🙏 Acknowledgments

- CodePath for AI201 course structure
- Groq for fast LLM inference API
- Sentence Transformers community
- ChromaDB team

## 📄 License

MIT License - See [LICENSE](../LICENSE) for details

---

**Author:** Oliver Tang  
**Course:** CodePath AI201  
**Date:** June 2026

For questions, please open an issue on GitHub.
