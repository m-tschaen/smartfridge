from enum import Enum
from pydantic import BaseModel, Field, model_validator


class Gender(str, Enum):
    male = "male"
    female = "female"


class ActivityLevel(str, Enum):
    sedentary = "sedentary"
    light = "light"
    moderate = "moderate"
    active = "active"
    very_active = "very_active"


class Goal(str, Enum):
    loss = "loss"
    maintain = "maintain"
    gain = "gain"


class UserProfile(BaseModel):
    weight_kg: float = Field(..., gt=0, le=200, description="Poids en kilogrammes")
    height_cm: float = Field(..., gt=0, le=250, description="Taille en centimetres")
    age: int = Field(..., gt=0, le=120, description="Age en annees")
    gender: Gender
    activity_level: ActivityLevel
    goal: Goal


class IngredientQuantity(BaseModel):
    ingredient: str
    measure: str


class Recipe(BaseModel):
    id: str
    name: str
    image: str | None = None
    ingredients: list[IngredientQuantity]

    @model_validator(mode="before")
    @classmethod
    def clean_meal_data(cls, data):
        ingredients = []

        for i in range(1, 21):
            ingredient = data.get(f"strIngredient{i}")
            measure = data.get(f"strMeasure{i}")

            if ingredient and ingredient.strip():
                ingredients.append({
                    "ingredient": ingredient.strip(),
                    "measure": (measure or "").strip()
                })

        return {
            "id": data.get("idMeal"),
            "name": data.get("strMeal"),
            "image": data.get("strMealThumb"),
            "ingredients": ingredients
        }