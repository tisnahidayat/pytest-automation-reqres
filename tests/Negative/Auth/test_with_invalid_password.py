from utils.api_client import APIClient
from utils.schema_loader import load_schema
from jsonschema import validate, ValidationError
import pytest, json

@pytest.fixture(scope="module")
def api():
    return APIClient()

@pytest.mark.negative
def test_with_invalid_password(api):
    data = {
        "email": "eve.holt@reqres.in",
        "password": "city"
    }
    
    response = api.post("api/login", data=data, use_auth=True)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    jsonData = response.json()
    expected_value = jsonData.get("token")
    assert isinstance(jsonData, dict), "Response JSON is not a dictionary"
    assert "token" in jsonData, "Response JSON does not contain 'token' field"
    assert isinstance(jsonData["token"], str), "'token' should be a string"
    assert expected_value == jsonData["token"], f"Token mismatch: expected {expected_value}, got {jsonData['token']}"

    assert response.elapsed.total_seconds() < 2, "Response took too long"


