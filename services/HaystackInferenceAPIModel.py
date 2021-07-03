import json
from typing import Optional
import requests
from services.QuestionAnswerContextlessModel import (
    QuestionAnswerContextlessModel,
)
from services.QuestionAnswerResult import QuestionAnswerResult


class HaystackInferenceAPIModel(QuestionAnswerContextlessModel):
    API_URL = f"http://localhost:8000/query"
    PROBABILITY_THRESHOLD = 0.1

    def predict(self, question: str) -> Optional[QuestionAnswerResult]:
        result = self._query(
            {
                "query": question,
                "filters": {},
                "top_k_retriever": 1,
                "top_k_reader": 1,
            }
        )

        # error = result.get("error")

        answers = result.get("answers")

        if not answers:
            raise RuntimeError("No answers")
        else:
            answer = answers[0]

            if answer["probability"] > self.PROBABILITY_THRESHOLD:
                return QuestionAnswerResult(
                    confidence=answer["probability"], answer=answer["answer"]
                )
            else:
                return None

    def _query(self, payload):
        data = json.dumps(payload)
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        response = requests.post(self.API_URL, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))
