# Implementation Plan - AI Rep Coach

This application will be an expanded version of the existing fitness tracker, built with Streamlit, MediaPipe, and Gemini. It will focus on upper body exercises and provide real-time feedback and motivation.

## Goal
Create a modular, scalable Streamlit application that tracks upper body exercises, counts reps, and uses a Gemini-powered agent for posture correction and motivation.

## User Review Required
> [!IMPORTANT]
> **Gemini API Key**: The application will require a Google Gemini API key to function. I will add a field in the Streamlit sidebar for you to enter this key, or it can be loaded from an environment variable.

## Proposed Architecture
The application will be divided into the following modules for scalability and readability:

### 1. `pose_engine.py`
- Wraps MediaPipe Pose solution.
- Handles frame processing and landmark extraction.

### 2. `exercises.py`
- Update `Exercise` class to return a list of angles for visualization.
- **Update Existing Exercises**:
    - `BicepCurl`: Add body sway angle (shoulder-hip-knee).
    - `PushUp`: Add elbow flare angle (shoulder-elbow-wrist relative to body) and body alignment.
    - `ShoulderPress`: Add elbow flare and back stability.
    - `FrontRaise`: Add back stability.
- **New Exercises**:
    - `ShoulderRotation`: Calculate angles for internal/external rotation (needs careful landmark selection, possibly elbow-shoulder-hip plane).
    - `NeckRotation`: Calculate nose-shoulder alignment or ear-shoulder angles (MediaPipe Face Mesh might be better, but Pose has nose/ears).
- **Refinement**:
    - Ensure `process` returns a dictionary of angles `{label: (value, point)}` for the UI to draw.

### 3. `gemini_coach.py`
- **Improvements**:
    - Add "Session Context": Track the history of feedback to avoid repetition.
    - specialized prompts: Differentiate between "Form Correction" (high priority) and "Motivation" (lower priority).
    - Dynamic Prompts: Inject random variations in the system prompt to vary the persona (e.g., "Drill Sergeant", "Supportive Friend").

### 4. `utils.py`
- Update `draw_angle` to handle a list/dict of angles.

### 5. `app.py`
- Update the visualization loop to iterate through the returned angles and draw them.
- Add new exercises to the sidebar.

## Verification Plan

### Automated Tests
- I will write a simple test script to verify that `exercises.py` logic correctly transitions states given mock landmark data.

### Manual Verification
- Run `streamlit run app.py`.
- Test each exercise with the webcam.
- Verify Gemini provides feedback when "bad form" is simulated or reps are completed.
