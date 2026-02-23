import requests
import streamlit as st
from typing import Dict, Any, Optional, List
import json

class APIClient:
    """API client for backend communication"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if st.session_state.get("access_token"):
            headers["Authorization"] = f"Bearer {st.session_state.access_token}"
        
        return headers
    
    def _handle_response(self, response: requests.Response) -> Any:
        """Handle API response"""
        try:
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.HTTPError as e:
            st.error(f"HTTP Error: {e}")
            if response.status_code == 401:
                st.session_state.authenticated = False
                st.rerun()
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"Request Error: {e}")
            return None
        except json.JSONDecodeError as e:
            st.error(f"JSON Decode Error: {e}")
            return None
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        """GET request"""
        try:
            response = self.session.get(
                f"{self.base_url}{endpoint}",
                headers=self._get_headers(),
                params=params,
                timeout=10
            )
            return self._handle_response(response)
        except requests.exceptions.Timeout:
            st.error("Request timeout")
            return None
        except requests.exceptions.ConnectionError:
            st.error("Connection error - is the backend running?")
            return None
    
    def post(self, endpoint: str, data: Dict[str, Any] = None) -> Any:
        """POST request"""
        try:
            response = self.session.post(
                f"{self.base_url}{endpoint}",
                headers=self._get_headers(),
                json=data,
                timeout=10
            )
            return self._handle_response(response)
        except requests.exceptions.Timeout:
            st.error("Request timeout")
            return None
        except requests.exceptions.ConnectionError:
            st.error("Connection error - is the backend running?")
            return None
    
    def put(self, endpoint: str, data: Dict[str, Any] = None) -> Any:
        """PUT request"""
        try:
            response = self.session.put(
                f"{self.base_url}{endpoint}",
                headers=self._get_headers(),
                json=data,
                timeout=10
            )
            return self._handle_response(response)
        except requests.exceptions.Timeout:
            st.error("Request timeout")
            return None
        except requests.exceptions.ConnectionError:
            st.error("Connection error - is the backend running?")
            return None
    
    def delete(self, endpoint: str) -> bool:
        """DELETE request"""
        try:
            response = self.session.delete(
                f"{self.base_url}{endpoint}",
                headers=self._get_headers(),
                timeout=10
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            st.error(f"Delete Error: {e}")
            return False
    
    def upload_file(self, endpoint: str, file, additional_data: Optional[Dict] = None) -> Any:
        """Upload file with multipart/form-data"""
        try:
            files = {'file': (file.name, file, file.type)}
            data = additional_data or {}
            
            response = self.session.post(
                f"{self.base_url}{endpoint}",
                headers={"Authorization": self._get_headers().get("Authorization")},
                files=files,
                data=data,
                timeout=30
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            st.error(f"Upload Error: {e}")
            return None

# Initialize API client
def get_api_client():
    """Get API client instance"""
    return APIClient("http://localhost:8000/api")