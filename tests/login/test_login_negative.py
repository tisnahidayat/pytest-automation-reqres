from utils.api_client import APIClient
from utils.schema_loader import load_schema
from jsonschema import validate, ValidationError
import pytest

@pytest.fixture(scope="module")
def api():
    return APIClient()

@pytest.mark.negative
def test_with_empty_data(api):
    data = {
        "email": "",
        "password": ""
    }
    response = api.post("api/login", data=data, use_auth=True)
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"

    jsonData = response.json()
    schema = load_schema("error_schema.json")
    try:
        validate(instance=jsonData, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Schema validation error: {e}")

    assert isinstance(jsonData, dict), "Response JSON is not a dictionary"
    assert "error" in jsonData, "Response JSON does not contain 'error' field"
    assert isinstance(jsonData["error"], str), "'error' should be a string"
    assert jsonData["error"] == "Missing email or username", f"Error message mismatch: expected 'Missing email or password', got {jsonData['error']}"

    assert response.elapsed.total_seconds() < 2, "Response took too long"

@pytest.mark.negative
def test_with_empty_email(api):
    data = {
        "email": "",
        "password": "cityslicka"
    }
    response = api.post("api/login", data=data, use_auth=True)
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"

    schema = load_schema("error_schema.json")
    jsonData = response.json()
    try:
        validate(instance=jsonData, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Schema validation error: {e}")

    assert isinstance(jsonData, dict), "Response JSON is not a dictionary"
    assert "error" in jsonData, "Response JSON does not contain 'error' field"
    assert isinstance(jsonData["error"], str), "'error' should be a string"
    assert jsonData["error"] == "Missing email or username", f"Error message mismatch: expected 'Missing email or password', got {jsonData['error']}"

    assert response.elapsed.total_seconds() < 2, "Response took too long"

@pytest.mark.negative
def test_with_empty_password(api):
    data = {
        "email": "eve.holt@reqres.in",
        "password": ""
    }
    response = api.post("api/login", data=data, use_auth=True)
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"

    schema = load_schema("user_creation_schema.json")
    jsonData = response.json()
    try:
        validate(instance=jsonData, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Schema validation error: {e}")

    assert isinstance(jsonData, dict), "Response JSON is not a dictionary"
    assert "error" in jsonData, "Response JSON does not contain 'error' field"
    assert isinstance(jsonData["error"], str), "'error' should be a string"
    assert jsonData["error"] == "Missing password", f"Error message mismatch: expected 'Missing email or password', got {jsonData['error']}"

    assert response.elapsed.total_seconds() < 2, "Response took too long"

@pytest.mark.negative
def test_with_invalid_email(api):
    data = {
        "email": "invalid_email",
        "password": "cityslicka"
    }
    
    response = api.post("api/login", data=data, use_auth=True)
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"

    schema = load_schema("error_schema.json")
    jsonData = response.json()
    try:
        validate(instance=jsonData, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Schema validation error: {e}")

    assert isinstance(jsonData, dict), "Response JSON is not a dictionary"
    assert "error" in jsonData, "Response JSON does not contain 'error' field"
    assert isinstance(jsonData["error"], str), "'error' should be a string"
    assert jsonData["error"] == "user not found", f"Error message mismatch: expected 'Missing email or password', got {jsonData['error']}"

    assert response.elapsed.total_seconds() < 2, "Response took too long"

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
    assert jsonData["error"] == "Missing API key", f"Error message mismatch: expected 'Missing API key', got {jsonData['error']}"

    assert response.elapsed.total_seconds() < 2, "Response took too long"

