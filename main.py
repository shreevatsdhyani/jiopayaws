from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from groq import Groq
import os
from dotenv import load_dotenv
import uvicorn
import nest_asyncio

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
print(os.getcwd())
try:
    vector_store = FAISS.load_local(
        "api/jiopay_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
    print("FAISS vector store loaded successfully!")
except Exception as e:
    print(f"Error loading FAISS vector store: {e}")
    vector_store = None

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
async def ask(query_request: QueryRequest):
    if vector_store is None:
        raise HTTPException(status_code=500, detail="FAISS vector store not loaded")

    query = query_request.query

    try:
        retrieved_docs = vector_store.similarity_search(query, k=3)
        retrieved_content = "\n\n".join(
            [f"Content: {doc.page_content}\nSource: {doc.metadata['source_url']}"
             for doc in retrieved_docs]
        )

        prompt = f"""You are a JioPay expert assistant. Use ONLY this context:

        {retrieved_content}

        Question: {query}

        Provide a step-by-step answer with source references. If unsure, say "I don't know"."""

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": prompt},
            ],
            temperature=0.1
        )

        return {
            "response": response.choices[0].message.content,
            "sources": [dict(doc.metadata) for doc in retrieved_docs]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def health_check():
    return {"status": "ok"}


def start_server():
    uvicorn.run(app, host="127.0.0.1", port=os.getenv("PORT"))

if _name_ == "_main_":
    nest_asyncio.apply()
    start_server()