import pytest, json
from utils.schema_loader import load_schema
from utils.api_client import APIClient
from utils.data_matches import assert_user_data_matches
from jsonschema import validate, ValidationError
@pytest.fixture(scope="module")
def api_client():
    return APIClient()

def test_get_user_by_id(api_client):
    
    response = api_client.get(f"api/users/1")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"

    jsonData = response.json()

    schema = load_schema("user_data_schema.json")
    try:
        validate(instance=jsonData, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Schema validation error: {e}")

    for key in ["data", "support"]:
        assert key in jsonData, f"Missing key: {key} in response data"
        assert isinstance(jsonData["data"], dict), f"Expected 'data' to be a dict, got {type(jsonData['data'])}"
        assert isinstance(jsonData["support"], dict), f"Expected 'support' to be a dict, got {type(jsonData['support'])}"

    actual_user = jsonData["data"]
    expected_data = jsonData["data"]
    
    assert_user_data_matches(actual_user, expected_data)

    assert response.elapsed.total_seconds() < 2, "Response took too long"
    
    
    
