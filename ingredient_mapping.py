BRITISH_TO_AMERICAN = {
    "aubergine": "eggplant",
}


def to_american(ingredient_name: str) -> str:
    normalized = ingredient_name.strip().lower()
    return BRITISH_TO_AMERICAN.get(normalized, ingredient_name)