import pytest, json
from utils.api_client import APIClient
from utils.schema_loader import load_schema
from jsonschema import validate, ValidationError

@pytest.fixture(scope="module")
def api_client():
    return APIClient()

def get_users_with_param(api_client):
    response = api_client.get("api/users", params={"page": 2}, use_auth=True)
    
    # Cek status & headers
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"

    # Ambil data dan validasi schema
    jsonData = response.json()
    schema = load_schema("posts_schema.json")
    try:
        validate(instance=jsonData, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Schema validation error: {e}")

    # Validasi properti utama
    for key in ["page", "per_page", "total", "total_pages", "data"]:
        assert key in jsonData

    # Validasi isi data
    data_list = jsonData["data"]
    assert isinstance(data_list, list) and len(data_list) > 0

    required_fields = ["id", "email", "first_name", "last_name", "avatar"]
    for user in data_list:
        for field in required_fields:
            assert field in user
            assert isinstance(user[field], (str, int))
    
    actual_user = data_list[0]
    for key, expected_value in jsonData["data"][0].items():
        assert actual_user[key] == expected_value, f"{key} mismatch: expected {expected_value}, got {actual_user[key]}"

    assert response.elapsed.total_seconds() < 2, "Response took too long"