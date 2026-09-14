from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from models import UserProfile
from metabolism import (
    calculate_bmr,
    calculate_tdee,
    calculate_target_calories,
    calculate_macros,
)
from meal_api import (
    search_recipes_by_ingredient,
    get_recipe_details,
)
from usda_api import search_food_nutrition
from pipeline import get_recipe_with_nutrition


load_dotenv()

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


@app.get("/recipes")
async def get_recipes(ingredient: str):
    recipes = await search_recipes_by_ingredient(ingredient)

    return {
        "ingredient": ingredient,
        "recipes": recipes,
    }


@app.get("/recipes/{meal_id}")
async def get_recipe(meal_id: str):
    recipe = await get_recipe_details(meal_id)

    if recipe is None:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )

    return recipe


@app.get("/nutrition/{food_name}")
async def get_food_nutrition(food_name: str):
    food = await search_food_nutrition(food_name)

    if food is None:
        raise HTTPException(
            status_code=404,
            detail="Food not found"
        )

    return food


@app.get("/recipes/{meal_id}/nutrition")
async def get_recipe_nutrition(meal_id: str):
    recipe = await get_recipe_with_nutrition(meal_id)

    if recipe is None:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )

    return recipe