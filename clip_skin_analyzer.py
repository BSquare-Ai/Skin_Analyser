import torch
import clip
import cv2
import numpy as np
from PIL import Image


# --------------------------------------------------
# Device selection
# --------------------------------------------------

device = "cuda" if torch.cuda.is_available() else "cpu"


# --------------------------------------------------
# Load CLIP Model
# --------------------------------------------------

model, preprocess = clip.load("ViT-B/32", device=device)
model.eval()


# --------------------------------------------------
# Dermatology-aware prompts (UPDATED with ACNE)
# --------------------------------------------------

prompts = [
    "a close-up photo of clear healthy facial skin with smooth texture and even tone",
    "a close-up photo of facial skin showing wrinkles or aging lines",
    "a close-up photo of facial skin with dark circles under the eyes",
    "a close-up photo of facial skin with hyperpigmentation or dark spots",
    "a close-up photo of facial skin with rough uneven texture",
    "a close-up photo of facial skin with acne, pimples, or breakouts"
]


# Tokenize prompts
text_tokens = clip.tokenize(prompts).to(device)


# Encode text features once
with torch.no_grad():
    text_features = model.encode_text(text_tokens)
    text_features /= text_features.norm(dim=-1, keepdim=True)


# --------------------------------------------------
# MedGrad Severity Function
# --------------------------------------------------

def get_severity(score):
    if score < 0.3:
        return "Mild"
    elif score < 0.7:
        return "Moderate"
    else:
        return "Severe"


# --------------------------------------------------
# CLIP Skin Analyzer
# --------------------------------------------------

def analyze_skin_clip(face):

    if face is None or face.size == 0:
        return {}

    # ----------------------------------------
    # Lighting normalization (important)
    # ----------------------------------------

    lab = cv2.cvtColor(face, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)

    lab = cv2.merge((l, a, b))
    face = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # ----------------------------------------
    # Convert OpenCV → PIL
    # ----------------------------------------

    image = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)

    # ----------------------------------------
    # Preprocess image for CLIP
    # ----------------------------------------

    image_input = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():

        # Encode image
        image_features = model.encode_image(image_input)
        image_features /= image_features.norm(dim=-1, keepdim=True)

        # Cosine similarity
        similarity = (image_features @ text_features.T) * 100

        probs = similarity.softmax(dim=-1)

    scores = probs.cpu().numpy()[0]

    # --------------------------------------------------
    # Final Result with Severity (MedGrad)
    # --------------------------------------------------

    result = {
        "Healthy Skin": float(scores[0]),

        "Wrinkles_DL": float(scores[1]),
        "Wrinkles_Severity": get_severity(scores[1]),

        "Dark Circles_DL": float(scores[2]),
        "Dark Circles_Severity": get_severity(scores[2]),

        "Pigmentation_DL": float(scores[3]),
        "Pigmentation_Severity": get_severity(scores[3]),

        "Texture_DL": float(scores[4]),
        "Texture_Severity": get_severity(scores[4]),

        "Acne_DL": float(scores[5]),
        "Acne_Severity": get_severity(scores[5])
    }

    return result