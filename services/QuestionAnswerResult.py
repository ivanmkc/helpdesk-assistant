from dataclasses import dataclass


@dataclass
class QuestionAnswerResult:
    confidence: float
    answer: str
