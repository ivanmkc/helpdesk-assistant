import typing
from typing import Text, Dict, Optional, List, Any
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher, Action

if typing.TYPE_CHECKING:  # pragma: no cover
    from rasa_sdk.types import DomainDict

from services.QuestionAnswerServiceInterface import (
    QuestionAnswerServiceInterface,
)
from services.question_answer_contextless_service import (
    QuestionAnswerContextlessService,
)
from services.coreference.coreference_service import CoreferenceService
from services.HaystackInferenceAPIModel import HaystackInferenceAPIModel
from rasa.shared.core.constants import ACTION_LISTEN_NAME
from rasa_sdk.events import FollowupAction
import logging

logger = logging.getLogger(__name__)
vers = "vers: 0.1.0, date: May 18, 2021"
logger.debug(vers)


ACTION_NAME = "question_answer_action"
SHOULD_USE_COREFERENCE = False

# tag = os.getenv("CHATBOT_ID")
TAG = "visitor_center"


class QuestionAnswerAction(Action):
    """
    Action that uses question answer extraction to get the relevant sentence
    """

    _question_service: QuestionAnswerServiceInterface

    def __init__(self) -> None:
        self._coreference_service = CoreferenceService()
        self._question_service = QuestionAnswerContextlessService(
            model=HaystackInferenceAPIModel(), tag=TAG
        )

    def name(self) -> Text:
        return ACTION_NAME

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        """
        Executes this action.

        Args:
            dispatcher: the dispatcher
            tracker: the tracker
            domain: the domain

        Returns: list of slots

        """

        question = tracker.latest_message["text"]

        # Check if subject is present
        if SHOULD_USE_COREFERENCE:
            pronouns = ["it", "this", "that", "there"]
            if any([pronoun in question for pronoun in pronouns]):
                last_bot_utterance = self.get_last_bot_utterance(tracker)
                question = self._coreference_service.resolve(
                    last_bot_utterance + " " + question
                )

                # Remove the last_bot_utterance
                if question.startswith(last_bot_utterance):
                    question = question[len(last_bot_utterance) :]

        return await self._ask_question(
            dispatcher=dispatcher,
            question=question,
            tracker=tracker,
        )

    def get_last_bot_utterance(self, tracker) -> Optional[str]:
        utterance: Optional[str] = None

        for event in reversed(tracker.events):
            event_type = event["event"]
            if event_type == "bot":
                utterance = event["text"]
                break

        if utterance is not None:
            if utterance[-1].isalpha():
                utterance = utterance + "."

        return utterance

    async def _ask_question(
        self,
        dispatcher: CollectingDispatcher,
        question: Text,
        tracker: Tracker,
    ) -> List[Dict]:

        try:
            result = self._question_service.handle_question(question=question)

            if result and len(result.answer) > 0:
                logger.debug(
                    f"Found answer '{result.answer}' for question with confidence {result.confidence}"
                )
                dispatcher.utter_message(text=result.answer)
            else:
                logger.debug("No answer found for question.")
                dispatcher.utter_message(response="utter_default")

        except Exception as exception:
            logger.error(exception)
            dispatcher.utter_message(response="utter_default")

        # TODO: Extract the subject and set found_object_names

        return [FollowupAction(name=ACTION_LISTEN_NAME)]
