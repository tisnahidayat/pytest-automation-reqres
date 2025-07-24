import pytest
from utils.api_client import APIClient

@pytest.fixture(scope="module")
def api():
    return APIClient()

@pytest.mark.positive
def test_delete_user(api):
    response = api.delete(f"api/users/2", use_auth=True)
    assert response.status_code == 204, f"Expected status code 204, got {response.status_code}"
    assert response.elapsed.total_seconds() < 2, "Response took too long"
