import streamlit as st
from backend.auth import register_user

st.set_page_config(
    page_title="Surface Detection System - Register",
    page_icon="📝",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

st.title("📝 Register")

name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
password = st.text_input("Password", type="password")
confirm = st.text_input("Confirm Password", type="password")

if st.button("Create Account", use_container_width=True):
    if not name or not email or not password:
        st.error("Please fill in all required fields.")
    elif password != confirm:
        st.error("Passwords do not match")
    elif len(password) < 6:
        st.error("Password must be at least 6 characters.")
    else:
        try:
            result = register_user(email=email, password=password, full_name=name)
            if result.get("success"):
                st.success(result.get("message", "Registration successful!"))
                st.info("Please check your email to verify your account, then log in.")
            else:
                st.error("Registration failed.")
        except Exception as e:
            st.error(str(e))

st.write("---")

if st.button("⬅ Back to Login"):
    st.switch_page("pages/login.py")