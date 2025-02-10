import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000"  # Replace with your actual API base URL


def create_leave(start_date, end_date, reason):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/leave",
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
            json={"start_date": start_date, "end_date": end_date, "reason": reason},
        )
        if response.status_code == 200:
            return (
                True,
                response.json(),
            )
        return False, response.json().get("message", "Failed to create leave.")
    except Exception as e:
        return False, str(e)


def get_leave():
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/leave",
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
        )
        if response.status_code == 200:
            return (
                True,
                response.json(),
            )
        return False, response.json().get("message", "Failed to get user leave.")
    except Exception as e:
        return False, str(e)
