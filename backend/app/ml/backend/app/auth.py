from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter(tags=["Authentication"])  # Removed prefix here

# Mock users
USERS: Dict[str, Dict[str, Any]] = {
    "demo_user": {
        "password": "password",
        "role": "user",
        "id": 1,
        "email": "demo@example.com"
    },
    "admin": {
        "password": "admin",
        "role": "admin",
        "id": 2,
        "email": "admin@example.com"
    }
}

@router.post("/auth/demo-login")  # Added /auth back here
async def demo_login(data: dict):
    """Simple login endpoint"""
    username = data.get("username", "")
    password = data.get("password", "")
    
    # Check credentials
    if username in USERS and USERS[username]["password"] == password:
        user = USERS[username]
        return {
            "success": True,
            "username": username,
            "role": user["role"],
            "user_id": user["id"],
            "email": user["email"],
            "message": "Login successful"
        }
    
    # For demo, accept demo_user/password
    if username == "demo_user" and password == "password":
        return {
            "success": True,
            "username": "demo_user",
            "role": "user",
            "user_id": 1,
            "email": "demo@example.com",
            "message": "Login successful"
        }
    
    # For demo, accept admin/admin
    if username == "admin" and password == "admin":
        return {
            "success": True,
            "username": "admin",
            "role": "admin",
            "user_id": 2,
            "email": "admin@example.com",
            "message": "Login successful"
        }
    
    # If all else fails
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/auth/login")
async def login(data: dict):
    """Alias for demo-login"""
    return await demo_login(data)

@router.get("/auth/test")
async def test_auth():
    """Test endpoint"""
    return {"message": "Auth is working", "status": "ok"}
