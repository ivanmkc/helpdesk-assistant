import abc
from services.QuestionAnswerResult import QuestionAnswerResult
from typing import Optional


class QuestionAnswerContextlessModel(abc.ABC):
    @abc.abstractmethod
    def predict(
        self, question: str, tag: Optional[str]
    ) -> Optional[QuestionAnswerResult]:
        pass
