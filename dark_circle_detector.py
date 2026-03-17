import cv2
import numpy as np


def detect_dark_circles(under_eye_patch):

    if under_eye_patch is None or under_eye_patch.size == 0:
        return 0

    # Resize for stability
    patch = cv2.resize(under_eye_patch, (128,128))

    # Convert to grayscale
    gray = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)

    # Dark circle estimation based on darkness + texture
    mean_intensity = np.mean(gray)
    std_intensity = np.std(gray)

    # Lower brightness → more dark circles
    darkness = max(0, 150 - mean_intensity)

    score = darkness + std_intensity

    score = min(100, score * 0.8)

    return float(round(score,2))