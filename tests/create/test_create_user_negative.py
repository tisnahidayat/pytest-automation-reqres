import pytest
from utils.api_client import APIClient
from utils.schema_loader import load_schema
from jsonschema import validate, ValidationError

@pytest.fixture(scope="module")
def api() :
    return APIClient()

@pytest.mark.negative
def test_create_user_only_name(api):
    data = {
        "name": "",
        "job": ""
    }

    response = api.post("api/users", data=data, use_auth=True)
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"

    jsonData = response.json()
    schema = load_schema("error_schema.json")
    try:
        validate(instance=jsonData, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Schema validation error: {e}")

    assert isinstance(jsonData, dict), "Response JSON is not a dictionary"
    assert "error" in jsonData, "Response JSON does not contain 'error' field"
    assert isinstance(jsonData["error"], str), "'error' should be a string"
    assert jsonData["error"] == "Missing email or password", f"Error message mismatch: expected 'Missing email or password', got {jsonData['error']}"

    assert response.elapsed.total_seconds() < 2, "Response took too long"