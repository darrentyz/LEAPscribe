import streamlit as st
from core.auth import require_password

st.set_page_config(page_title="Methodology", page_icon="🧩", layout="wide")
require_password()

st.title("🧩 Methodology")
st.markdown("""
**Flow**  
1. **Upload**: Ingest PDF/DOCX/TXT → extract text → chunk & embed (FAISS).  
2. **Analyze**: LLM proposes missing info as targeted questions.  
3. **Fill**: User answers once.  
4. **Draft**: LLM drafts full case study grounded by RAG + your answers.  
5. **Visuals**: LLM proposes diagrams; Images API generates a cover illustration.

**Tech Stack**  
- Streamlit multipage app (+ password gate)  
- Vector DB: FAISS (local)  
- LLM: Chat Completions (drafting, questions, prompts)  
- Embeddings: `text-embedding-3-small`  
- Images: `gpt-image-1` (PNG base64 → displayed)
""")
