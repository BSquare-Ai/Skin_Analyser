import os
import random
# ✅ Switched to the modern 2026 SDK
from google import genai

# Configure Gemini Client
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    # Initialize the new Client
    client = genai.Client(api_key=api_key)
    # Using the latest stable high-speed model
    MODEL_ID = "gemini-2.0-flash" 
else:
    client = None


# ---------------- RULE-BASED LOGIC ---------------- #
def rule_based_recommendation(report, conditions):
    recommendations = []

    # Safe extraction using .get() to prevent KeyErrors
    skin_type = conditions.get("Skin Type", "")
    pigmentation = conditions.get("Pigmentation Risk", "")
    wrinkles = conditions.get("Wrinkle Risk", "")
    dark = conditions.get("Dark Circle Severity", "")

    if pigmentation in ["High", "Moderate"]:
        recommendations.append("Use Vitamin C serum in the morning to reduce pigmentation.")

    if wrinkles in ["High", "Medium"]:
        recommendations.append("Use Retinol or peptide-based creams at night to improve wrinkles.")

    if skin_type == "Dry":
        recommendations.append("Use Hyaluronic acid moisturizer to improve hydration.")

    if dark in ["High", "Moderate"]:
        recommendations.append("Use caffeine-based eye creams for dark circles.")

    recommendations.append("Apply SPF 50 sunscreen daily.")

    return recommendations


# ---------------- LIFESTYLE LOGIC ---------------- #
def get_lifestyle_tip(lifestyle):
    tips = []

    sleep = lifestyle.get("sleep_hours", 0)
    water = lifestyle.get("water_intake_liters", 0)
    stress = lifestyle.get("stress_level", "")
    diet = lifestyle.get("diet_type", "")

    if water < 2:
        tips.append("Increase water intake to at least 2–3 liters daily for better hydration.")

    if sleep < 7:
        tips.append("Improve sleep quality to support skin repair and recovery.")

    if stress in ["high", "medium"]:
        tips.append("Reduce stress through relaxation techniques to improve skin health.")

    if diet != "balanced":
        tips.append("Maintain a balanced diet rich in antioxidants for healthier skin.")

    if not tips:
        tips.append("Maintain your current healthy lifestyle to keep your skin in good condition.")

    return random.choice(tips)


# ---------------- MAIN FUNCTION ---------------- #
def get_product_recommendations(report, lifestyle, conditions):
    # Step 1: Generate Base recommendations
    base_recommendations = rule_based_recommendation(report, conditions)

    # Step 2: Add lifestyle-aware tip
    lifestyle_tip = get_lifestyle_tip(lifestyle)
    base_recommendations.append(lifestyle_tip)

    # Step 3: Attempt LLM enhancement
    try:
        if client is None:
            raise Exception("Gemini API key not configured in environment variables.")

        prompt = f"""
        You are an expert AI dermatologist. Provide a high-end, personalized skincare plan.

        [PATIENT DATA]
        Skin Metrics: {report}
        Daily Lifestyle: {lifestyle}
        Clinical Conditions: {conditions}

        [CURRENT BASE ADVICE]
        {base_recommendations}

        [TASK]
        1. Refine and expand the base recommendations.
        2. Be highly specific about active ingredients (e.g., Niacinamide, Bakuchiol, Ceramides).
        3. Explain *why* these help based on the patient's metrics.
        4. Organize the routine into Morning and Evening steps.
        5. Tone: Professional, supportive, and clinical.
        """

        # Using the new 2026 generation syntax
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )

        return getattr(response, "text", str(response))

    except Exception as e:
        # Step 4: Fallback to local logic if API fails or is offline
        print(f"⚠️ LLM Error: {e}. Falling back to rule-based logic.")
        return "Personalized Recommendations\n" + "\n".join([f"- {rec}" for rec in base_recommendations])