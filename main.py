from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from profiles import save_profile, get_profile
from fastapi.templating import Jinja2Templates
from fastapi import Request
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
from auth import register_user, login_user, get_current_user
from fridge import add_ingredient, get_fridge_items, remove_ingredient
from pipeline import get_recipe_with_nutrition, get_suggestions_from_fridge
from fridge import add_ingredient, get_fridge_items, remove_ingredient

load_dotenv()

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Smart Fridge & Nutrition Coach"}

@app.get("/test")
async def test_page(request: Request):
    return templates.TemplateResponse(request, "test.html", {})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {})

@app.get("/homepage")
async def homepage_page(request: Request):
    return templates.TemplateResponse(request, "homepage.html", {})

@app.post("/signup")
def signup(form_data: OAuth2PasswordRequestForm = Depends()):
    return register_user(form_data)

@app.post("/token")
def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return login_user(form_data)

@app.post("/profile")
async def create_profile(profile: UserProfile, current_user: str = Depends(get_current_user)):
    save_profile(current_user, profile.model_dump())
    return profile

@app.get("/profile")
async def read_profile(current_user: str = Depends(get_current_user)):
    profile = get_profile(current_user)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found ")
    return profile 

@app.post("/fridge")
async def add_to_fridge(ingredient: str, current_user: str = Depends(get_current_user)):
    return add_ingredient(current_user, ingredient)


@app.get("/fridge")
async def read_fridge(current_user: str = Depends(get_current_user)):
    return get_fridge_items(current_user)


@app.delete("/fridge/{item_id}")
async def delete_from_fridge(item_id: str, current_user: str = Depends(get_current_user)):
    return remove_ingredient(current_user, item_id)

@app.post("/metabolism")
async def get_metabolism(profile: UserProfile, current_user: str = Depends(get_current_user)):
    bmr = calculate_bmr(profile)
    tdee = calculate_tdee(profile)

    return {
        "bmr": round(bmr, 2),
        "tdee": round(tdee, 2),
    }


@app.post("/nutrition-plan")
async def get_nutrition_plan(profile: UserProfile, current_user: str = Depends(get_current_user)):
    target_calories = calculate_target_calories(profile)
    macros = calculate_macros(profile)

    return {
        "target_calories": round(target_calories, 2),
        "macros": macros,
    }


@app.get("/recipes")
async def get_recipes(ingredient: str, current_user: str = Depends(get_current_user)):
    recipes = await search_recipes_by_ingredient(ingredient)

    return {
        "ingredient": ingredient,
        "recipes": recipes,
    }


@app.get("/recipes/{meal_id}")
async def get_recipe(meal_id: str, current_user: str = Depends(get_current_user)):
    recipe = await get_recipe_details(meal_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return recipe


@app.get("/nutrition/{food_name}")
async def get_food_nutrition(food_name: str, current_user: str = Depends(get_current_user)):
    food = await search_food_nutrition(food_name)

    if food is None:
        raise HTTPException(
            status_code=404,
            detail="Food not found"
        )

    return food


@app.get("/recipes/{meal_id}/nutrition")
async def get_recipe_nutrition(meal_id: str, current_user: str = Depends(get_current_user)):
    recipe = await get_recipe_with_nutrition(meal_id)

    if recipe is None:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )

    return recipe

@app.get("/suggestions")
async def get_suggestions(current_user: str = Depends(get_current_user)):
    fridge_items = get_fridge_items(current_user)
    ingredients = [item["ingredient"] for item in fridge_items]

    if not ingredients:
        return {"suggestions": []}

    suggestions = await get_suggestions_from_fridge(ingredients)
    return {"suggestions": suggestions}
