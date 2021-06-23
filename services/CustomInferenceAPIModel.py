import json
import requests
from services.QuestionAnswerModel import (
    QuestionAnswerModel,
    QuestionAnswerResponse,
)


class CustomInferenceAPIModel(QuestionAnswerModel):
    API_URL = f"https://qa-xvtglwhs5q-uc.a.run.app/predict/qa/single"

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
        response = requests.request("POST", self.API_URL, data=data)
        return json.loads(response.content.decode("utf-8"))
