from google import genai
import time
import random

class GeminiCoach:
    def __init__(self, api_key):
        self.api_key = api_key
        if api_key:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = None
            
        self.last_feedback_time = 0
        self.feedback_cooldown = 8 # Increased cooldown slightly
        self.history = [] # Keep track of last few messages to avoid repetition

    def get_feedback(self, exercise_name, reps, stage, warnings, angles):
        """
        Generates feedback based on the current exercise state.
        """
        if not self.client:
            return "Please enter a valid Gemini API Key in the sidebar to enable the AI Coach."

        current_time = time.time()
        if current_time - self.last_feedback_time < self.feedback_cooldown:
            return None

        # Dynamic Persona/Style
        styles = [
            "motivational and high energy",
            "technical and precise",
            "supportive and encouraging",
            "like a drill sergeant"
        ]
        style = random.choice(styles)

        # Context Construction
        angle_info = ", ".join([f"{k}: {int(v[0])}" for k, v in angles.items()])
        
        prompt = f"""
        You are a fitness coach. The user is doing {exercise_name}.
        Current Reps: {reps}
        Current Stage: {stage}
        Form Warnings: {', '.join(warnings) if warnings else 'None'}
        Key Angles: {angle_info}
        
        Previous Feedback: {self.history[-3:] if self.history else 'None'}
        
        Task: Provide a short feedback message (under 20 words).
        Style: {style}
        
        Priority:
        1. If there are Form Warnings, correct them immediately.
        2. If Reps are increasing, motivate them.
        3. If nothing special, comment on their form or angles.
        
        Do not repeat previous feedback exactly.
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            feedback = response.text
            self.history.append(feedback)
            self.last_feedback_time = current_time
            return feedback
        except Exception as e:
            return f"Error connecting to Coach: {str(e)}"
