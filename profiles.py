from auth import supabase 

def save_profile(username: str, profile_data: dict):
    existing = supabase.table("profiles").select("*").eq("username", username).execute()
    if existing.data:
        supabase.table("profiles").update(profile_data).eq("username",username).execute()
    else:
        profile_data["username"] = username
        supabase.table("profiles").insert(profile_data).execute()

def get_profile(username: str):
    response = supabase.table("profiles").select("*").eq("username", username).execute()
    profiles = response.data
    if not profiles:
        return None
    return profiles[0]