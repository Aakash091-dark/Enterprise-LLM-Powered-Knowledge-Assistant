# backend/rag_engine.py

import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Text splitter to chunk documents into manageable pieces
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

def load_documents_from_folder(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            docs = loader.load()
        elif filename.endswith(".txt"):
            loader = TextLoader(file_path)
            docs = loader.load()
        elif filename.endswith(".docx") or filename.endswith(".doc"):
            loader = UnstructuredWordDocumentLoader(file_path)
            docs = loader.load()
        else:
            # Unsupported file type, skip
            continue
        
        # Split documents into chunks
        for doc in docs:
            splitted = text_splitter.split_text(doc.page_content)
            for chunk in splitted:
                documents.append({"page_content": chunk, "metadata": doc.metadata})
    return documents

def create_or_update_vector_store(docs_folder, vector_store_folder, embedding_model):
    documents = load_documents_from_folder(docs_folder)
    
    # Extract texts and metadatas
    texts = [doc["page_content"] for doc in documents]
    metadatas = [doc["metadata"] for doc in documents]

    # Create or update FAISS vector store
    if os.path.exists(os.path.join(vector_store_folder, "faiss_index")):
        vector_store = FAISS.load_local(vector_store_folder, embedding_model)
        vector_store.add_texts(texts, metadatas=metadatas)
    else:
        vector_store = FAISS.from_texts(texts, embedding_model, metadatas=metadatas)

    # Save vector store locally
    vector_store.save_local(vector_store_folder)
    return vector_store

def save_vector_store(vector_store, vector_store_folder):
    vector_store.save_local(vector_store_folder)

def load_vector_store(vector_store_folder, embedding_model):
    return FAISS.load_local(vector_store_folder, embedding_model)
