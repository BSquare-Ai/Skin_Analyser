import numpy as np
import cv2


def estimate_head_pose(landmarks, frame_shape):

    h, w, _ = frame_shape

    try:
        nose = landmarks.landmark[1]
        left_eye = landmarks.landmark[33]
        right_eye = landmarks.landmark[263]
        chin = landmarks.landmark[152]
    except:
        return 0, 0, 0   # ✅ FIX

    # Convert to pixel coordinates
    nose_point = np.array([nose.x * w, nose.y * h])
    left_eye_point = np.array([left_eye.x * w, left_eye.y * h])
    right_eye_point = np.array([right_eye.x * w, right_eye.y * h])
    chin_point = np.array([chin.x * w, chin.y * h])

    # --------------------------------------------------
    # 1️⃣ YAW (left-right)
    # --------------------------------------------------
    eye_center = (left_eye_point + right_eye_point) / 2
    yaw_vector = nose_point - eye_center
    yaw_angle = np.degrees(np.arctan2(yaw_vector[0], yaw_vector[1]))

    # --------------------------------------------------
    # 2️⃣ PITCH (up-down)
    # --------------------------------------------------
    vertical_vector = chin_point - nose_point
    pitch_angle = np.degrees(np.arctan2(vertical_vector[1], vertical_vector[0]))

    # --------------------------------------------------
    # 3️⃣ ROLL (optional, simple approx)
    # --------------------------------------------------
    eye_diff = right_eye_point - left_eye_point
    roll_angle = np.degrees(np.arctan2(eye_diff[1], eye_diff[0]))

    return float(yaw_angle), float(pitch_angle), float(roll_angle)