from typing import Optional
import json
import os
import requests


class CoreferenceService:
    """
    CoreferenceService
    """

    def __init__(self) -> None:
        host = os.getenv("COREFERENCE_HOST")

        if host is None:
            raise ValueError(
                "No coreference host provided as QA_HOST environment variable is not set"
            )

        self.api_url = f"{host}/predict/coreference/single"

    def resolve(self, text: str) -> Optional[str]:
        return self._query({"text": text}).get("text")

    def _query(self, payload):
        data = json.dumps(payload)

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        response = requests.post(self.api_url, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))
