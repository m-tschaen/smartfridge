import os
import httpx

USDA_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"


async def search_food_nutrition(food_name: str):
    api_key = os.getenv("USDA_API_KEY")

    params = {
        "api_key": api_key
    }

    body = {
        "query": food_name,
        "dataType": ["SR Legacy", "Foundation"],
        "pageSize": 1
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(
            USDA_URL,
            params=params,
            json=body
        )

        response.raise_for_status()

        data = response.json()
        foods = data.get("foods") or []

        if not foods:
            return None

        food = foods[0]
        nutrients = food.get("foodNutrients", [])

        nutrition = {
            "food": food_name,
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0
        }

        for nutrient in nutrients:
            nutrient_id = nutrient.get("nutrientId")

            if nutrient_id == 1008:
                nutrition["calories"] = nutrient.get("value", 0)

            elif nutrient_id == 1003:
                nutrition["protein"] = nutrient.get("value", 0)

            elif nutrient_id == 1005:
                nutrition["carbs"] = nutrient.get("value", 0)

            elif nutrient_id == 1004:
                nutrition["fat"] = nutrient.get("value", 0)

        return nutrition