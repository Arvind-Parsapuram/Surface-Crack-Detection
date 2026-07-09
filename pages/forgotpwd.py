import streamlit as st
from backend.auth import send_reset_email

st.set_page_config(
    page_title="Surface Detection System - Forgot Password",
    page_icon="🔒",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

st.title("🔒 Forgot Password")

st.write("Enter your registered email address.")

email = st.text_input("Email Address")

if st.button("Send Reset Link", use_container_width=True):
    if not email:
        st.error("Please enter your email address.")
    else:
        try:
            result = send_reset_email(email=email)
            if result.get("success"):
                st.success(result.get("message", "Password reset link sent to your email."))
            else:
                st.error("Failed to send reset link.")
        except Exception as e:
            st.error(str(e))

st.divider()

if st.button("⬅ Back to Login"):
    st.switch_page("pages/login.py")
