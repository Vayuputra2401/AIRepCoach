import numpy as np
import mediapipe as mp
from utils import calculate_angle

class Exercise:
    def __init__(self, name):
        self.name = name
        self.counter = 0
        self.stage = None
        self.form_warnings = []
        self.angles = {} # Dictionary {label: (value, position)}

    def process(self, landmarks):
        """
        Process landmarks to count reps and check form.
        Should be implemented by subclasses.
        Returns:
            angles: dict of {label: (value, position)}
            keypoint: main keypoint for visualization (deprecated, use angles dict)
        """
        raise NotImplementedError

    def get_metrics(self):
        return {
            "reps": self.counter,
            "stage": self.stage,
            "warnings": self.form_warnings,
            "angles": self.angles
        }
    
    def reset(self):
        self.counter = 0
        self.stage = None
        self.form_warnings = []
        self.angles = {}

class BicepCurl(Exercise):
    def __init__(self):
        super().__init__("Bicep Curl")

    def process(self, landmarks):
        self.form_warnings = []
        self.angles = {}
        
        # Get coordinates
        shoulder = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].x,
                 landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].x,
                 landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].y]
        hip = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x,
               landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y]
        
        # Main Curl Angle
        curl_angle = calculate_angle(shoulder, elbow, wrist)
        self.angles["Curl"] = (curl_angle, elbow)
        
        # Body Sway Angle (Shoulder-Hip-Vertical or similar, simplified to Shoulder-Hip-Knee if visible, or just check if elbow moves too much)
        # Here we check Elbow-Shoulder-Hip to see if elbow is swinging forward
        swing_angle = calculate_angle(elbow, shoulder, hip)
        self.angles["Swing"] = (swing_angle, shoulder)

        # Curl logic
        if curl_angle > 160:
            self.stage = "down"
        if curl_angle < 30 and self.stage == 'down':
            self.stage = "up"
            self.counter += 1
            
        # Form checks
        if swing_angle < 10: # Elbow moving too far back/forward relative to body
             self.form_warnings.append("Keep your elbow fixed at your side!")
            
        return self.angles, elbow

class PushUp(Exercise):
    def __init__(self):
        super().__init__("Push Up")
        
    def process(self, landmarks):
        self.form_warnings = []
        self.angles = {}
        
        # Get coordinates
        shoulder = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].x,
                 landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].x,
                 landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].y]
        hip = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x,
               landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y]
        ankle = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].x,
                 landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].y]
        
        # Elbow Angle
        elbow_angle = calculate_angle(shoulder, elbow, wrist)
        self.angles["Elbow"] = (elbow_angle, elbow)
        
        # Body Alignment
        body_angle = calculate_angle(shoulder, hip, ankle)
        self.angles["Body"] = (body_angle, hip)

        # Pushup logic
        if elbow_angle > 160:
            self.stage = "up"
        if elbow_angle < 90 and self.stage == 'up':
            self.stage = "down"
            self.counter += 1
            
        # Form check
        if body_angle < 160:
             self.form_warnings.append("Keep your back straight!")
             
        return self.angles, elbow

class ShoulderPress(Exercise):
    def __init__(self):
        super().__init__("Shoulder Press")

    def process(self, landmarks):
        self.form_warnings = []
        self.angles = {}
        
        # Get coordinates
        shoulder = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].x,
                 landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].x,
                 landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].y]
        hip = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x,
               landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y]
        
        # Press Angle
        press_angle = calculate_angle(shoulder, elbow, wrist)
        self.angles["Press"] = (press_angle, elbow)
        
        # Elbow Flare (Elbow-Shoulder-Hip) - should be around 90 or slightly less, not too high/low
        flare_angle = calculate_angle(elbow, shoulder, hip)
        self.angles["Flare"] = (flare_angle, shoulder)
        
        # Press logic
        if press_angle < 70:
            self.stage = "down"
        if press_angle > 160 and self.stage == 'down':
            self.stage = "up"
            self.counter += 1
            
        return self.angles, elbow

class FrontRaise(Exercise):
    def __init__(self):
        super().__init__("Front Raise")

    def process(self, landmarks):
        self.form_warnings = []
        self.angles = {}
        
        # Get coordinates
        hip = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x,
               landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y]
        shoulder = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y]
        wrist = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].x,
                 landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].y]
        
        # Raise Angle
        raise_angle = calculate_angle(hip, shoulder, wrist)
        self.angles["Raise"] = (raise_angle, shoulder)
        
        # Raise logic
        if raise_angle < 20:
            self.stage = "down"
        if raise_angle > 80 and self.stage == 'down':
            self.stage = "up"
            self.counter += 1
            
        # Form: Don't go too high
        if raise_angle > 100:
            self.form_warnings.append("Don't raise above shoulder level!")
            
        return self.angles, shoulder

