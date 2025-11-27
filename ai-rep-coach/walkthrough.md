# AI Rep Coach - Walkthrough

This is a modular, AI-powered fitness tracker application built with Streamlit, MediaPipe, and Google Gemini.

## Features
- **Real-time Rep Counting**: Tracks Bicep Curls, Push Ups, Shoulder Presses, Front Raises, **Shoulder Rotations**, and **Neck Rotations**.
- **Comprehensive Angle Tracking**: Visualizes multiple key angles for each exercise (e.g., Elbow Flexion + Body Sway) to ensure perfect form.
- **Smart AI Coach**: Integrated with Google Gemini to provide **context-aware** motivation and feedback. It remembers your session history to avoid repetitive advice.
- **Privacy First**: All processing happens locally (except for the text prompt sent to Gemini).

## Prerequisites
- **Python 3.9 - 3.11** (Recommended: 3.11). *Note: MediaPipe may not support Python 3.12+ yet.*
- **Webcam**

## Installation
1.  Navigate to the `ai-rep-coach` directory:
    ```bash
    cd ai-rep-coach
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```
2.  **Settings**:
    - Select your exercise from the sidebar.
    - Enter your **Google Gemini API Key** in the sidebar to enable the AI Coach.
3.  **Start Working Out**:
    - Stand back so the camera can see your full upper body.
    - Follow the "Stage" indicator (UP/DOWN).
    - Listen to the Coach's feedback!

## Code Structure
- `app.py`: Main application entry point and UI.
- `exercises.py`: Logic for each exercise (angles, states, counting).
- `pose_engine.py`: MediaPipe Pose wrapper.
- `gemini_coach.py`: Interface for the Gemini API.
- `utils.py`: Helper functions for geometry and drawing.
