import streamlit as st
from utils import generate_roadmap


# --- Streamlit UI Starts Here ---
if not st.session_state.get('logged_in'):
        st.warning("Please login first.")
        st.stop()

st.set_page_config(page_title="Career GPS", layout="wide")

# Top row with "Track My Progress" and "Logout" buttons
spacer_col, button_col1, button_col2 = st.columns([0.8, 0.1, 0.1]) 

with button_col1:
    if st.button("Track My Progress", use_container_width=True, key="track_progress_button"):
        st.switch_page("pages/Progress_tracker.py") # Make sure this path is correct

with button_col2:
    if st.button("Logout", use_container_width=True, key="logout_button"):
        st.session_state.clear()
        st.switch_page("main.py")  

        
st.title("📍 Career GPS: Your Personalized Career Roadmap")
st.markdown("Welcome! Let's build your custom career roadmap step by step.")

# Section 1: Upload Resume or Enter Skills
st.header("Step 1: Tell us about your background")
option = st.radio("How would you like to input your background?", ["Type it manually", "Upload Resume"])

user_info = ""

if option == "Type it manually":
    user_info = st.text_area("Enter your current skills, past courses, or projects", placeholder="E.g., I know Python and basic SQL. I watched some YouTube tutorials on data analysis.")
elif option == "Upload Resume":
    uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
    if uploaded_file:
        user_info = uploaded_file.read().decode("utf-8", errors="ignore")

# Section 2: Career Goal
st.header("Step 2: Choose your career goal")
career_goal = st.text_input("What do you want to become?", placeholder="E.g., Data Analyst")

# Generate Button
if st.button("🚀 Generate My Roadmap"):
    if user_info and career_goal:
        with st.spinner("Generating your personalized roadmap..."):
            roadmap = generate_roadmap(user_info, career_goal)
            st.success("Here's your roadmap! 💡")
            st.markdown(roadmap)
    else:
        st.warning("Please provide both your background and a career goal.")

# Footer
st.markdown("---")