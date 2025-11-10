import streamlit as st
from core.auth import require_password
from core.llm import chat, generate_image

st.set_page_config(page_title="Generate Visuals", page_icon="🖼️", layout="wide")
require_password()

st.title("🖼️ Step 4 — Generate Visuals")

draft = st.session_state.get("case_markdown")
if not draft:
    st.warning("Please complete **Step 3 — Draft Case Study** first.")
    st.stop()

st.subheader("Cover Illustration")
style = st.selectbox("Style", ["flat illustration", "isometric", "line art", "minimal infographic"], index=0)
theme = st.text_input("Theme keywords", value="public finance, collaboration, knowledge sharing, AI assistance, case studies")

if st.button("Generate Cover Image (1024x1024)"):
    prompt = f"A {style} depicting {theme}. Clean, professional, government context, minimal color palette."
    try:
        png_bytes = generate_image(prompt, size="1024x1024")
        st.image(png_bytes, caption="Generated Cover", use_column_width=True)
        st.session_state["cover_image"] = png_bytes
        st.success("✅ Cover image generated.")
    except Exception as e:
        st.error(str(e))

st.divider()
st.subheader("Auto-create Simple Diagram Prompts")
if st.button("Suggest Diagram Prompts from Draft"):
    p = f"""From the following case study markdown, list three concise prompts for diagrams/flowcharts to visualise the process and impact.
    Return bullet points only (max 3 prompts).
    ---
    {draft[:5000]}
    ---"""
    out = chat([{"role":"user","content":p}])
    st.markdown(out)
