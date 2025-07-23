import pytest
from utils.api_client import APIClient

@pytest.fixture(scope="module")
def api():
    return APIClient()

def test_register_user(api):
    data = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }
    response = api.post("api/register", data=data, use_auth=True)

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json; charset=utf-8", f"Unexpected Content-Type header"

    jsonData = response.json()
    expected_value = jsonData
    assert isinstance(jsonData, dict), "Response JSON is not a dictionary"
    assert "id" in jsonData, "Response JSON does not contain 'id' field"
    assert "token" in jsonData, "Response JSON does not contain 'token' field"
    assert isinstance(jsonData["token"], str), "'token' should be a string"
    assert isinstance(jsonData["id"], int), "'id' should be an integer"
    assert expected_value["id"] == jsonData["id"], f"ID mismatch: expected {expected_value['id']}, got {jsonData['id']}"
    assert expected_value["token"] == jsonData["token"], f"Token mismatch: expected {expected_value['token']}, got {jsonData['token']}"

    assert response.elapsed.total_seconds() < 2, "Response took too long"

