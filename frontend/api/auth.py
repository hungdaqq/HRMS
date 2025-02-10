import requests

API_BASE_URL = "http://localhost:8000"  # Replace with your actual API base URL


def login(username, password):
    """
    Authenticate user via the login API.
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/login",
            json={"username": username, "password": password},
        )
        if response.status_code == 200:
            return (
                True,
                response.json(),
            )
        return False, response.json().get("message", "Invalid username or password.")
    except Exception as e:
        return False, str(e)
