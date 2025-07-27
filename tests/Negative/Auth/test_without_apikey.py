from utils.api_client import APIClient
from utils.schema_loader import load_schema
from jsonschema import validate, ValidationError
import pytest, json

@pytest.fixture(scope="module")
def api():
    return APIClient()

@pytest.mark.negative
def test_without_apikey(api):
    data = {
        "email": "eve.holt@reqres.in",
        "password": "city"
    }
    response = api.post("api/login", data=data, use_auth=False)
    assert response.status_code == 401, f"Expected status code 401, got {response.status_code}"

    schema = load_schema("error_schema.json")
    jsonData = response.json()
    try:
        validate(instance=jsonData, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Schema validation error: {e}")
    
    assert isinstance(jsonData, dict), "Response JSON is not a dictionary"
    assert "error" in jsonData, "Response JSON does not contain 'error' field"
    assert isinstance(jsonData["error"], str), "'error' should be a string"
    assert jsonData["error"] == "Missing API key.", f"Error message mismatch: expected 'Missing API key', got {jsonData['error']}"

    assert response.elapsed.total_seconds() < 2, "Response took too long"


