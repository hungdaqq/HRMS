import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000"  # Replace with your actual API base URL


def get_user_profile():
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/user/details",
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
        )
        if response.status_code == 200:
            return (
                True,
                response.json()["data"],
            )
        return False, response.json().get("message", "Failed to get user profile.")
    except Exception as e:
        return False, str(e)


def get_all_users():
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/user",
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
        )
        if response.status_code == 200:
            return (
                True,
                response.json()["data"],
            )
        return False, response.json().get("message", "Failed to get users.")
    except Exception as e:
        return False, str(e)
