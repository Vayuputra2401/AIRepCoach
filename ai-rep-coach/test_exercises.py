import unittest
from exercises import BicepCurl, PushUp, ShoulderPress, FrontRaise
import mediapipe as mp

class MockLandmark:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def create_mock_landmarks(points):
    """
    Creates a list of mock landmarks.
    points: dict of {landmark_id: (x, y)}
    """
    landmarks = [MockLandmark(0, 0)] * 33 # Initialize all
    for id, (x, y) in points.items():
        landmarks[id] = MockLandmark(x, y)
    return landmarks

class TestExercises(unittest.TestCase):
    def test_bicep_curl(self):
        curl = BicepCurl()
        
        # Down position (approx 180 degrees)
        # Shoulder (0, 0), Elbow (0, 1), Wrist (0, 2)
        landmarks_down = create_mock_landmarks({
            mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value: (0, 0),
            mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value: (0, 1),
            mp.solutions.pose.PoseLandmark.LEFT_WRIST.value: (0, 2)
        })
        curl.process(landmarks_down)
        self.assertEqual(curl.stage, "down")
        
        # Up position (approx 0 degrees)
        # Shoulder (0, 0), Elbow (0, 1), Wrist (0, 0)
        landmarks_up = create_mock_landmarks({
            mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value: (0, 0),
            mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value: (0, 1),
            mp.solutions.pose.PoseLandmark.LEFT_WRIST.value: (0, 0.1) # Close to shoulder
        })
        curl.process(landmarks_up)
        self.assertEqual(curl.stage, "up")
        self.assertEqual(curl.counter, 1)

if __name__ == '__main__':
    unittest.main()
