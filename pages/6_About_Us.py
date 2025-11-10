import streamlit as st

st.set_page_config(page_title="About Us", page_icon="ℹ️", layout="wide")

st.title("ℹ️ About Us")
st.markdown("""
**Problem Statement**  
Agencies are often reluctant to share their success stories on the Learn & LEAP Portal due to time, writing expertise, or resource constraints. This leads to missed cross-learning opportunities across WOG Finance.

**Solution**  
LEAPscribe guides officers from raw artefacts → AI analysis → targeted Q&A → polished case studies with images/diagrams. It standardises knowledge capture and lowers effort by 80–90% through LLM assistance.

**Security**  
- Password-protected (assignment requirement).  
- Secrets stored in Streamlit Cloud `secrets.toml`.  
""")
