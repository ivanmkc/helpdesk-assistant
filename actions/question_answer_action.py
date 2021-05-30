import typing
from typing import Text, Dict, List, Any, Optional
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher, Action

if typing.TYPE_CHECKING:  # pragma: no cover
    from rasa_sdk.types import DomainDict

from services.question_answer_service import (
    QuestionAnswerService,
)

from rasa.shared.core.constants import ACTION_LISTEN_NAME
from rasa_sdk.events import FollowupAction
import logging

logger = logging.getLogger(__name__)
vers = "vers: 0.1.0, date: May 18, 2021"
logger.debug(vers)


CONTEXT_FILE_PATH = "context/context.txt"


class QuestionAnswerAction(Action):
    """
    Action that uses question answer extraction to get the relevant sentence
    """

    def __init__(self) -> None:
        self._question_service = QuestionAnswerService(
            file_path=CONTEXT_FILE_PATH
        )

    def name(self) -> Text:
        return "question_answer_action"

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

        return await self._ask_question(
            dispatcher=dispatcher,
            question=question,
            tracker=tracker,
        )

    async def _ask_question(
        self,
        dispatcher: CollectingDispatcher,
        question: Text,
        tracker: Tracker,
    ) -> List[Dict]:

        try:
            result = self._question_service.handle_question(question=question)

            if result and len(result.answer) > 0:
                dispatcher.utter_message(text=result.answer)
            else:
                dispatcher.utter_message(template="utter_default")

        except Exception as exception:
            logger.debug(exception)
            dispatcher.utter_message(template="utter_default")

        return [FollowupAction(name=ACTION_LISTEN_NAME)]
