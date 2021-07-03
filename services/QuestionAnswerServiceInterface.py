import abc
from typing import Optional, Text
from services.QuestionAnswerResult import QuestionAnswerResult


class QuestionAnswerServiceInterface(abc.ABC):
    @abc.abstractmethod
    def handle_question(
        self, question: Text
    ) -> Optional[QuestionAnswerResult]:
        pass
