def interpret_skin_results(results):

    texture = results["texture_score"]
    wrinkles = results["wrinkle_score"]
    pigment = results["pigmentation_score"]
    health = results["skin_health_score"]

    # ---- Normalize raw metrics into 0–100 scores ----
    # Lower multipliers to avoid saturation

    wrinkle_score = min(100, wrinkles * 8)
    pigment_score = min(100, pigment * 2)
    texture_score = min(100, texture / 8)

    # ---- Wrinkle level ----
    if wrinkle_score < 30:
        wrinkle_level = "Low"
    elif wrinkle_score < 60:
        wrinkle_level = "Moderate"
    else:
        wrinkle_level = "High"

    # ---- Pigmentation level ----
    if pigment_score < 30:
        pigment_level = "Low"
    elif pigment_score < 60:
        pigment_level = "Moderate"
    else:
        pigment_level = "High"

    # ---- Texture level ----
    if texture_score < 30:
        texture_level = "Smooth"
    elif texture_score < 60:
        texture_level = "Normal"
    else:
        texture_level = "Rough"

    # ---- Final report ----
    report = {

        "Skin Health Score": round(health, 2),

        "Wrinkle Score": round(wrinkle_score, 2),
        "Wrinkles": wrinkle_level,

        "Pigmentation Score": round(pigment_score, 2),
        "Pigmentation": pigment_level,

        "Texture Score": round(texture_score, 2),
        "Texture": texture_level
    }

    return report