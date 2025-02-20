import requests
import streamlit as st
import datetime

API_BASE_URL = "http://localhost:8000"  # Replace with your actual API base URL


def create_attendance(username, status):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/attendance",
            json={
                "employee": username,
                "date": str(datetime.datetime.now()),
                "status": status,
            },
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
        )
        if 200 <= response.status_code < 400:
            return True, response.json()
        return False, response.json().get("message", "Failed to create attendance.")
    except Exception as e:
        return False, str(e)


def get_attendance():
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/attendance",
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
        )
        if 200 <= response.status_code < 400:
            return True, response.json()
        return False, response.json().get("message", "Failed to retrieve attendance.")
    except Exception as e:
        return False, str(e)
