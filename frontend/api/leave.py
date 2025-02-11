import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000"  # Replace with your actual API base URL


def create_leave(date, reason):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/leave",
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
            json={"date": date, "reason": reason},
        )
        if 200 <= response.status_code < 400:
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


def get_new_leave():
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/leave?status=New",
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
        )
        if response.status_code == 200:
            return (
                True,
                response.json(),
            )
        return False, response.json().get("message", "Failed to get new leave.")
    except Exception as e:
        return False, str(e)


def update_leave_request(leave_id, status):
    try:
        response = requests.put(
            f"{API_BASE_URL}/api/leave/{leave_id}",
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
            json={"status": status},
        )
        if response.status_code == 200:
            return (
                True,
                response.json(),
            )
        return False, response.json().get("message", "Failed to approve leave.")
    except Exception as e:
        return False, str(e)
