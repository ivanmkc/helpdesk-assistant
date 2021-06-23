from typing import Text, List
from services.CustomInferenceAPIModel import CustomInferenceAPIModel
from services.QuestionAnswerModel import (
    QuestionAnswerModel,
    QuestionAnswerResult,
)

CONFIDENCE_THRESHOLD = 0.3


class QuestionAnswerService:
    """
    QuestionAnswerService
    """

    def __init__(
        self,
        file_path: str,
        model: QuestionAnswerModel = CustomInferenceAPIModel(),
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
        result = self._model.predict(question=question, context=self._context)

        confidence = result.score

        if confidence > CONFIDENCE_THRESHOLD:
            start_index = result.start
            end_index = result.end
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
