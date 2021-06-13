import typing
from typing import Text, Dict, List, Any
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher, Action

if typing.TYPE_CHECKING:  # pragma: no cover
    from rasa_sdk.types import DomainDict

from rasa_sdk.events import AllSlotsReset, SlotSet
import logging
import yaml

from data_generation.models.object_models import Object

logger = logging.getLogger(__name__)
vers = "vers: 0.1.0, date: May 18, 2021"
logger.debug(vers)


OBJECTS_FILE_PATH = "context/objects.yaml"

SLOT_OBJECT_TYPES = "object_types"
SLOT_OBJECT_NAMES = "object_names"
SLOT_OBJECT_ACTIVITY_PROVIDED = "object_activity_provided"
SLOT_OBJECT_THING_PROVIDED = "object_thing_provided"

ACTION_NAME = "action_find_objects"


class FindObjectsAction(Action):
    """
    Action that sets the object_names slot
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

        object_types = (
            tracker.get_slot(SLOT_OBJECT_TYPES)
            if SLOT_OBJECT_TYPES in slot_names_since_last_user_utterance
            else None
        )

        object_names = (
            tracker.get_slot(SLOT_OBJECT_NAMES)
            if SLOT_OBJECT_NAMES in slot_names_since_last_user_utterance
            else None
        )

        object_activity_provided = (
            tracker.get_slot(SLOT_OBJECT_ACTIVITY_PROVIDED)
            if SLOT_OBJECT_ACTIVITY_PROVIDED
            in slot_names_since_last_user_utterance
            else None
        )

        object_thing_provided = (
            tracker.get_slot(SLOT_OBJECT_THING_PROVIDED)
            if SLOT_OBJECT_THING_PROVIDED
            in slot_names_since_last_user_utterance
            else None
        )

        # If no parameters were set, then quit
        if not any(
            [
                object_types,
                object_names,
                object_activity_provided,
                object_thing_provided,
            ]
        ):
            # return [FollowupAction(name=question_answer_action.ACTION_NAME)]
            # return []
            return [AllSlotsReset()]

        # Find objects of the given type
        found_objects: List[Object] = []
        for object in self.objects:

            # Match type if specified
            if object_types and object.type not in object_types:
                continue

            # Match activity if specified
            if object_activity_provided and object_activity_provided not in [
                activity.name for activity in object.activities_provided
            ]:
                continue

            # Match thing if specified
            if object_thing_provided and object_thing_provided not in [
                thing.name for thing in object.things_provided
            ]:
                continue

            # Match object name if specified
            if object_names and object.name not in object_names:
                continue

            found_objects.append(object)

        # if len(found_objects) > 0:
        #     dispatcher.utter_message(text=f"You might try the following:")

        #     for i, obj in enumerate(found_objects, 1):
        #         dispatcher.utter_message(text=f"{i}: {obj.intro}")
        # else:
        #     dispatcher.utter_message(text=f"I don't think I know any.")

        # return [FollowupAction(name=ACTION_LISTEN_NAME)]
        return [
            AllSlotsReset(),
            SlotSet(
                key=SLOT_OBJECT_NAMES,
                value=[object.name for object in found_objects],
            ),
        ]
