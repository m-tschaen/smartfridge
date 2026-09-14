import asyncio

from meal_api import get_recipe_details
from usda_api import search_food_nutrition


async def get_recipe_with_nutrition(meal_id: str):
    recipe = await get_recipe_details(meal_id)

    if recipe is None:
        return None

    tasks = [
        search_food_nutrition(item.ingredient)
        for item in recipe.ingredients
    ]

    nutrition_results = await asyncio.gather(*tasks)

    ingredients = []

    for ingredient, nutrition in zip(recipe.ingredients, nutrition_results):
        ingredients.append({
            "ingredient": ingredient.ingredient,
            "measure": ingredient.measure,
            "nutrition": nutrition
        })

    return {
        "id": recipe.id,
        "name": recipe.name,
        "image": recipe.image,
        "ingredients": ingredients
    }