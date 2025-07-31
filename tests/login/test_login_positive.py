import pytest
from utils.api_client import APIClient

@pytest.fixture(scope="module")
def api():
    return APIClient()

@pytest.mark.positive
def test_login_positive(api):
    data = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }
    response = api.post("api/login", data=data, use_auth=True)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json; charset=utf-8", f"Unexpected Content-Type header"

    jsonData = response.json()
    expected_value = jsonData.get("token")
    assert isinstance(jsonData, dict), "Response JSON is not a dictionary"
    assert "token" in jsonData, "Response JSON does not contain 'token' field"
    assert isinstance(jsonData["token"], str), "'token' should be a string"
    assert expected_value == jsonData["token"], f"Token mismatch: expected {expected_value}, got {jsonData['token']}"


    assert response.elapsed.total_seconds() < 2, "Response took too long"


