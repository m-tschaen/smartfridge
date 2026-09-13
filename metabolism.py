from models import UserProfile, Gender, ActivityLevel, Goal

ACTIVITY_MULTIPLIERS = {
    ActivityLevel.sedentary: 1.2,
    ActivityLevel.light: 1.375,
    ActivityLevel.moderate: 1.55,
    ActivityLevel.active: 1.725,
    ActivityLevel.very_active: 1.9,
}

def calculate_bmr(profile: UserProfile) -> float:
    base = (10 * profile.weight_kg) + (6.25 * profile.height_cm) - (5 * profile.age)
    if profile.gender == Gender.male:
        return base + 5
    else:
        return base - 161


def calculate_tdee(profile: UserProfile) -> float:
    bmr = calculate_bmr(profile)
    multiplier = ACTIVITY_MULTIPLIERS[profile.activity_level]
    return bmr * multiplier

CALORIE_DELTA =  {
    Goal.loss: -500,
    Goal.maintain: 0, 
    Goal.gain: 300,
}

MACRO_PERCENTAGES = {
    "protein": 0.30,
    "fat": 0.30,
    "carbs": 0.40,
}

CALORIES_PER_GRAM = {
    "protein": 4,
    "fat": 9,
    "carbs": 4,
}


def calculate_target_calories(profile: UserProfile) -> float:
    tdee = calculate_tdee(profile)
    delta = CALORIE_DELTA[profile.goal]
    return tdee + delta


def calculate_macros(profile: UserProfile) -> dict:
    target_calories = calculate_target_calories(profile)
    macros = {}
    for macro_name, percentage in MACRO_PERCENTAGES.items():
        macro_calories = target_calories * percentage
        macro_grams = macro_calories / CALORIES_PER_GRAM[macro_name]
        macros[macro_name] = round(macro_grams, 1)
    return macros