class ShoulderRotation(Exercise):
    def __init__(self):
        super().__init__("Shoulder Rotation")
        
    def process(self, landmarks):
        self.form_warnings = []
        self.angles = {}
        
        # External/Internal Rotation
        # Best viewed from front/side with elbow at 90 degrees
        # Points: Wrist, Elbow, Hip (or Shoulder if arm is abducted)
        
        shoulder = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].x,
                 landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].x,
                 landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].y]
        hip = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x,
               landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y]
        
        # 1. Elbow Flexion (should be ~90)
        elbow_flexion = calculate_angle(shoulder, elbow, wrist)
        self.angles["Elbow Flex"] = (elbow_flexion, elbow)
        
        # 2. Rotation Angle (Wrist-Elbow-Hip) - Approximate for 2D
        # If elbow is pinned to side:
        # 0 deg = hand at belly (Internal)
        # 90 deg = hand straight forward (Neutral)
        # 180 deg = hand out to side (External)
        rotation_angle = calculate_angle(wrist, elbow, hip)
        self.angles["Rotation"] = (rotation_angle, wrist)
        
        # Logic
        # Assume starting neutral/internal and rotating out
        if rotation_angle < 45:
            self.stage = "in"
        if rotation_angle > 80 and self.stage == "in":
            self.stage = "out"
            self.counter += 1
            
        if elbow_flexion > 110 or elbow_flexion < 70:
            self.form_warnings.append("Keep elbow bent at 90 degrees")
            
        return self.angles, elbow

class NeckRotation(Exercise):
    def __init__(self):
        super().__init__("Neck Rotation")
        
    def process(self, landmarks):
        self.form_warnings = []
        self.angles = {}
        
        # Neck Rotation (Side to Side)
        # Using Nose and Shoulders
        nose = [landmarks[mp.solutions.pose.PoseLandmark.NOSE.value].x,
                landmarks[mp.solutions.pose.PoseLandmark.NOSE.value].y]
        l_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x,
                      landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y]
        r_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                      landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        
        # Calculate angle between Nose and Left Shoulder
        l_angle = calculate_angle(r_shoulder, l_shoulder, nose) # Angle at L shoulder? No.
        
        # Better: Angle of Nose relative to the Shoulder line center?
        # Let's use Nose-Shoulder-Shoulder angle?
        # Or simply Nose x-position relative to shoulders.
        
        # Let's try Angle: Nose - MidShoulder - Vertical?
        # MidShoulder
        mid_shoulder = [(l_shoulder[0] + r_shoulder[0])/2, (l_shoulder[1] + r_shoulder[1])/2]
        
        # Angle between Nose, MidShoulder, and a point directly above MidShoulder (Vertical)
        vertical_point = [mid_shoulder[0], mid_shoulder[1] - 0.5]
        
        neck_tilt = calculate_angle(nose, mid_shoulder, vertical_point)
        self.angles["Neck Tilt"] = (neck_tilt, nose)
        
        # Logic: Looking Left/Right
        # In 2D, rotation looks like the nose moving towards a shoulder.
        # We can check the distance or angle to each shoulder.
        
        dist_l = np.linalg.norm(np.array(nose) - np.array(l_shoulder))
        dist_r = np.linalg.norm(np.array(nose) - np.array(r_shoulder))
        
        # Normalize by shoulder width
        shoulder_width = np.linalg.norm(np.array(l_shoulder) - np.array(r_shoulder))
        
        # Heuristic
        if dist_l < shoulder_width * 0.4:
            self.stage = "left"
        elif dist_r < shoulder_width * 0.4:
            self.stage = "right"
            if self.stage == "left": # Completed a cycle? Or just count every side?
                pass
        else:
            if self.stage == "left" or self.stage == "right":
                 # Returned to center
                 pass
        
        # Simplified counter: Count when returning to center from a side?
        # Let's count Left -> Center -> Right -> Center as 1?
        # Or just Left -> Right as 1.
        
        # Let's go with: Tilt > 30 deg is a "rep" if we alternate.
        # Simplified: Just count tilts.
        if neck_tilt > 20:
             if self.stage == "center":
                 self.stage = "turned"
                 self.counter += 1
        else:
             self.stage = "center"

        return self.angles, nose
