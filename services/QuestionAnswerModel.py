import abc
from dataclasses import dataclass


@dataclass
class QuestionAnswerResponse:
    score: float
    start: int
    end: int


class QuestionAnswerModel(abc.ABC):
    @abc.abstractmethod
    def predict(self, question: str, context: str) -> QuestionAnswerResponse:
        pass


@dataclass
class QuestionAnswerResult:
    confidence: float
    answer: str
