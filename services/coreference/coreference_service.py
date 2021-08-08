from typing import Optional
import json
import requests


class CoreferenceService:
    """
    CoreferenceService
    """

    API_URL = (
        "https://coref-xvtglwhs5q-uc.a.run.app/predict/coreference/single"
    )

    def resolve(self, text: str) -> Optional[str]:
        return self._query({"text": text}).get("text")

    def _query(self, payload):
        data = json.dumps(payload)

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        response = requests.post(self.API_URL, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))
