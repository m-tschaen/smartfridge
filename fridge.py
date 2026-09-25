from auth import supabase


def add_ingredient(username: str, ingredient: str):
    normalized = ingredient.strip().lower()

    existing = supabase.table("fridge_items").select("*").eq("username", username).eq("ingredient", normalized).execute()

    if existing.data:
        return {"message": f"{ingredient} est deja dans votre frigo"}

    data = {
        "username": username,
        "ingredient": normalized,
    }
    supabase.table("fridge_items").insert(data).execute()
    return {"message": f"{ingredient} ajoute au frigo"}


def get_fridge_items(username: str):
    response = supabase.table("fridge_items").select("*").eq("username", username).execute()
    return response.data


def remove_ingredient(username: str, item_id: str):
    supabase.table("fridge_items").delete().eq("id", item_id).eq("username", username).execute()
    return {"message": "Ingredient supprime"}