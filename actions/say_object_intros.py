from rasa_sdk.interfaces import ACTION_LISTEN_NAME
import typing
from typing import Text, Dict, List, Any
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher, Action

if typing.TYPE_CHECKING:  # pragma: no cover
    from rasa_sdk.types import DomainDict

from rasa_sdk.events import SlotSet
import logging
import yaml

from rasa_sdk.events import FollowupAction

from data_generation.models.object_models import Object
import actions.get_object_info as get_object_info

logger = logging.getLogger(__name__)
vers = "vers: 0.1.0, date: May 18, 2021"
logger.debug(vers)


OBJECTS_FILE_PATH = "context/objects.yaml"

SLOT_OBJECT_NAME_OR_TYPE = "object_name_or_type"
SLOT_FOUND_OBJECT_NAMES = "found_object_names"
SLOT_OBJECT_ACTIVITY_PROVIDED = "object_activity_provided"

ACTION_NAME = "say_object_intros"


class SayObjectIntrosAction(Action):
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

        found_object_names = tracker.get_slot(SLOT_FOUND_OBJECT_NAMES)
        object_attribute = tracker.get_slot(
            get_object_info.SLOT_OBJECT_ATTRIBUTE
        )

        # If no parameters were set, then quit
        if not found_object_names or len(found_object_names) == 0:
            dispatcher.utter_message(text=f"I don't think I know any.")
            return [FollowupAction(name=ACTION_LISTEN_NAME)]

        # Find objects of the given type
        found_objects: List[Object] = []
        for object in self.objects:
            if object.name in found_object_names:
                found_objects.append(object)

        if len(found_objects) == 1:
            found_object = found_objects[0]
            dispatcher.utter_message(text=found_object.intro)

            if object_attribute:
                attribute_value = found_object.__getattribute__(
                    object_attribute
                )

                if attribute_value:
                    dispatcher.utter_message(text=attribute_value)

        elif len(found_objects) > 0:
            dispatcher.utter_message(text=f"You have a few options.")

            for object in found_objects:
                dispatcher.utter_message(text=f"{object.intro}")
        else:
            dispatcher.utter_message(text=f"I don't think I know any.")

        return [FollowupAction(name=ACTION_LISTEN_NAME)]
