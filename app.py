import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import gradio as gr
import cv2
import numpy as np
import mediapipe as mp


from dotenv import load_dotenv
load_dotenv()
from patch_analyzer import analyze_skin_patches
from face_regions import extract_skin_regions, draw_skin_regions
from skin_heatmap import draw_skin_heatmap
from skin_condition_interpreter import interpret_skin_conditions
from llm_recommender import get_product_recommendations
from clip_skin_analyzer import analyze_skin_clip
from head_pose import estimate_head_pose


# ---------- GLOBALS ----------
frame_counter = 0
last_recommendation = "Waiting for analysis..."
face_mesh = None

last_report = {}
last_region_health = {}
captured = False

# 🔥 ADD THIS
llm_called = False


# ---------- INIT FACEMESH ----------
def get_facemesh():
    global face_mesh

    if face_mesh is None:
        mp_face_mesh = mp.solutions.face_mesh

        face_mesh = mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        )

    return face_mesh


# ---------- MAIN ----------
def analyze_stream(frame, sleep, water, stress, diet, skincare):

    global frame_counter, last_recommendation
    global last_report, last_region_health, captured
    global llm_called  # 🔥 ADD THIS

    try:
        if frame is None:
            return None, "No frame received", last_recommendation

        frame = frame.copy()
        facemesh = get_facemesh()

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = facemesh.process(rgb)

        if not results.multi_face_landmarks:
            return rgb, "No face detected", last_recommendation

        landmarks = results.multi_face_landmarks[0]

        # ---------- HEAD POSE ----------
        yaw, pitch, roll = estimate_head_pose(landmarks, frame.shape)

        # ---------- DRAW ----------
        draw_skin_regions(frame, landmarks)

        # ---------- EXTRACT ----------
        regions, boxes = extract_skin_regions(frame, landmarks)
        if not regions:
            return rgb, "No regions detected", last_recommendation

        boxes = boxes or {}

        # ================================
        # 🟢 LIVE ANALYSIS
        # ================================
        region_scores = []
        region_health_live = {}

        for name, region in regions.items():
            result = analyze_skin_patches(region)

            if result:
                region_scores.append(result)
                region_health_live[name] = result.get("Skin Health Score", 50)

        def avg(key):
            vals = [r.get(key, 50) for r in region_scores]
            return round(float(np.mean(vals)), 2) if vals else 50

        live_report = {
            "Skin Health Score": avg("Skin Health Score"),
            "Wrinkle Score": avg("Wrinkle Score"),
            "Pigmentation Score": avg("Pigmentation Score"),
            "Texture Score": avg("Texture Score"),
            "Dark Circles Score": avg("Dark Circles Score"),
            "Acne": 0
        }

        # ================================
        # 🔴 CAPTURE
        # ================================
        if abs(yaw) > 60 and not captured:

            report = live_report.copy()

            h, w, _ = frame.shape
            face_crop = frame[0:h, 0:w]

            clip_result = analyze_skin_clip(face_crop)

            if isinstance(clip_result, dict):
                report["Acne"] = int(clip_result.get("Acne_DL", 0) * 100)

            last_report = report
            last_region_health = region_health_live
            captured = True

        # ================================
        # 🎯 OUTPUT SELECT
        # ================================
        if captured:
            report = last_report
            region_health = last_region_health
        else:
            report = live_report
            region_health = region_health_live

        # ---------- CONDITIONS ----------
        conditions = interpret_skin_conditions(report)

        # ---------- LIFESTYLE ----------
        lifestyle = {
            "sleep_hours": sleep,
            "water_intake_liters": water,
            "stress_level": stress,
            "diet_type": diet,
            "skincare_routine": skincare
        }

        # ================================
        # 🔥 FIXED LLM (ONLY ONCE EVER)
        # ================================
        if captured and not llm_called:
            try:
                last_recommendation = get_product_recommendations(
                    report,
                    lifestyle,
                    conditions
                )
                llm_called = True  # 🔒 LOCK AFTER FIRST CALL
            except Exception as e:
                print("LLM ERROR:", e)

        recommendation = last_recommendation

        # ---------- HEATMAP ----------
        heatmap_frame = draw_skin_heatmap(
            frame.copy(),
            regions,
            region_health,
            boxes
        )

        # ---------- TEXT ----------
        y_text = 30
        for key, value in report.items():
            cv2.putText(
                heatmap_frame,
                f"{key}: {value}",
                (20, y_text),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
            y_text += 25

        # YAW
        cv2.putText(
            heatmap_frame,
            f"Yaw: {int(yaw)}",
            (20, y_text + 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )

        # STATUS
        msg = "Captured ✅" if captured else "Live Analysis Running..."
        cv2.putText(
            heatmap_frame,
            msg,
            (20, y_text + 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        heatmap_frame = cv2.cvtColor(heatmap_frame, cv2.COLOR_BGR2RGB)

        report_text = "\n".join([f"{k}: {v}" for k, v in report.items()])

        return heatmap_frame, report_text, recommendation

    except Exception as e:
        import traceback
        traceback.print_exc()
        return frame, f"Error: {str(e)}", "Recommendation unavailable"


# ---------- UI ----------
with gr.Blocks(title="AI Dermatology Skin Analyzer") as demo:

    gr.Markdown("# 💆‍♀️ AI Dermatology Skin Analyzer")
    gr.Markdown("Live dermatology analysis with AI")

    with gr.Row():
        webcam = gr.Image(sources=["webcam"], type="numpy", streaming=True)
        output_video = gr.Image(label="Skin Heatmap Overlay")

    with gr.Row():
        sleep = gr.Number(label="Sleep Hours", value=7)
        water = gr.Number(label="Water Intake (Liters)", value=2)

        stress = gr.Dropdown(["low", "medium", "high"], value="medium")
        diet = gr.Dropdown(["balanced", "oily", "junk", "healthy"], value="balanced")
        skincare = gr.Dropdown(["yes", "no"], value="yes")

    with gr.Row():
        report_box = gr.Textbox(label="Skin Analysis Report")
        recommendation_box = gr.Textbox(label="AI Recommendation")

    webcam.stream(
        analyze_stream,
        inputs=[webcam, sleep, water, stress, diet, skincare],
        outputs=[output_video, report_box, recommendation_box]
    )

demo.launch()