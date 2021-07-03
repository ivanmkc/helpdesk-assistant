import json
import requests
import os
from services.QuestionAnswerModel import (
    QuestionAnswerModel,
    QuestionAnswerResponse,
)


class HuggingFaceInferenceAPIModel(QuestionAnswerModel):
    API_TOKEN = os.getenv("HUGGING_FACE_API_KEY")
    MODEL_NAME = "bert-large-uncased-whole-word-masking-finetuned-squad"
    # MODEL_NAME = "deepset/bert-large-uncased-whole-word-masking-squad2"
    API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

    def predict(self, question: str, context: str) -> QuestionAnswerResponse:
        result = self._query(
            {"inputs": {"question": question, "context": context,}}
        )

        error = result.get("error")

        if error:
            raise RuntimeError(error)
        else:
            return QuestionAnswerResponse(
                score=result["score"], start=result["start"], end=result["end"]
            )

    def _query(self, payload):
        headers = {"Authorization": f"Bearer {self.API_TOKEN}"}
        data = json.dumps(payload)
        response = requests.request(
            "POST", self.API_URL, headers=headers, data=data
        )
        return json.loads(response.content.decode("utf-8"))
