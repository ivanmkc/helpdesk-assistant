from enum import Enum, unique

# from transformers import pipeline
from typing import Text, Dict, List, Any, Optional
import json
import requests
import abc
import os

CONFIDENCE_THRESHOLD = 0.3


class QuestionAnswerModel(abc.ABC):
    @abc.abstractmethod
    def predict(self, question: str, context: str) -> Dict:
        pass


class HuggingFaceInferenceAPIModel(QuestionAnswerModel):
    API_TOKEN = os.getenv("HUGGING_FACE_API_KEY")
    MODEL_NAME = "deepset/minilm-uncased-squad2"
    # MODEL_NAME = "deepset/bert-large-uncased-whole-word-masking-squad2"
    API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

    def predict(self, question: str, context: str) -> Dict:
        result = self._query(
            {
                "inputs": {
                    "question": question,
                    "context": context,
                }
            }
        )

        error = result.get("error")

        if error:
            raise RuntimeError(error)
        else:
            return result

    def _query(self, payload):
        headers = {"Authorization": f"Bearer {self.API_TOKEN}"}
        data = json.dumps(payload)
        response = requests.request(
            "POST", self.API_URL, headers=headers, data=data
        )
        return json.loads(response.content.decode("utf-8"))


# class TransformersModel(QuestionAnswerModel):
#     def __init__(self):
#         self._pipeline = pipeline(
#             "question-answering",
#             model="deepset/minilm-uncased-squad2",
#         )

#     def predict(self, question: str, context: str) -> Dict:
#         return self._pipeline(question=question, context=context)


class QuestionAnswerResult:
    confidence: float
    answer: str

    def __init__(self, confidence: float, answer: str):
        self.confidence = confidence
        self.answer = answer


class QuestionAnswerService:
    """
    QuestionAnswerService
    """

    def __init__(
        self,
        file_path: str,
        model: QuestionAnswerModel = HuggingFaceInferenceAPIModel(),
    ):

        self._context = self._read_file(file_path)
        self._model = model

        # Build map of start and ends of each line
        self._newline_locations: List[int] = []
        self._period_locations: List[int] = []
        for index, character in enumerate(self._context):
            if character == "\n":
                self._newline_locations.append(index)
                self._period_locations.append(index)
            if character == ".":
                self._period_locations.append(index)

        # Add one for the end
        self._newline_locations.append(len(self._context))

    def handle_question(self, question: Text) -> QuestionAnswerResult:
        return QuestionAnswerResult(confidence=0.8, answer="placeholder")
        result = self._model.predict(question=question, context=self._context)

        confidence = result["score"]

        if confidence > CONFIDENCE_THRESHOLD:
            start_index = result["start"]
            end_index = result["end"]
            # answer = result["answer"]

            # Get entire sentence from start of current sentence to next newline
            start_index_result = 0
            end_index_result = 0

            for location in self._period_locations:
                if location <= start_index:
                    start_index_result = location + 1
                else:
                    break

            for location in self._newline_locations:
                if location >= end_index:
                    end_index_result = location
                    break

            return QuestionAnswerResult(
                confidence=confidence,
                answer=self._context[
                    start_index_result:end_index_result
                ].strip(),
            )

        else:
            return None

    def _read_file(self, file_path: str) -> Text:
        # Open a file: file
        file = open(file_path, mode="r")

        # read all lines at once
        contents = file.read()

        # close the file
        file.close()

        return contents
