import streamlit as st


st.set_page_config(page_title="LEAPscribe — Case Study Wizard", page_icon="🧙🏼‍♂️", layout="wide")


st.title("🪄 LEAPscribe — Case Study Wizard")
st.markdown("""
Welcome! This wizard will guide you from **uploads → AI analysis → fill missing info → polished case study → generated visuals**.
Use the sidebar to navigate steps.
""")

st.markdown("""
**Steps Overview**
1. Upload materials
2. AI finds gaps & asks you targeted questions
3. You answer once
4. AI drafts the full case study
5. AI generates a cover image and diagrams
""")
st.info("Go to **1️⃣ Upload & Analyse** in the sidebar to begin.")
