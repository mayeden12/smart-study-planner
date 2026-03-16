import streamlit as st
import api_client as api


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Smart Study Planner", page_icon="📚", layout="wide")

    try:
        local_css("frontend/assets/style.css")
    except:
        pass

    # --- Premium Sidebar Menu ---
    with st.sidebar:
        st.title("Menu")
        st.markdown("---")
        menu_selection = st.radio(
            "Navigation",
            ["🏠 Home & Schedule", "🚀 Learning Hub", "🛠️ Preferences", "📖 Info"],
            label_visibility="collapsed"
        )
        st.markdown("---")
        st.caption("Powered by Local AI Engine")

    # --- Main Content Routing ---
    if menu_selection == "🏠 Home & Schedule":
        st.title("👋 Welcome to BrainBoost")
        st.subheader("Your Daily Focus")
        
        st.markdown("Select a date below to view your goals for the day, track progress, and mark things as done.")
        
        # Visual Calendar Picker
        selected_date = st.date_input("📅 Select a Day", help="Click to open the monthly calendar")
        selected_date_str = str(selected_date)
        
        st.divider()
        
        topics = api.fetch_topics()
        daily_topics = [
            t for t in topics 
            if t.get("due_date") and str(t.get("due_date")).split("T")[0] == selected_date_str
        ]
        
        if not daily_topics:
            st.info("No study sessions scheduled for this day. Enjoy your free time! 🎉")
        else:
            # Calculate daily progress
            done_topics = [t for t in daily_topics if t.get("status") == "done"]
            progress = len(done_topics) / len(daily_topics)
            st.progress(progress, text=f"Daily Progress: {len(done_topics)} out of {len(daily_topics)} completed")
            
            st.markdown(f"### 🗓️ Schedule for {selected_date.strftime('%b %d, %Y')}")
            
            for t in daily_topics:
                with st.container(border=True):
                    col1, col2 = st.columns([0.8, 0.2])
                    with col1:
                        status_emoji = "✅" if t.get("status") == "done" else "⏳"
                        fav_icon = "⭐" if t.get("is_favorite") else ""
                        st.markdown(f"**{status_emoji} {fav_icon} {t['title']}**")
                        if t.get("description"):
                            st.caption(t["description"])
                    with col2:
                        if t.get("status") != "done":
                            if st.button("✔️ Mark Done", key=f"done_{t['id']}"):
                                api.update_topic(t['id'], {"status": "done"})
                                st.rerun()
                        else:
                            st.success("Done!")

    elif menu_selection == "🚀 Learning Hub":
        st.title("🧠 BrainBoost Learning Tracker")
        st.caption("Manage your subjects and unlock AI-powered insights for faster learning.")

        # Moved form into an expander to change the layout look
        with st.expander("➕ Add a New Subject", expanded=False):
            with st.form("new_topic_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    title = st.text_input("Subject / Topic Name (Required)")
                    desc = st.text_area("Key Notes")
                with col2:
                    status = st.selectbox("Current Status", ["todo", "in_progress", "done"])
                    due_date = st.date_input("Exam Deadline")
                
                submit_btn = st.form_submit_button("💾 Save Subject")
            if submit_btn:
                if title.strip():
                    api.create_topic({
                        "title": title.strip(),
                        "description": desc.strip(),
                        "status": status,
                        "due_date": str(due_date) if due_date else None
                    })
                    st.rerun()

        st.markdown("---")
        st.subheader("📚 Active Subjects")
        topics = api.fetch_topics()
        
        if not topics:
            st.info("No subjects added yet. Create one above to get started!")
        else:
            for t in topics:
                fav_icon = "⭐" if t.get("is_favorite") else "☆"
                status_emoji = {"todo": "⏳", "in_progress": "🔄", "done": "✅"}.get(t["status"], "📋")
                
                with st.expander(f"{status_emoji} {fav_icon} {t['title']}"):
                    if t.get("description"):
                        st.markdown(f"**Notes:** {t['description']}")
                    if t.get("due_date"):
                        st.markdown(f"**Deadline:** {t['due_date']}")
                    
                    st.divider()
                    
                    b1, b2, b3, _ = st.columns([1, 1, 1.5, 3])
                    if b1.button("⭐ Pin", key=f"fav_{t['id']}"):
                        api.update_topic(t['id'], {"is_favorite": not t.get("is_favorite")})
                        st.rerun()
                    if b2.button("🗑️ Drop", key=f"del_{t['id']}"):
                        api.delete_topic(t['id'])
                        st.rerun()
                    if b3.button("💡 Generate Insight", key=f"hack_{t['id']}"):
                        with st.spinner("AI is thinking..."):
                            api.generate_study_hack(t['id'])
                            st.rerun()
                    
                    if t.get("study_hack"):
                        st.info(f"**⚡ AI Flash-Insight:**\n\n{t['study_hack']}")

    elif menu_selection == "🛠️ Preferences":
        st.title("⚙️ System Settings")
        with st.container(border=True):
            st.write("**Backend Server Connection:**")
            st.code(api.API_URL, language="bash")
            st.write("**AI Model Version:**")
            st.info("TinyLlama (Local Engine)")

    elif menu_selection == "📖 Info":
        st.title("ℹ️ How to Use")
        with st.container(border=True):
            st.markdown("""
            1. Select a date on the **Home** page to add items to your schedule.
            2. Go to the **Learning Hub** to view all subjects and expand them to see notes.
            3. Click **💡 Generate Insight** to trigger the AI for a rapid learning strategy!
            """)


if __name__ == "__main__":
    main()