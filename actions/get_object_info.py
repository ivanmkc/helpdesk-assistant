import typing
from typing import Text, Dict, List, Any, Optional
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher, Action

if typing.TYPE_CHECKING:  # pragma: no cover
    from rasa_sdk.types import DomainDict

from rasa_sdk.events import FollowupAction
import logging
import yaml

from data_generation.models.object_models import Object
import actions.find_objects_action as find_objects_action
import actions.question_answer_action as question_answer_action
from data_generation.models.object_models import Concept

logger = logging.getLogger(__name__)
vers = "vers: 0.1.0, date: May 18, 2021"
logger.debug(vers)


OBJECTS_FILE_PATH = "context/objects.yaml"

SLOT_OBJECT_ATTRIBUTE = "object_attribute"

ACTION_NAME = "action_get_object_info"


class GetObjectInfo(Action):
    """
    Action that utters intro based on found_object_names and object_attribute
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

        found_object_names = tracker.get_slot(
            find_objects_action.SLOT_FOUND_OBJECT_NAMES
        )
        object_attribute = tracker.get_slot(SLOT_OBJECT_ATTRIBUTE)

        if not found_object_names or not object_attribute:
            # dispatcher.utter_message(response="utter_default")
            FollowupAction(name=question_answer_action.ACTION_NAME)

        found_object: Optional[Concept] = None

        # Find objects of the given name
        for object in self.objects:
            if object.name in found_object_names:
                found_object = object
                break

        # Find objects of the given type
        if not found_object:
            for object in self.objects:
                if found_object:
                    break
                for type in object.types:
                    if type.name in found_object_names:
                        found_object = object
                        break

        # Find objects with the given thing
        if not found_object:
            for object in self.objects:
                if found_object:
                    break
                for thing in object.things_provided:
                    if thing.name in found_object_names:
                        found_object = object
                        break

        if found_object:
            attribute_value = found_object.__getattribute__(object_attribute)

            # Answer with the first value found
            if attribute_value:
                dispatcher.utter_message(text=attribute_value)
                return []
            else:
                # dispatcher.utter_message(
                #     text="Sorry, I don't have the answer to that."
                # )
                return [
                    FollowupAction(name=question_answer_action.ACTION_NAME),
                ]

        # dispatcher.utter_message(
        #     text="Sorry, I don't have the answer to that."
        # )

        return [
            FollowupAction(name=question_answer_action.ACTION_NAME),
        ]
