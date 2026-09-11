from fastapi import FastAPI
from models import UserProfile

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Smart Fridge & Nutrition Coach"}

@app.get("/profile")
async def create_profile(profile: UserProfile):
    return profile