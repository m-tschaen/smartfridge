import os
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv
import jwt
from supabase import create_client, Client

load_dotenv()

SECRET_KEY = "cle_secrete_du_frigo"
ALGORITHM = "HS256"

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def register_user(form_data: OAuth2PasswordRequestForm):
    existing_user = supabase.table("users").select("*").eq("username", form_data.username).execute()
    if existing_user.data:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user_data = {
        "username": form_data.username,
        "password": form_data.password,
    }
    supabase.table("users").insert(new_user_data).execute()

    return {"message": f"User {form_data.username} registered successfully"}


def login_user(form_data: OAuth2PasswordRequestForm):
    response = supabase.table("users").select("*").eq("username", form_data.username).execute()
    users_list = response.data

    if not users_list or users_list[0]["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect ids in the database")

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {"sub": form_data.username, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")