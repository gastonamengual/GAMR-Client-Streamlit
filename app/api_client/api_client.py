from dataclasses import dataclass
from typing import Any

import requests

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

    def authenticate(self) -> None:
        try:
            response = requests.post(
                f"{self.base_url}/token", json={"username": Settings.USERNAME_API}
            )

            if not response.ok:
                msg = f"ERROR {response.status_code} - Token not obtained: {response.json()}"  # noqa: E501
                raise TokenNotObtainedError(msg)
            token = response.json().get("token")

            self.token = token

        except requests.exceptions.RequestException as ex:
            msg = f"Token request failed: {ex}"
            raise TokenNotObtainedError(msg) from ex

    def perform_post_request(
        self, json_content: dict[str, Any], path: str
    ) -> requests.Response:
        try:
            return requests.post(
                f"{self.base_url}/{path}",
                headers=self.headers,
                json=json_content,
            )
        except requests.exceptions.RequestException as ex:
            msg = f"Post request failed: {ex}"
            raise PredictionNotObtained(msg) from ex

    def perform_get_request(self, path: str) -> requests.Response:
        try:
            return requests.get(
                f"{self.base_url}/{path}",
                headers=self.headers,
            )
        except Exception as ex:
            msg = f"Get request failed: {ex}"
            raise PredictionNotObtained(msg) from ex
