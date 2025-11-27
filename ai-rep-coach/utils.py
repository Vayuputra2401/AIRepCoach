import numpy as np
import cv2

def calculate_angle(a, b, c):
    """
    Calculates the angle between three points a, b, and c.
    Points are expected to be [x, y] or [x, y, z] lists/arrays.
    The angle is calculated at point b.
    """
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
        
    return angle

def draw_angle(image, angle, position, label=None, color=(255, 255, 255)):
    """
    Draws the angle value on the image at the specified position.
    """
    text = str(int(angle))
    if label:
        text = f"{label}: {int(angle)}"
        
    cv2.putText(image, text, 
                tuple(np.multiply(position, [640, 480]).astype(int)), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)

def draw_angles(image, angles_dict):
    """
    Draws multiple angles from a dictionary {label: (value, position)}.
    """
    for label, (value, position) in angles_dict.items():
        draw_angle(image, value, position, label)

