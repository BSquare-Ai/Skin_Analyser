import cv2
import numpy as np


def analyze_skin_patches(patch, frame=None, box=None):

    if patch is None or patch.size == 0:
        return {}

    # Resize patch for consistency
    patch = cv2.resize(patch, (128, 128))

    # Convert to grayscale
    gray = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)


    # --------------------------------
    # WRINKLE DETECTION
    # --------------------------------
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)

    wrinkle_score = np.var(laplacian)
    wrinkle_score = min(100, wrinkle_score / 8)


    # --------------------------------
    # TEXTURE DETECTION
    # --------------------------------
    texture_score = np.std(gray)
    texture_score = min(100, texture_score * 1.2)


    # --------------------------------
    # PIGMENTATION DETECTION
    # --------------------------------
    hsv = cv2.cvtColor(patch, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(hsv)

    pigmentation_score = np.std(v)
    pigmentation_score = min(100, pigmentation_score * 1.1)


    # --------------------------------
    # DAMAGE + HEALTH SCORE
    # --------------------------------
    damage = (
        wrinkle_score * 0.4 +
        texture_score * 0.3 +
        pigmentation_score * 0.3
    )

    health_score = 100 - damage

    health_score = max(0, min(100, health_score))


    results = {

        "Skin Health Score": float(round(health_score, 2)),
        "Wrinkle Score": float(round(wrinkle_score, 2)),
        "Pigmentation Score": float(round(pigmentation_score, 2)),
        "Texture Score": float(round(texture_score, 2)),
        "Dark Circles Score": 0

    }


    # --------------------------------
    # OPTIONAL VISUAL OVERLAY
    # --------------------------------
    if frame is not None and box is not None:

        x, y, w, h = box

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.putText(
            frame,
            f"W:{results['Wrinkle Score']:.0f}",
            (x, y - 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"T:{results['Texture Score']:.0f}",
            (x, y - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"P:{results['Pigmentation Score']:.0f}",
            (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )

    return results