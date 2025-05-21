import streamlit as st

def main():
    st.set_page_config(page_title="Career GPS", layout="wide")
    st.title("📍 Career GPS")
    st.markdown("Your personal AI mentor to help you navigate your career journey")

    if st.button("Get Started 🚀"):
        st.switch_page("pages/auth.py") 

if __name__ == "__main__":
    main()
