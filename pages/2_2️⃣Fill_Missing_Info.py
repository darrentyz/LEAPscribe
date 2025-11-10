import streamlit as st
from core.auth import require_password

st.set_page_config(page_title="Fill Missing Info", page_icon="📝", layout="wide")
require_password()
st.title("📝 Step 2 — Fill Missing Info")

qs = st.session_state.get("missing_questions", [])
if not qs:
    st.warning("No questions yet. Please run **Step 1 — Upload & Analyze** first.")
    st.stop()

st.markdown("Answer these to enrich the case study draft:")

answers = {}
with st.form("fill_form"):
    for i, q in enumerate(qs, start=1):
        answers[q] = st.text_area(f"{i}. {q}", height=80)
    submitted = st.form_submit_button("Save Answers")
if submitted:
    st.session_state["answers"] = answers
    st.success("✅ Answers saved. Proceed to **3️⃣ Draft Case Study**.")
