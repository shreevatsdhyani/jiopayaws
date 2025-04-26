```markdown
# JioPay Customer Support Chatbot - Backend

*Retrieval-Augmented Generation (RAG) powered customer support system*

## 📌 Overview
This repository contains the backend service for JioPay's AI-powered customer support chatbot. The system combines:
- **FAISS vector database** for efficient document retrieval
- **LLaMA-3-8B** (via Groq API) for response generation
- **FastAPI** RESTful endpoints

## 🛠️ Technical Stack
- **Framework**: FastAPI (Python)
- **Vector DB**: FAISS
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **LLM**: LLaMA-3-8B (hosted on Groq)
- **Infrastructure**: AWS EC2 (t2.micro)
- **CI/CD**: GitHub Actions

## 📂 Repository Structure
```
.
├── jiopay_index/            # FAISS vector store directory
│   ├── index.faiss          # FAISS index file
│   └── index.pkl            # Index metadata
├── main.py                  # FastAPI application
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── .gitignore               # Git ignore rules
```

## 🚀 Deployment Setup

### Prerequisites
- AWS EC2 instance (Ubuntu 20.04+ recommended)
- Python 3.9+
- Redis (for production session management)

### Installation
```bash
# Clone repository
git clone https://github.com/your-repo/jiopay-chatbot-backend.git
cd jiopay-chatbot-backend

# Install dependencies
python -m pip install -r requirements.txt

# Set environment variables
cp .env.example .env
nano .env  # Add your Groq API key
```

### Environment Variables
```ini
GROQ_API_KEY=your_groq_api_key_here
FAISS_INDEX_PATH=./jiopay_index
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### Running the Service
```bash
# Development
uvicorn main:app --reload

# Production (with Gunicorn)
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## 🔌 API Endpoints
### `POST /query`
**Request:**
```json
{
  "query": "How do I recharge with JioPay?"
}
```

**Response:**
```json
{
  "answer": "You can recharge using JioPay by...",
  "sources": [
    "https://www.jio.com/faq",
    "https://www.jio.com/recharge"
  ]
}
```

## 🔒 Security Considerations
- Ensure EC2 security group restricts access to:
  - Port 8000 (FastAPI)
  - SSH (port 22)
- Rotate Groq API keys regularly
- Monitor API usage with AWS CloudWatch

## 🤝 Integration with Frontend
The frontend (hosted on Vercel) communicates with this backend via:
```
POST https://your-ec2-public-ip:8000/query
```

## 📈 Monitoring
```bash
# View logs
journalctl -u jiopay-chatbot -f

# Health check
curl http://localhost:8000/health
```
