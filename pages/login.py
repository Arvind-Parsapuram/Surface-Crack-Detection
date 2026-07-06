import streamlit as st
from backend.auth import login_user

st.set_page_config(
    page_title="Surface Detection System - Login",
    page_icon="🔐",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

st.title("🛣️ Surface Detection System")
st.subheader("Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login", use_container_width=True):
    if not email or not password:
        st.error("Please enter both email and password.")
    else:
        try:
            result = login_user(email=email, password=password)
            if result.get("success"):
                st.session_state["access_token"] = result["access_token"]
                st.session_state["user"] = result["user"]
                st.success("Login Successful ✅")
                st.switch_page("pages/Home.py")
            else:
                st.error("Invalid email or password")
        except Exception as e:
            st.error(str(e))

st.write("---")

col1, col2 = st.columns(2)
with col1:
    if st.button("Forgot Password"):
        st.switch_page("pages/forgotpwd.py")
with col2:
    if st.button("Register"):
        st.switch_page("pages/register.py")
