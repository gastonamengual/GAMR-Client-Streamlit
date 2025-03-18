from dataclasses import dataclass
from typing import Any

import requests  # type: ignore

from app.settings import Settings

from .error import PredictionNotObtained, TokenNotObtainedError


@dataclass
class API_Client:
    base_url: str
    token: str | None = ""

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def authenticate(self):
        try:
            response = requests.post(
                f"{self.base_url}/token", json={"username": Settings.USERNAME_API}
            )

            if not response.ok:
                raise TokenNotObtainedError(
                    f"ERROR {response.status_code} - Token not obtained: {response.json()}"
                )
            token = response.json().get("token")

            self.token = token

        except Exception as ex:
            raise TokenNotObtainedError(f"Token request failed: {ex}")

    def perform_post_request(self, json_content: dict[str, Any], path: str):
        try:
            response = requests.post(
                f"{self.base_url}/{path}",
                headers=self.headers,
                json=json_content,
            )
            return response
        except Exception as e:
            raise PredictionNotObtained(f"Post request failed: {e}")

    def perform_get_request(self, path: str):
        try:
            response = requests.get(
                f"{self.base_url}/{path}",
                headers=self.headers,
            )
            return response
        except Exception as e:
            raise PredictionNotObtained(f"Get request failed: {e}")
