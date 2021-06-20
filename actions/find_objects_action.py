import typing
from typing import Text, Dict, List, Any
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher, Action

if typing.TYPE_CHECKING:  # pragma: no cover
    from rasa_sdk.types import DomainDict

from rasa_sdk.events import SlotSet
import logging
import yaml

from data_generation.models.object_models import Object

logger = logging.getLogger(__name__)
vers = "vers: 0.1.0, date: May 18, 2021"
logger.debug(vers)


OBJECTS_FILE_PATH = "context/objects.yaml"

SLOT_OBJECT_NAME_OR_TYPE = "object_name_or_type"
SLOT_FOUND_OBJECT_NAMES = "found_object_names"
SLOT_OBJECT_ACTIVITY_PROVIDED = "object_activity_provided"

ACTION_NAME = "action_find_objects"


class FindObjectsAction(Action):
    """
    Action that sets the found_object_names slot
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

        slot_names_since_last_user_utterance: List[str] = []
        for event in reversed(tracker.events):
            event_type = event["event"]
            if event_type == "slot":
                slot_names_since_last_user_utterance.append(event["name"])
            elif event_type == "user":
                break

        object_name_or_type = (
            tracker.get_slot(SLOT_OBJECT_NAME_OR_TYPE)
            if SLOT_OBJECT_NAME_OR_TYPE in slot_names_since_last_user_utterance
            else None
        )

        # found_object_names = (
        #     tracker.get_slot(SLOT_FOUND_OBJECT_NAMES)
        #     if SLOT_FOUND_OBJECT_NAMES in slot_names_since_last_user_utterance
        #     else None
        # )

        object_activity_provided = (
            tracker.get_slot(SLOT_OBJECT_ACTIVITY_PROVIDED)
            if SLOT_OBJECT_ACTIVITY_PROVIDED
            in slot_names_since_last_user_utterance
            else None
        )

        # If no parameters were set, then quit
        if not any([object_name_or_type]):
            # return [FollowupAction(name=question_answer_action.ACTION_NAME)]
            # return []
            # return [AllSlotsReset()]
            return []

        found_objects_by_name: List[Object] = []
        found_objects_by_type: List[Object] = []
        found_objects_by_things_provided: List[Object] = []

        for object in self.objects:
            # Find objects by name
            if object_name_or_type == object.name:
                found_objects_by_name.append(object)

            # Find objects by type
            if object_name_or_type in [type.name for type in object.types]:
                found_objects_by_type.append(object)

            # Find objects by things provided
            if object_name_or_type in [
                thing.name for thing in object.things_provided
            ]:
                found_objects_by_things_provided.append(object)

        found_objects = (
            found_objects_by_name
            or found_objects_by_type
            or found_objects_by_things_provided
        )

        return [
            SlotSet(
                key=SLOT_FOUND_OBJECT_NAMES,
                value=[object.name for object in found_objects]
                if len(found_objects) > 0
                else None,
            ),
        ]
