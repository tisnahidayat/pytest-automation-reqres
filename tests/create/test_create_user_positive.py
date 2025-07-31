import pytest
from utils.api_client import APIClient
from utils.schema_loader import load_schema
from jsonschema import validate, ValidationError
from utils.data_matches import assert_user_data_matches

@pytest.fixture(scope="module")
def api():
    return APIClient()

@pytest.mark.positive
def test_create_user_with_valid_data(api):
    data = {
        "name": "John Doe",
        "job": "Software Engineer"
    }
    response = api.post("api/users", data=data, use_auth=True)
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json; charset=utf-8", f"Unexpected Content-Type header"
    jsonData = response.json()
    
    schema = load_schema("user_creation_schema.json")
    try:
        validate(instance=jsonData, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Schema validation error: {e}")

    assert isinstance(jsonData, dict), "Response JSON is not a dictionary"
    for key in ["name", "job", "id", "createdAt"]:
        assert key in jsonData, f"Missing key: {key} in response data"
        assert isinstance(jsonData[key], str) or isinstance(jsonData[key], int), f"Expected '{key}' to be a string or integer, got {type(jsonData[key])}"

    assert_user_data_matches(jsonData, data)
    assert response.elapsed.total_seconds() < 2, "Response took too long"

@pytest.mark.positive
def test_create_user_with_different_data(api):
    data = {
        "name": "Alice",
        "job": "Designer"
    }

    response = api.post("api/users", data=data, use_auth=True)
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json; charset=utf-8", f"Unexpected Content-Type header"
    jsonData = response.json()
    
    schema = load_schema("user_creation_schema.json")
    try:
        validate(instance=jsonData, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Schema validation error: {e}")

    assert isinstance(jsonData, dict), "Response JSON is not a dictionary"
    for key in ["name", "job", "id", "createdAt"]:
        assert key in jsonData, f"Missing key: {key} in response data"
        assert isinstance(jsonData[key], str) or isinstance(jsonData[key], int), f"Expected '{key}' to be a string or integer, got {type(jsonData[key])}"

    assert_user_data_matches(jsonData, data)
    assert response.elapsed.total_seconds() < 2, "Response took too long"   


