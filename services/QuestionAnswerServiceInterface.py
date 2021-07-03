import abc
from typing import Optional
from services.QuestionAnswerResult import QuestionAnswerResult


class QuestionAnswerServiceInterface(abc.ABC):
    @abc.abstractmethod
    def handle_question(self, question: str) -> Optional[QuestionAnswerResult]:
        pass
