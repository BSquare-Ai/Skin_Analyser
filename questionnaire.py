def get_lifestyle_answers():

    print("\nLifestyle Questionnaire")

    # Sleep
    while True:
        try:
            sleep = float(input("How many hours do you sleep daily? "))
            if 0 <= sleep <= 24:
                break
        except:
            pass
        print("Please enter a valid number between 0 and 24.")

    # Water intake
    while True:
        try:
            water = float(input("How many liters of water per day? "))
            if 0 <= water <= 10:
                break
        except:
            pass
        print("Please enter a valid number (e.g., 2 or 2.5).")

    # Stress
    valid_stress = ["low", "medium", "high"]
    while True:
        stress = input("Stress level (low / medium / high): ").strip().lower()
        if stress in valid_stress:
            break
        print("Please type: low, medium, or high.")

    # Diet
    valid_diet = ["balanced", "oily", "junk", "healthy"]
    while True:
        diet = input("Diet type (balanced / oily / junk / healthy): ").strip().lower()
        if diet in valid_diet:
            break
        print("Please type: balanced, oily, junk, or healthy.")

    # Skincare routine
    valid_skincare = ["yes", "no"]
    while True:
        skincare = input("Do you use skincare products regularly? (yes/no): ").strip().lower()
        if skincare in valid_skincare:
            break
        print("Please type yes or no.")

    lifestyle = {
        "sleep_hours": float(sleep),
        "water_intake_liters": float(water),
        "stress_level": stress,
        "diet_type": diet,
        "skincare_routine": skincare
    }

    return lifestyle