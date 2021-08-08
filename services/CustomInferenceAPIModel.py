import json
import os
import requests
from services.QuestionAnswerModel import (
    QuestionAnswerModel,
    QuestionAnswerResponse,
)


class CustomInferenceAPIModel(QuestionAnswerModel):
    def __init__(self) -> None:
        qa_host = os.getenv("QA_HOST")

        if qa_host is None:
            raise ValueError(
                "No QA host provided as QA_HOST environment variable is not set"
            )

        self.api_url = f"{qa_host}/predict/qa/single"

    def predict(self, question: str, context: str) -> QuestionAnswerResponse:
        result = self._query(
            {
                "question": question,
                "context": context,
            }
        )

        error = result.get("error")

        if error:
            raise RuntimeError(error)
        else:
            return QuestionAnswerResponse(
                score=result["score"], start=result["start"], end=result["end"]
            )

    def _query(self, payload):
        data = json.dumps(payload)
        response = requests.request("POST", self.api_url, data=data)
        return json.loads(response.content.decode("utf-8"))
