# LEAPscribe — Case Study Wizard (Reworked Journey)

User Journey:
1) Upload supporting materials (slides, reports, emails).
2) AI analyses content, identifies missing information, prompts for inputs.
3) AI crafts a polished case study with: title, exec summary, problem, implementation, benefits, learning points, POC.
4) AI also generates relevant images/diagrams/charts.
5) App is password-protected and includes "About Us" and "Methodology" pages.

## Local run
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
export ADMIN_PASSWORD=choose_a_password
streamlit run app.py
```

## Streamlit Cloud
Add in Settings → Secrets:
```toml
OPENAI_API_KEY = "sk-..."
ADMIN_PASSWORD = "StrongPassword123!"
# Optional model overrides:
# CHAT_MODEL = "gpt-4o-mini"
# EMBEDDING_MODEL = "text-embedding-3-small"
```
