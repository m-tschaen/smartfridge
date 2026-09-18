import httpx

from models import Recipe


THEMEALDB_URL = "https://www.themealdb.com/api/json/v1/1"


async def search_recipes_by_ingredient(ingredient: str):
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(
                f"{THEMEALDB_URL}/filter.php",
                params={"i": ingredient}
            )
            response.raise_for_status()
            data = response.json()

    except httpx.TimeoutException:
        return []

    except httpx.HTTPStatusError:
        return []

    return data.get("meals") or []


async def get_recipe_details(meal_id: str):
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(
                f"{THEMEALDB_URL}/lookup.php",
                params={"i": meal_id}
            )
            response.raise_for_status()
            data = response.json()

    except httpx.TimeoutException:
        return None

    except httpx.HTTPStatusError:
        return None

    meals = data.get("meals") or []

    if not meals:
        return None

    return Recipe.model_validate(meals[0])