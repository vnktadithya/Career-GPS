import streamlit as st

def home():
    if not st.session_state.get('logged_in'):
        st.warning("Please login first.")
        st.stop()

    col1, col2, col3 = st.columns([1, 10, 1])

    with col3:
        if st.button("Logout"):
            st.session_state.clear()
            st.switch_page("main.py") 

    st.title(f"👋 Welcome, {st.session_state['username']}!")
    st.markdown("## 🚀 Welcome to Career GPS!")
    st.markdown("""
Career GPS is your personalized career roadmap builder powered by AI.

Whether you're just starting out or switching careers, we guide you step-by-step with curated resources, weekly milestones, and a practical learning plan tailored just for you.

---

### 💡 What You Can Do Here:

1. **Build Your Personalized Roadmap**  
   Just tell us your background and career goal, and we'll create a realistic weekly plan with resources from top platforms.

2. **Track Your Progress** *(coming soon)*  
   Mark completed weeks, get suggestions, and stay motivated.

3. **Explore Career Domains**  
   Get AI-powered guidance in trending fields like:
   - Data Analytics
   - AI and Agentic AI
   - Web Development
   - Cybersecurity
   - And more!

---

### 📋 How It Works:
- Login / Register
- Enter your background and goal
- Receive a weekly roadmap tailored to you
- Start learning and track your progress!

""")

    # Call to Action
    st.markdown("---")
    st.markdown("### ✅ Ready to build your roadmap?")
    if st.button("👉 Get Started"):
        st.switch_page("pages/Generate_Roadmap.py")  

home()
