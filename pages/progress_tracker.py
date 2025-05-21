import streamlit as st
import pandas as pd
import plotly.express as px
from db import store_progress, create_progress_table, get_progress, delete_single_goal

def progress_dashboard():
    if not st.session_state.get('logged_in'):
        st.warning("Please login first.")
        st.stop()

    col1, col2, col3 = st.columns([1, 10, 1])  # Adjust the proportions to align the button to the right

    with col3:
        if st.button("Logout"):
            st.session_state.clear()
            st.switch_page("main.py") 
            
    create_progress_table()
    username = st.session_state['username']
    st.title("📈 Weekly Progress Tracker")
    st.markdown("Welcome to your dashboard! Here's how you're progressing each week:")

    # Session state for editing and temporary goal inputs
    if "edit_mode" not in st.session_state:
        st.session_state["edit_mode"] = False
    if "temp_goals" not in st.session_state:
        st.session_state["temp_goals"] = {}

    def toggle_edit_mode():
        st.session_state["edit_mode"] = not st.session_state["edit_mode"]
        if not st.session_state["edit_mode"]:
            st.session_state["temp_goals"] = {}

    def add_temp_goal(week):
        st.session_state["temp_goals"].setdefault(week, []).append("")

    st.button("✏️ Edit Goals", on_click=toggle_edit_mode)

    # Get current progress
    data = get_progress(username)
    if data:
        df = pd.DataFrame(data, columns=["Week", "Goal", "Completed", "Suggestions"])
        df["Week"] = df["Week"].apply(lambda w: int(w.decode()) if isinstance(w, bytes) else int(w))
    else:
        df = pd.DataFrame(columns=["Week", "Goal", "Completed", "Suggestions"])

    if st.session_state["edit_mode"]:
        st.subheader("📝 Edit Your Weekly Goals")

        all_weeks = sorted(df["Week"].unique()) if not df.empty else []
        existing_weeks = set(all_weeks)

        with st.expander("➕ Add Goals for a New Week"):
            new_week = st.number_input("New Week Number", min_value=1, step=1, key="new_week_input")
            if st.button("Add Goal Box", key="new_week_add_btn"):
                add_temp_goal(new_week)

            for i, goal in enumerate(st.session_state["temp_goals"].get(new_week, [])):
                st.session_state["temp_goals"][new_week][i] = st.text_input(f"New Goal {i + 1} for Week {new_week}",
                                                                            value=goal,
                                                                            key=f"new_goal_{new_week}_{i}")
            if st.button(f"Submit Goals for Week {new_week}", key=f"submit_new_week_goals"):
                for goal in st.session_state["temp_goals"].get(new_week, []):
                    if goal.strip():
                        store_progress(username, new_week, goal.strip(), False)
                st.success(f"Goals added for Week {new_week}")
                st.session_state["temp_goals"].pop(new_week, None)
                st.rerun()

        # Edit existing goals
        for week in sorted(existing_weeks):
            with st.expander(f"Week {week}"):
                week_goals = df[df["Week"] == week]
                for _, row in week_goals.iterrows():
                    col1, col2 = st.columns([0.85, 0.15])
                    with col1:
                        st.text(row["Goal"])
                    with col2:
                        if st.button("🗑️", key=f"delete_{week}_{row['Goal']}"):
                            delete_single_goal(username, week, row["Goal"])
                            st.rerun()

                if st.button(f"Add Goal Box for Week {week}", key=f"add_btn_week_{week}"):
                    add_temp_goal(week)

                for i, goal in enumerate(st.session_state["temp_goals"].get(week, [])):
                    st.session_state["temp_goals"][week][i] = st.text_input(
                        f"New Goal {i + 1} for Week {week}",
                        value=goal,
                        key=f"input_week_{week}_{i}"
                    )

                if st.button(f"Submit New Goals for Week {week}", key=f"submit_btn_week_{week}"):
                    for goal in st.session_state["temp_goals"].get(week, []):
                        if goal.strip():
                            store_progress(username, week, goal.strip(), False)
                    st.success(f"Goals updated for Week {week}")
                    st.session_state["temp_goals"].pop(week, None)
                    st.rerun()

    # Fetch data again after edits
    data = get_progress(username)
    if not data:
        st.info("No progress data available yet.")
        st.stop()

    df = pd.DataFrame(data, columns=["Week", "Goal", "Completed", "Suggestions"])

    # ✅ Update Progress
    st.subheader("✅ Update Your Progress")
    grouped = df.groupby("Week")
    for week, group in grouped:
        st.markdown(f"### Week {int(week)}")
        for i, row in group.iterrows():
            checkbox_key = f"{row['Week']}_{i}"
            checked = st.checkbox(row["Goal"], value=row["Completed"], key=checkbox_key)
            if checked != row["Completed"]:
                store_progress(username, row["Week"], row["Goal"], checked)
                st.rerun()
    # 🎯 Weekly Completion Stats
    df["Completed (%)"] = df.groupby("Week")["Completed"].transform(lambda x: 100 * x.sum() / len(x))

    # 📊 Bar Chart
    st.subheader("📊 Weekly Progress Overview")

    custom_blues = [(0.0, "#add8e6"),  # light blue
                (0.5, "#4682b4"),  # steel blue
                (1.0, "#08306b")]  # dark navy blue
    
    bar_data = df.drop_duplicates("Week")
    bar_chart = px.bar(bar_data, x="Week", y="Completed (%)", color="Completed (%)",
                       color_continuous_scale=custom_blues, title="Weekly Progress")
    st.plotly_chart(bar_chart, use_container_width=True)

    # 🥧 Pie Chart
    st.subheader("🥧 Overall Completion Ratio")
    completed = df["Completed"].sum()
    incomplete = len(df) - completed
    pie_data = pd.DataFrame({"Status": ["Completed", "Incomplete"], "Count": [completed, incomplete]})
    pie_chart = px.pie(pie_data, names="Status", values="Count", title="Overall Progress")
    st.plotly_chart(pie_chart, use_container_width=True)

    # 💡 Suggestions
    st.subheader("🎯 Weekly Feedback")
    for week, group in grouped:
        st.markdown(f"### Week {int(week)}")
        if all(group["Completed"]):
            st.success("Awesome! All goals completed for this week 👏")
        else:
            st.warning("Try focusing on incomplete goals. Stay consistent 💪")
        st.markdown("---")

progress_dashboard()