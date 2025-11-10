import streamlit as st

def require_password():
    if "authed" not in st.session_state:
        st.session_state.authed = False
    if st.session_state.authed:
        return True

    st.markdown("### 🔒 This app is password-protected")
    pw = st.text_input("Enter password", type="password")
    if st.button("Unlock"):
        if pw and pw == st.secrets.get("ADMIN_PASSWORD", ""):
            st.session_state.authed = True
            st.rerun()
        else:
            st.error("Wrong password.")
    st.stop()
