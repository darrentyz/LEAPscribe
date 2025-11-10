import streamlit as st
from core.auth import require_password
from core.rag import extract_text, upsert_documents, query
from core.llm import chat
from core.utils import parse_questions_list

st.set_page_config(page_title="Upload & Analyze", page_icon="📤", layout="wide")
require_password()

st.title("📤 Step 1 — Upload & Analyze")

uploads = st.file_uploader("Upload files (PDF/DOCX/TXT)", type=["pdf","docx","txt","md"], accept_multiple_files=True)
if st.button("Ingest & Analyze") and uploads:
    texts = []
    for f in uploads:
        t = extract_text(f.read(), f.name)
        texts.append(t)
        upsert_documents([{"text": t, "meta": {"filename": f.name, "source": "user_upload"}}])
    st.success("✅ Ingested & indexed.")

    corpus_sample = "\n\n".join([t[:1500] for t in texts])[:4000]
    prompt = f"""You are assisting to prepare a public-sector finance **case study**.
    Based on the following uploaded content (may be partial), list the **missing information** that we must ask the user **as bullet questions**.
    Cover: title direction, executive summary angle, problem clarity, implementation specifics (timeline, roles, tools), benefits with metrics, learning points, and a POC contact.
    Content sample:
    ---
    {corpus_sample}
    ---
    Return only bullet questions (max 10).
    """
    qs = chat([{"role":"user","content":prompt}])
    st.session_state["missing_questions_text"] = qs
    st.session_state["missing_questions"] = parse_questions_list(qs)
    st.success("🔎 Analysis complete. Proceed to **2️⃣ Fill Missing Info**.")
    with st.expander("See suggested questions"):
        st.markdown(qs)
