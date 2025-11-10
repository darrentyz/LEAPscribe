import streamlit as st
from core.auth import require_password
from core.rag import query
from core.llm import chat
from core.utils import build_case_study

st.set_page_config(page_title="Draft Case Study", page_icon="📄", layout="wide")
require_password()

st.title("📄 Step 3 — Draft Case Study")

answers = st.session_state.get("answers", {})
if not answers:
    st.warning("Please complete **Step 2 — Fill Missing Info** first.")
    st.stop()

topic_hint = st.text_input("Optional: topic hint for better grounding (e.g., 'budget consolidation, procurement chatbot')", value="finance transformation, case study")
if st.button("Draft Now"):
    ctx = query(topic_hint, k=8)
    base = "\n\n".join([c["text"] for c in ctx]) if ctx else "(no context)"
    answers_text = "\n".join([f"- {k}: {v}" for k,v in answers.items() if v.strip()])

    prompt = f"""You are a professional case study writer for public-sector finance.
    Using the CONTEXT (from uploaded files) and the USER ANSWERS (provided via a form), draft a polished, visually engaging case study with the following sections:

    1) Captivating Title
    2) Executive Summary (3–5 sentences)
    3) Problem / Need for the project
    4) Implementation Approach (timeline, roles, tools, governance)
    5) Benefits & Impact (quantify where possible, use bullets if helpful)
    6) Key Learning Points (bulleted)
    7) Point of Contact (POC: name, role, email — use placeholders if missing)
    8) Suggested Visuals/Diagrams (list 2–3 ideas)

    CONTEXT:
    {base}

    USER ANSWERS:
    {answers_text}

    Return **Markdown only**.
    """
    draft = chat([{"role":"user","content":prompt}])
    st.session_state["case_markdown"] = draft
    st.success("✅ Draft ready. See below and proceed to **4️⃣ Generate Visuals**.")
    st.markdown(draft)
