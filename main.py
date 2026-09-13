from fastapi import FastAPI
from models import UserProfile
from metabolism import calculate_bmr, calculate_tdee, calculate_target_calories, calculate_macros

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Smart Fridge & Nutrition Coach"}

@app.post("/profile")
async def create_profile(profile: UserProfile):
    return profile

@app.post("/metabolism")
async def get_metabolism(profile: UserProfile):
    bmr = calculate_bmr(profile)
    tdee = calculate_tdee(profile)
    return {
        "bmr": round(bmr, 2),
        "tdee": round(tdee, 2),
    }

@app.post("/nutrition-plan")
async def get_nutrition_plan(profile: UserProfile):
    target_calories = calculate_target_calories(profile)
    macros = calculate_macros(profile)
    return {
        "target_calories": round(target_calories, 2),
        "macros": macros,
    }