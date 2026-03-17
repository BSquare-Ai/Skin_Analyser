import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import cv2
import mediapipe as mp
import numpy as np

from patch_analyzer import analyze_skin_patches
from face_regions import extract_skin_regions, draw_skin_regions
from skin_heatmap import draw_skin_heatmap
from skin_condition_interpreter import interpret_skin_conditions
from llm_recommender import get_product_recommendations
from clip_skin_analyzer import analyze_skin_clip


# -------------------------------
# INIT
# -------------------------------
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
)

cap = cv2.VideoCapture(0)

print("Press Q to quit")

report = {}
last_recommendation = "Waiting..."


# -------------------------------
# MAIN LOOP
# -------------------------------
while True:

    ret, frame = cap.read()
    if not ret or frame is None:
        continue

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:

        for landmarks in results.multi_face_landmarks:

            # -------------------------------
            # DRAW REGIONS
            # -------------------------------
            draw_skin_regions(frame, landmarks)

            # -------------------------------
            # EXTRACT REGIONS
            # -------------------------------
            regions, boxes = extract_skin_regions(frame, landmarks)

            if not regions:
                continue

            region_scores = []
            region_health = {}

            # -------------------------------
            # PATCH ANALYSIS
            # -------------------------------
            for name, region in regions.items():

                result = analyze_skin_patches(region)

                if result:
                    region_scores.append(result)
                    region_health[name] = result.get("Skin Health Score", 50)

            if len(region_scores) == 0:
                continue

            # -------------------------------
            # AGGREGATE SCORES
            # -------------------------------
            def avg(key):
                vals = [r.get(key, 50) for r in region_scores]
                return round(float(np.mean(vals)), 2)

            report = {
                "Skin Health": avg("Skin Health Score"),
                "Wrinkles": avg("Wrinkle Score"),
                "Pigmentation": avg("Pigmentation Score"),
                "Texture": avg("Texture Score"),
                "Dark Circles": avg("Dark Circles Score")
            }

            # -------------------------------
            # CLIP ANALYSIS (FULL FACE)
            # -------------------------------
            h, w, _ = frame.shape
            face_crop = frame[0:h, 0:w]

            clip_result = analyze_skin_clip(face_crop)

            # Merge CLIP insight (optional weight)
            if isinstance(clip_result, dict):
                report["Acne (CLIP)"] = int(clip_result.get("Acne_DL", 0) * 100)

            # -------------------------------
            # CONDITIONS
            # -------------------------------
            conditions = interpret_skin_conditions(report)

            # -------------------------------
            # LLM (Gemini)
            # -------------------------------
            lifestyle = {
                "sleep_hours": 7,
                "water_intake_liters": 2,
                "stress_level": "medium",
                "diet_type": "balanced",
                "skincare_routine": "yes"
            }

            try:
                last_recommendation = get_product_recommendations(
                    report, lifestyle, conditions
                )
            except:
                pass

            # -------------------------------
            # HEATMAP
            # -------------------------------
            frame = draw_skin_heatmap(
                frame,
                regions,
                region_health,
                boxes
            )

    # -------------------------------
    # DISPLAY TEXT
    # -------------------------------
    y = 30

    for key, value in report.items():
        cv2.putText(
            frame,
            f"{key}: {value}",
            (20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )
        y += 25

    # -------------------------------
    # SHOW WINDOW
    # -------------------------------
    cv2.imshow("AI Skin Analyzer", frame)

    key = cv2.waitKey(1)

    if key == ord('q') or key == ord('Q'):
        break


cap.release()
cv2.destroyAllWindows()