import streamlit as st
import requests
from streamlit_chat import message

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Enterprise LLM Assistant", page_icon="🤖", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .title {
        font-size: 3rem;
        font-weight: 700;
        color: #4a90e2;
        margin-bottom: 0;
    }
    .subtitle {
        font-size: 1.25rem;
        color: #777;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .upload-section, .query-section {
        background: #f9f9f9;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 2px 10px rgba(74, 144, 226, 0.1);
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #357ABD;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="title">🤖 Enterprise LLM-Powered Assistant</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Upload your documents and ask questions — get fast, precise answers.</p>', 
    unsafe_allow_html=True,
)

# Upload Section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.header("📂 Upload Documents")

uploaded_files = st.file_uploader(
    "Choose PDF, DOCX, or TXT files",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
)

if uploaded_files:
    if st.button("Upload and Process"):
        with st.spinner("Uploading and processing..."):
            success = True
            for file in uploaded_files:
                files = {"file": (file.name, file, file.type)}
                try:
                    resp = requests.post(f"{BACKEND_URL}/upload", files=files)
                    if resp.status_code != 200:
                        success = False
                        st.error(f"Failed to upload {file.name}: {resp.text}")
                except Exception as e:
                    success = False
                    st.error(f"Error uploading {file.name}: {e}")
            if success:
                st.success("✅ All documents uploaded and processed!")
st.markdown('</div>', unsafe_allow_html=True)

# Chat Section
st.markdown('<div class="query-section" style="margin-top:2rem;">', unsafe_allow_html=True)
st.header("💬 Ask Your Question")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.text_input("Type your question here...")

if st.button("Send") and question:
    with st.spinner("Thinking..."):
        try:
            resp = requests.get(f"{BACKEND_URL}/query", params={"query": question})
            if resp.status_code == 200:
                answer = resp.json().get("answer", "No answer returned.")
                # Append to chat history
                st.session_state.chat_history.append({"user": question, "bot": answer})
            else:
                st.error(f"Error: {resp.text}")
        except Exception as e:
            st.error(f"Failed to get answer: {e}")

# Display chat history as chat bubbles
for chat in st.session_state.chat_history:
    message(chat["user"], is_user=True, key=chat["user"] + "_user")
    message(chat["bot"], key=chat["user"] + "_bot")

st.markdown('</div>', unsafe_allow_html=True)
