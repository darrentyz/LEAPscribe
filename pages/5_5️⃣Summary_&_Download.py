import streamlit as st
from core.auth import require_password
from docx import Document
from docx.shared import Inches
from io import BytesIO
import base64

st.set_page_config(page_title="Summary & Download", page_icon="📦", layout="wide")
require_password()

st.title("📦 Step 5 — Summary & Download")

case_md = st.session_state.get("case_markdown")
cover_image = st.session_state.get("cover_image")

if not case_md:
    st.warning("Please complete **Step 3 – Draft Case Study** and **Step 4 – Generate Visuals** first.")
    st.stop()

# --- Preview combined content ---
st.header("Preview")
if cover_image:
    st.image(cover_image, caption="Cover Image", use_column_width=True)
st.markdown(case_md)

st.divider()

# --- Download as DOCX ---
def build_docx(markdown_text: str, image_bytes: bytes | None):
    """Return DOCX bytes from markdown + optional cover image."""
    doc = Document()

    if image_bytes:
        img_stream = BytesIO(image_bytes)
        doc.add_picture(img_stream, width=Inches(5.5))
        doc.add_paragraph()

    # Basic markdown → paragraphs
    for line in markdown_text.splitlines():
        line = line.strip()
        if not line:
            doc.add_paragraph()
        elif line.startswith("# "):
            doc.add_heading(line[2:], level=1)
        elif line.startswith("## "):
            doc.add_heading(line[3:], level=2)
        elif line.startswith("**") and line.endswith("**"):
            doc.add_paragraph(line.strip("*"), style="Intense Quote")
        else:
            doc.add_paragraph(line)

    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

if st.button("📥 Generate & Download DOCX"):
    doc_buf = build_docx(case_md, cover_image)
    st.success("✅ DOCX generated successfully!")
    st.download_button(
        label="⬇️ Download Case Study (.docx)",
        data=doc_buf,
        file_name="LEAPscribe_Case_Study.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
