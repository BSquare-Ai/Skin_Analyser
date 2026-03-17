def interpret_skin_conditions(report):

    conditions = {}

    health = report.get("Skin Health Score", 50)
    wrinkles = report.get("Wrinkle Score", 50)
    pigment = report.get("Pigmentation Score", 50)
    texture = report.get("Texture Score", 50)
    dark = report.get("Dark Circles Score", 50)


    # Skin type estimation
    if texture < 60:
        conditions["Skin Type"] = "Dry"
    elif texture > 75:
        conditions["Skin Type"] = "Oily"
    else:
        conditions["Skin Type"] = "Combination"


    # Hydration level
    if health < 60:
        conditions["Hydration Level"] = "Low"
    elif health < 80:
        conditions["Hydration Level"] = "Moderate"
    else:
        conditions["Hydration Level"] = "Good"


    # Wrinkle risk
    if wrinkles > 70:
        conditions["Wrinkle Risk"] = "High"
    elif wrinkles > 50:
        conditions["Wrinkle Risk"] = "Medium"
    else:
        conditions["Wrinkle Risk"] = "Low"


    # Pigmentation risk
    if pigment > 70:
        conditions["Pigmentation Risk"] = "High"
    elif pigment > 50:
        conditions["Pigmentation Risk"] = "Moderate"
    else:
        conditions["Pigmentation Risk"] = "Low"


    # Dark circle severity
    if dark > 70:
        conditions["Dark Circle Severity"] = "High"
    elif dark > 50:
        conditions["Dark Circle Severity"] = "Moderate"
    else:
        conditions["Dark Circle Severity"] = "Low"


    return conditions