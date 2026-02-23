import requests
from typing import Tuple, Dict, Any

def login_user(username: str, password: str, api_base_url: str) -> Tuple[bool, Any]:
    """Authenticate user"""
    try:
        response = requests.post(
            f"{api_base_url}/auth/token",
            data={
                "username": username,
                "password": password
            },
            timeout=10
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Invalid credentials")
    
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to server"
    except requests.exceptions.Timeout:
        return False, "Connection timeout"
    except Exception as e:
        return False, str(e)

def register_user(user_data: Dict[str, Any], api_base_url: str) -> Tuple[bool, Any]:
    """Register new user"""
    try:
        response = requests.post(
            f"{api_base_url}/auth/register",
            json=user_data,
            timeout=10
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Registration failed")
    
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to server"
    except requests.exceptions.Timeout:
        return False, "Connection timeout"
    except Exception as e:
        return False, str(e)

def logout_user():
    """Logout user"""
    # Clear session state
    import streamlit as st
    for key in ['authenticated', 'user', 'access_token']:
        if key in st.session_state:
            del st.session_state[key]

def refresh_token(api_base_url: str, refresh_token: str) -> Tuple[bool, Any]:
    """Refresh access token"""
    try:
        response = requests.post(
            f"{api_base_url}/auth/refresh",
            json={"refresh_token": refresh_token},
            timeout=10
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, None
    
    except:
        return False, None

def verify_token(token: str, api_base_url: str) -> bool:
    """Verify if token is valid"""
    try:
        response = requests.get(
            f"{api_base_url}/auth/verify",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        return response.status_code == 200
    except:
        return False