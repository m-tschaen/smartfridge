from enum import Enum
from pydantic import BaseModel, Field

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