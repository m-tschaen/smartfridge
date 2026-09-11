from models import UserProfile, Gender, ActivityLevel

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