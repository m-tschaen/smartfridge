from fastapi import FastAPI
from models import UserProfile
from metabolism import calculate_bmr, calculate_tdee

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Smart Fridge & Nutrition Coach"}

@app.get("/profile")
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