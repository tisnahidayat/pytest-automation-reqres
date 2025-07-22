import requests as req
from dotenv import load_dotenv
import os

load_dotenv()

class APIClient:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL")
        self.api_key = os.getenv("API_KEY")

        if not self.base_url or not self.api_key:
            raise ValueError("BASE_URL/API_KEY is not set in the environment variables.")

    def _get_headers(self, use_auth=True):
        headers = {
            "Content-Type": "application/json"
        }
        if use_auth:
            headers["x-api-key"] =  self.api_key
        return headers

    def get(self, endpoint, params=None, use_auth=False):
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers(use_auth=use_auth) if use_auth else None
        response = req.get(url, params=params, headers=headers)
        return response

    def post(self, endpoint, data=None, use_auth=True):
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers(use_auth)
        response = req.post(url, json=data, headers=headers)
        return response

    def put(self, endpoint, data=None, use_auth=True):
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers(use_auth=use_auth)
        response = req.put(url, json=data, headers=headers)
        return response

    def delete(self, endpoint, use_auth=True):
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers(use_auth=use_auth)
        response = req.delete(url, headers=headers)
        return response
