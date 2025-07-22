import pytest, random
from utils.api_client import APIClient
@pytest.fixture(scope="module")
def api_client():
    return APIClient()

def test_get_user(api_client):
    response = api_client.get(f"api/users/{random.randint(1, 12)}", use_auth=True)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["id"] == response.json()["data"]["id"]
    assert "email" in data["data"]
    assert "first_name" in data["data"]
    assert "last_name" in data["data"]
    assert data["data"]["first_name"] == response.json()["data"]["first_name"]
    assert data["data"]["last_name"] == response.json()["data"]["last_name"]
