# backend/app.py
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from typing import List

from rag_engine import (
    embedding_model,
    vector_store,
    save_vector_store,
    load_vector_store,
    create_or_update_vector_store,
)

from transformers import pipeline
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline

app = FastAPI()

# Enable CORS for frontend requests (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to save uploaded docs and vector store
DOCS_DIR = "data/company_docs"
VECTOR_STORE_DIR = "data/vector_store"

os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

# Initialize embedding model (unchanged)
embedding_model = embedding_model  # from rag_engine.py

# Load or initialize vector store (if exists)
if os.path.exists(os.path.join(VECTOR_STORE_DIR, "faiss_index")):
    vector_store = load_vector_store(VECTOR_STORE_DIR, embedding_model)
else:
    vector_store = None

# Initialize HuggingFace text-generation pipeline with smaller model
llm_pipeline = pipeline(
    "text-generation",
    model="distilgpt2",      # smaller model for 6GB GPU
    tokenizer="distilgpt2",
    max_new_tokens=512,
    do_sample=True,
    temperature=0.7,
    top_p=0.9,
    device=0,                # GPU device index 0
)

llm = HuggingFacePipeline(pipeline=llm_pipeline)

# Setup RetrievalQA chain for querying vector store
qa_chain = None
if vector_store:
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        return_source_documents=True,
    )

@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    saved_files = []
    for file in files:
        file_location = os.path.join(DOCS_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file.filename)

    # Update or create vector store with new documents
    global vector_store, qa_chain
    vector_store = create_or_update_vector_store(DOCS_DIR, VECTOR_STORE_DIR, embedding_model)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        return_source_documents=True,
    )

    return {"uploaded_files": saved_files, "message": "Documents uploaded and vector store updated."}

@app.get("/query")
async def query_knowledge_base(question: str = Query(..., min_length=1)):
    if not qa_chain:
        return {"error": "No documents indexed yet. Please upload documents first."}

    result = qa_chain.run(question)
    return {"question": question, "answer": result}

@app.get("/")
async def root():
    return {"message": "Welcome to Enterprise LLM-Powered Knowledge Assistant backend!"}
