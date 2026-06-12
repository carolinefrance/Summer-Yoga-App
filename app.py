import streamlit as st
import time
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- STATE MANAGEMENT ---
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "duration_mins" not in st.session_state:
    st.session_state.duration_mins = 0.0
# Add a state variable to hold the completed plank time so it auto-fills the form
if "plank_completed_mins" not in st.session_state:
    st.session_state.plank_completed_mins = 0.0

st.set_page_config(page_title="Summer Yoga Challenge", page_icon="🧘‍♀️", layout="centered")
st.title("Summer Fitness Challenge ☀️")

tab1, tab2, tab3 = st.tabs(["🧘‍♀️ Class Review", "💪 Daily Metrics", "🏋️‍♀️ Weight Training"])

# --- TAB 1: YOGA CLASS REVIEW ---
with tab1:
    st.header("Post-Class Evaluation")
    with st.form("yoga_eval_form"):
        st.subheader("Teacher & Class Stats")
        teacher = st.selectbox("Teacher", ["Wednesday Cooper", "Other"]) 
        
        st.markdown("### Metrics (1-5 Stars)")
        col1, col2 = st.columns(2)
        with col1:
            rating = st.slider("Overall Sentiment", 1, 5, 5)
            verbal = st.slider("Verbal Cues", 1, 5, 5)
        with col2:
            choreo = st.slider("Choreography", 1, 5, 5)
            music = st.slider("Music", 1, 5, 5)
            friendly = st.slider("Friendliness", 1, 5, 5)
            
        st.markdown("### Qualitative Notes")
        injuries = st.text_area("Injuries or Pain Points? (Before/After)")
        target_postures = st.text_area("Postures to work on?")
        best_worst = st.text_area("Best / Worst parts of class?")
        
        if st.form_submit_button("Save Yoga Evaluation"):
            st.success("Yoga Review Saved!")

# --- TAB 2: DAILY METRICS ---
with tab2:
    st.header("Daily Body Metrics")
    with st.form("daily_metrics_form"):
        col1, col2 = st.columns(2)
        with col1:
            # Assigning the inputs to variables so we can save them
            weight = st.number_input("Weight (lbs)", min_value=0.0, format="%.1f")
            chest = st.number_input("Chest (in)", min_value=0.0, format="%.1f")
            bicep = st.number_input("Bicep (in)", min_value=0.0, format="%.1f")
            water = st.number_input("Water (Cups)", min_value=0, step=1)
        with col2:
            waist = st.number_input("Waist (in)", min_value=0.0, format="%.1f")
            hips = st.number_input("Hips (in)", min_value=0.0, format="%.1f")
            thigh = st.number_input("Thigh (in)", min_value=0.0, format="%.1f")
            
        if st.form_submit_button("Save Daily Metrics"):
            # 1. Get today's date formatted perfectly
            today = datetime.today().strftime('%m/%d/%Y')
            
            # 2. Read the existing sheet (ttl=0 ensures we don't load a cached, old version)
            df = conn.read(worksheet="DailyMetrics", ttl=0).dropna(how="all")
            
            # 3. Create the new row (Headers must match your Google Sheet exactly)
            new_row = pd.DataFrame([{
                "Date": today, "Weight (lbs)": weight, "Chest": chest, 
                "Waist": waist, "Hips": hips, "Bicep": bicep, 
                "Thigh": thigh, "Water (Cups)": water
            }])
            
            # 4. Push back to Google Sheets!
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(worksheet="DailyMetrics", data=updated_df)
            
            st.success("✅ Daily Metrics successfully saved to Google Sheets!")

# --- TAB 3: WEIGHT TRAINING ---
with tab3:
    st.header("Weight Training Log")
    
    # 1. THE MAIN SESSION TIMER
    st.markdown("### Session Timer")
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        if st.button("▶️ Start Workout", use_container_width=True):
            st.session_state.start_time = time.time()
            st.session_state.duration_mins = 0.0 
    with t_col2:
        if st.button("⏹️ Stop Workout", use_container_width=True):
            if st.session_state.start_time is not None:
                elapsed = time.time() - st.session_state.start_time
                st.session_state.duration_mins = round(elapsed / 60, 2)
                st.session_state.start_time = None
            else:
                st.warning("You have to start the timer first!")
                
    if st.session_state.start_time is not None:
        st.info("⏱️ Workout in progress...")
    elif st.session_state.duration_mins > 0:
        st.success(f"✅ Workout complete: {st.session_state.duration_mins} minutes")

    st.divider()

    # 2. THE PLANK COUNTDOWN
    st.markdown("### Plank Countdown")
    plank_target = st.number_input("Set Plank Goal (Minutes)", min_value=1, max_value=20, value=5, step=1)
    
    if st.button("⏳ Start Plank", use_container_width=True):
        # We create an empty container to hold the live ticking clock
        timer_placeholder = st.empty()
        total_seconds = plank_target * 60
        
        # This loop will temporarily block the UI thread while you hold the plank
        for i in range(total_seconds, -1, -1):
            mins, secs = divmod(i, 60)
            # Update the placeholder with the current time
            timer_placeholder.markdown(f"<h1 style='text-align: center; color: #ff4b4b;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
            time.sleep(1)
            
        timer_placeholder.empty() # Clear the timer when done
        st.success(f"🎉 Awesome work! {plank_target} minute plank complete.")
        st.balloons()
        # Save to state so it populates the form below
        st.session_state.plank_completed_mins += float(plank_target)

    st.divider()

    # 3. THE DATA FORM
    with st.form("weight_training_form"):
        zone = st.radio(
            "Select Target Zone", 
            ["🏋️ Chest", "💪 Back", "🤷‍♀️ Shoulders", "🦵 Legs", "🦾 Arms"],
            horizontal=True
        )
        
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            duration = st.number_input("Total Duration (Mins)", value=st.session_state.duration_mins, min_value=0.0, format="%.2f")
        with col_form2:
            plank_mins = st.number_input("Plank Duration (Mins)", value=st.session_state.plank_completed_mins, min_value=0.0, format="%.2f")
        
        if st.form_submit_button("Save Workout"):
            today = datetime.today().strftime('%m/%d/%Y')
            
            # Read the YogaData sheet
            df_yoga = conn.read(worksheet="YogaData", ttl=0).dropna(how="all")
            
            # Create a new row for the workout
            new_workout = pd.DataFrame([{
                "Date": today,
                "Class Name": f"Weight Training: {zone}",
                "Duration (Mins)": duration,
                "Plank (Mins)": plank_mins
            }])
            
            # Push to Google Sheets
            updated_yoga_df = pd.concat([df_yoga, new_workout], ignore_index=True)
            conn.update(worksheet="YogaData", data=updated_yoga_df)
            
            st.success(f"✅ Saved {zone} workout to Google Sheets!")
    