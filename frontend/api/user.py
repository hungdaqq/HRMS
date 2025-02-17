import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000"  # Replace with your actual API base URL


def get_user_profile():
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/user/profile",
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
                response.json(),
            )
        return False, response.json().get("message", "Failed to get users.")
    except Exception as e:
        return False, str(e)


def register(username, email, password, salary, title, full_name, profile_image=None):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/register",
            json={
                "username": username,
                "email": email,
                "password": password,
                "salary": salary,
                "title": title,
                "full_name": full_name,
                "profile_image": profile_image,
            },
        )
        if 200 <= response.status_code < 400:
            return True, response.json()["data"]
        return False, response.json().get("message", "Failed to create user.")
    except Exception as e:
        return False, str(e)


def update_user_image(profile_image, user_id):
    try:
        response = requests.put(
            f"{API_BASE_URL}/api/user/{user_id}",
            json={
                "profile_image": profile_image,
            },
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
        )
        if 200 <= response.status_code < 400:
            return True, response.json()["data"]
        return False, response.json().get("message", "Failed to update user.")
    except Exception as e:
        return False, str(e)
