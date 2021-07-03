from typing import Text, List
from services.HaystackInferenceAPIModel import HaystackInferenceAPIModel
from services.QuestionAnswerServiceInterface import (
    QuestionAnswerServiceInterface,
)
from services.QuestionAnswerContextlessModel import (
    QuestionAnswerContextlessModel,
)
from services.QuestionAnswerResult import QuestionAnswerResult
from typing import Optional


class QuestionAnswerContextlessService(QuestionAnswerServiceInterface):
    """
    QuestionAnswerService
    """

    def __init__(
        self,
        model: QuestionAnswerContextlessModel = HaystackInferenceAPIModel(),
    ):
        self._model = model

    def handle_question(
        self, question: Text
    ) -> Optional[QuestionAnswerResult]:
        return self._model.predict(question=question)
