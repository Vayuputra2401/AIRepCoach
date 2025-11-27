import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from pose_engine import PoseEngine
from exercises import BicepCurl, PushUp, ShoulderPress, FrontRaise, ShoulderRotation, NeckRotation
from gemini_coach import GeminiCoach
from utils import draw_angles
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Rep Coach", layout="wide")

st.title("AI Rep Coach 🏋️‍♂️")
st.subheader("Your personal AI-powered fitness assistant")

# Sidebar
st.sidebar.title("Settings")
exercise_option = st.sidebar.selectbox(
    "Select Exercise",
    ("Bicep Curl", "Push Up", "Shoulder Press", "Front Raise", "Shoulder Rotation", "Neck Rotation")
)

# Load API Key from env or sidebar
env_api_key = os.getenv("GEMINI_API_KEY", "")
api_key = st.sidebar.text_input("Gemini API Key", value=env_api_key, type="password")

# Initialize components
if 'pose_engine' not in st.session_state:
    st.session_state.pose_engine = PoseEngine()

if 'coach' not in st.session_state or st.session_state.get('api_key') != api_key:
    st.session_state.coach = GeminiCoach(api_key)
    st.session_state.api_key = api_key

# Exercise selection logic
if 'current_exercise_name' not in st.session_state or st.session_state.current_exercise_name != exercise_option:
    if exercise_option == "Bicep Curl":
        st.session_state.exercise = BicepCurl()
    elif exercise_option == "Push Up":
        st.session_state.exercise = PushUp()
    elif exercise_option == "Shoulder Press":
        st.session_state.exercise = ShoulderPress()
    elif exercise_option == "Front Raise":
        st.session_state.exercise = FrontRaise()
    elif exercise_option == "Shoulder Rotation":
        st.session_state.exercise = ShoulderRotation()
    elif exercise_option == "Neck Rotation":
        st.session_state.exercise = NeckRotation()
    st.session_state.current_exercise_name = exercise_option

exercise = st.session_state.exercise
pose_engine = st.session_state.pose_engine
coach = st.session_state.coach

# Layout
col1, col2 = st.columns([2, 1])

with col2:
    st.markdown("### Metrics")
    reps_placeholder = st.empty()
    stage_placeholder = st.empty()
    feedback_placeholder = st.empty()
    
    st.markdown("---")
    st.markdown("### Coach's Corner 🗣️")
    ai_message_placeholder = st.empty()
    
    st.markdown("---")
    st.markdown("### Live Angles 📐")
    angles_placeholder = st.empty()

run = st.checkbox('Start Camera', value=True)
FRAME_WINDOW = col1.image([])

cap = cv2.VideoCapture(0)

last_feedback = "Ready to start!"

while run:
    ret, frame = cap.read()
    if not ret:
        st.write("Failed to access camera")
        break
    
    # Process frame
    image, results = pose_engine.process_frame(frame)
    
    try:
        landmarks = results.pose_landmarks.landmark
        
        # Exercise Logic
        angles, keypoint = exercise.process(landmarks)
        
        # Visualization
        draw_angles(image, angles)
        
        # Update Metrics
        metrics = exercise.get_metrics()
        reps_placeholder.metric("Reps", metrics["reps"])
        stage_placeholder.text(f"Stage: {metrics['stage']}")
        
        # Display Angles in Sidebar
        angle_text = ""
        for label, (val, _) in metrics["angles"].items():
            angle_text += f"**{label}**: {int(val)}°\n\n"
        angles_placeholder.markdown(angle_text)
        
        if metrics["warnings"]:
            feedback_placeholder.error(f"⚠️ {metrics['warnings'][0]}")
        else:
            feedback_placeholder.success("Form looks good!")
            
        # AI Coach
        ai_feedback = coach.get_feedback(
            exercise.name, 
            metrics["reps"], 
            metrics["stage"], 
            metrics["warnings"],
            metrics["angles"]
        )
        
        if ai_feedback:
            last_feedback = ai_feedback
            
        ai_message_placeholder.info(f"🤖 Coach: {last_feedback}")
        
    except Exception as e:
        pass # Landmarks might not be visible
        
    # Draw landmarks
    image = pose_engine.draw_landmarks(image, results)
    
    FRAME_WINDOW.image(image)

cap.release()
