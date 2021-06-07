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
import yaml

from data_generation.models import Object
import actions.find_objects_action as find_objects_action

logger = logging.getLogger(__name__)
vers = "vers: 0.1.0, date: May 18, 2021"
logger.debug(vers)


OBJECTS_FILE_PATH = "context/objects.yaml"

SLOT_OBJECT_ATTRIBUTE = "object_attribute"

ACTION_NAME = "get_object_info"


class GetObjectInfo(Action):
    """
    Action that uses a knowledge base to find relevant objects
    """

    objects: List[Object]

    def __init__(self) -> None:
        with open(OBJECTS_FILE_PATH, "r") as file:
            self.objects = yaml.load(file, yaml.Loader)

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

        object_name = tracker.get_slot(find_objects_action.SLOT_OBJECT_NAME)
        object_attribute = tracker.get_slot(SLOT_OBJECT_ATTRIBUTE)

        if not object_name or not object_attribute:
            dispatcher.utter_message(response="utter_ask_rephrase")
            return []

        # Find objects of the given type
        for object in self.objects:

            if object_name == object.name:
                attribute_value = object.__getattribute__(object_attribute)

                if attribute_value:
                    dispatcher.utter_message(text=attribute_value)
                else:
                    dispatcher.utter_message(
                        text="Sorry, I don't have the answer to that."
                    )

                return []

        dispatcher.utter_message(
            text="Sorry, I don't have the answer to that."
        )

        return []
