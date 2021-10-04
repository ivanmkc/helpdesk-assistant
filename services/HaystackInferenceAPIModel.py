import json
from typing import List, Optional
import requests
from services.QuestionAnswerContextlessModel import (
    QuestionAnswerContextlessModel,
)
from services.QuestionAnswerResult import QuestionAnswerResult
import os

DEFAULT_TAGS = ["common_knowledge"]


class HaystackInferenceAPIModel(QuestionAnswerContextlessModel):
    PROBABILITY_THRESHOLD = 0.2

    def __init__(self) -> None:
        haystack_host = os.getenv("HAYSTACK_HOST")

        if haystack_host is None:
            raise ValueError(
                "No haystack host provided as HAYSTACK_HOST environment variable is not set"
            )

        self.api_url = f"{haystack_host}/query"

    def predict(
        self, question: str, tag: Optional[str] = None
    ) -> Optional[QuestionAnswerResult]:
        filters = {"tag": [tag] + DEFAULT_TAGS} if tag else {}
        result = self._query(
            {
                "query": question,
                "filters": filters,
                "top_k_retriever": 1,
                "top_k_reader": 1,
            }
        )

        answers = result.get("answers")

        if not answers:
            raise RuntimeError("No answers")
        else:
            answer = answers[0]
            if answer["probability"] > self.PROBABILITY_THRESHOLD:
                context = answer["context"]
                start_index = answer["offset_start"]

                # Build map of start and ends of each line
                newline_locations: List[int] = []
                period_locations: List[int] = []
                for index, character in enumerate(context):
                    if character == "\n":
                        newline_locations.append(index)
                        period_locations.append(index)
                    if character == ".":
                        period_locations.append(index)

                # Get entire sentence from start of current sentence to last newline or period.
                start_index_result = 0
                end_index_result = 0

                for location in period_locations:
                    if location <= start_index:
                        start_index_result = location + 1
                    else:
                        break

                newline_locations_after_start = [
                    index
                    for index in newline_locations
                    if index > start_index_result
                ]

                end_index_result = min(
                    newline_locations_after_start + [len(context)]
                )

                answer_substring = context[
                    start_index_result:end_index_result
                ].strip()
                answer_topic = answer["meta"]["name"]

                if answer_topic in answer_substring:
                    answer_complete = answer_substring
                else:
                    # TODO: Tailor response based on if a user is trying to find something or an attribute of something.
                    answer_complete = answer_substring

                # if not answer_complete.endswith("."):
                #     answer_complete += "."

                return QuestionAnswerResult(
                    confidence=answer["probability"],
                    answer=answer_complete.strip(),
                )
            else:
                return None

    def _query(self, payload):
        data = json.dumps(payload)
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        response = requests.post(self.api_url, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))
