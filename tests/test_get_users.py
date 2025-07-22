import pytest
from utils.api_client import APIClient

@pytest.fixture(scope="module")
def api_client():
    return APIClient()

def test_get_users(api_client):
    response = api_client.get("api/users", params={"page": 1}, use_auth=False)
    assert response.status_code == 200

