import asyncio

from meal_api import get_recipe_details, search_recipes_by_ingredient
from usda_api import search_food_nutrition
from ingredient_mapping import to_american


async def get_recipe_with_nutrition(meal_id: str):
    recipe = await get_recipe_details(meal_id)

    if recipe is None:
        return None

    tasks = [
        search_food_nutrition(to_american(item.ingredient))
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


async def get_suggestions_from_fridge(fridge_ingredients: list[str]):
    tasks = [search_recipes_by_ingredient(ing) for ing in fridge_ingredients]
    results_per_ingredient = await asyncio.gather(*tasks)

    recipe_matches = {}

    for ingredient, recipes in zip(fridge_ingredients, results_per_ingredient):
        for meal in recipes:
            meal_id = meal["idMeal"]

            if meal_id not in recipe_matches:
                recipe_matches[meal_id] = {
                    "idMeal": meal_id,
                    "strMeal": meal["strMeal"],
                    "strMealThumb": meal["strMealThumb"],
                    "matched_ingredients": [],
                }

            recipe_matches[meal_id]["matched_ingredients"].append(ingredient)

    suggestions = list(recipe_matches.values())
    suggestions.sort(key=lambda r: len(r["matched_ingredients"]), reverse=True)

    return suggestions