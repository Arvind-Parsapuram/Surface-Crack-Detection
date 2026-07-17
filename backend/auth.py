import os
from typing import Any
import bcrypt

from backend.database import get_supabase, get_service_client

from dotenv import load_dotenv

load_dotenv()


def register_user(username: str, password: str, full_name: str) -> dict:
    supabase = get_service_client()
    try:
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        result = supabase.table("users").insert({
            "username": username,
            "password_hash": password_hash,
            "full_name": full_name,
        }).execute()
        user = result.data[0]
        return {
            "success": True,
            "message": "Registration successful. You can now log in.",
            "access_token": None,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "full_name": user["full_name"],
            },
        }
    except Exception as e:
        msg = str(e)
        if "duplicate key" in msg.lower() or "already exists" in msg.lower():
            return {"success": False, "message": "Username already taken."}
        return {"success": False, "message": f"Registration failed: {msg}"}


def login_user(username: str, password: str) -> dict:
    supabase = get_service_client()
    try:
        result = supabase.table("users").select("*").eq("username", username).execute()
        if not result.data:
            return {"success": False, "message": "Invalid username or password"}
        user = result.data[0]
        if user.get("password_hash") is None:
            return {"success": False, "message": "Invalid username or password"}
        if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            return {"success": False, "message": "Invalid username or password"}
        return {
            "success": True,
            "message": "Login successful",
            "access_token": None,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "full_name": user["full_name"],
            },
        }
    except Exception as e:
        return {"success": False, "message": "Invalid username or password"}



