
# 🧠 Enterprise LLM-Powered Knowledge Assistant

> A full-stack, LLM-powered assistant for enterprises to query internal documents in natural language using RAG (Retrieval-Augmented Generation). It enables smarter decision-making by turning scattered data into actionable insights.

---

## 📸 Demo UI

![Alt text for image]([Screenshot 2025-06-07 084425.png](https://github.com/Aakash091-dark/Enterprise-LLM-Powered-Knowledge-Assistant/blob/main/Screenshot%202025-06-07%20084425.png))



---

## 📌 Problem Statement

Modern enterprises have huge amounts of unstructured data — PDFs, manuals, policy documents — and employees often waste hours trying to find specific information. Traditional search fails to capture **context** or **semantics**.

---

## 💡 Solution

Our assistant uses **LLMs + vector search (FAISS)** to answer enterprise-specific questions accurately and quickly from uploaded documents.

---

## ✨ Features

- 🔍 Upload & query PDF, DOCX, TXT
- 💬 Natural language Q&A
- ⚡ Vector search with FAISS
- 🤖 LLM-based context generation
- 🖥️ React + Tailwind frontend
- 🚀 FastAPI backend
- 🐳 Dockerized for easy deployment
- 📉 Lightweight models for 6GB GPUs

---

## 🧱 Tech Stack

| Layer      | Tools                                       |
| ---------- | ------------------------------------------- |
| Frontend   | React.js, Tailwind CSS                      |
| Backend    | Python, FastAPI, LangChain, FAISS           |
| ML Models  | SentenceTransformers, FLAN-T5, Transformers |
| Packaging  | Docker, Docker Compose                      |
| Deployment | Localhost / Render / HuggingFace / Azure    |

---

## 🧠 Architecture


User ➝ React Frontend ➝ FastAPI API ➝ Vector DB (FAISS)

⬇

LLM (FLAN-T5)


## 🧰 Project Structure

elka/
├── backend/
│   ├── app.py
│   ├── model.py
│   ├── rag_engine.py
│   ├── requirements.txt
├── frontend/
│   └── src/
│       ├── App.js
│       └── components/ChatInterface.jsx
├── docker-compose.yml
├── Dockerfile
└── README.md

## ⚙️ Getting Started

### 🚀 Local Setup

git clone https://github.com/yourusername/elka.git
cd elka
docker-compose up --build


## 💬 How to Use


* Open the frontend at [http://localhost:3000](http://localhost:3000)
* Click **Upload Document** and select `.pdf`, `.docx`, or `.txt`
* Enter your question in the chat box
* LLM will return an accurate, contextual response


## ⚠️ Troubleshooting



| Problem                       | Solution                                                   |
| ----------------------------- | ---------------------------------------------------------- |
| Docker can't find engine      | Enable "Use WSL 2 based engine" in Docker Desktop settings |
| `requirements.txt`not found | Ensure the file exists in `/backend`folder               |
| Model too large for GPU       | Use `flan-t5-small`or `flan-t5-base`                   |
| Slow Docker build             | Use a faster internet or pre-download models               |


## 🧱 Model Configuration (for 6GB GPU)


```
from transformers import AutoModelForSeq2SeqLM
llm = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
```

```
from sentence_transformers import SentenceTransformer
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
```


## 🚧 Challenges Faced


| Challenge                     | Resolution                                   |
| ----------------------------- | -------------------------------------------- |
| Docker engine errors          | Switched to WSL2 engine                      |
| Model OOM on 6GB GPU          | Used smaller LLMs (`flan-t5-small`)        |
| File parsing issues           | Added robust file handling logic             |
| Deployment & port issues      | Set environment variables and fixed ports    |
| Vector mismatch in large PDFs | Implemented chunking + FAISS metadata filter |


## 📈 Future Scope


* ✅ Add user login & roles (RBAC)
* ✅ Chat memory / history
* ✅ Text-to-speech / voice chat
* ✅ Email summaries & automation
* ✅ Organization-wide dashboard



## 🤝 Contribution

```
git checkout -b feature/your-feature
git commit -m "Add your feature"
git push origin feature/your-feature

```



## 👤 Author

**Aakash Sehrawat**

📧 Email: [kingdarksoul091@gmail.com]()

🔗 LinkedIn: [linkedin.com/in/aakashsehrawat](https://linkedin.com/in/aakashsehrawat)
