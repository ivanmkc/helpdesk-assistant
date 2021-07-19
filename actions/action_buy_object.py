import typing
from typing import Text, Dict, List, Any, Optional
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher, Action
from rasa_sdk.events import SlotSet

if typing.TYPE_CHECKING:  # pragma: no cover
    from rasa_sdk.types import DomainDict

from rasa_sdk.events import FollowupAction
import logging
import yaml

from data_generation.models.object_models import Object
import actions.find_objects_action as find_objects_action
from actions.find_objects_action import OBJECTS_FILE_PATH


logger = logging.getLogger(__name__)
vers = "vers: 0.1.0, date: May 18, 2021"
logger.debug(vers)

ACTION_NAME = "action_buy_object"


class ActionBuyObject(Action):
    objects: List[Object]

    def __init__(self) -> None:
        with open(OBJECTS_FILE_PATH, "r") as file:
            self.objects = yaml.load(file, yaml.Loader)

    def name(self) -> Text:
        return ACTION_NAME

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        slot_names_since_last_user_utterance: List[str] = []
        for event in reversed(tracker.events):
            event_type = event["event"]
            if event_type == "slot":
                slot_names_since_last_user_utterance.append(event["name"])
            elif event_type == "user":
                break

        found_object_names = (
            tracker.get_slot(find_objects_action.SLOT_FOUND_OBJECT_NAMES)
            if find_objects_action.SLOT_FOUND_OBJECT_NAMES
            in slot_names_since_last_user_utterance
            else None
        )

        number_value = (
            tracker.get_slot("number")
            if "number" in slot_names_since_last_user_utterance
            else None
        )

        # Find objects of the given type
        found_objects: List[Object] = []
        for object in self.objects:
            if (
                object.name in found_object_names
                and object.buy_info is not None
            ):
                found_objects.append(object)

        # Disambiguate
        if len(found_objects) == 1:
            found_object = found_objects[0]
            buy_info = found_object.buy_info

            return [
                # Set appropriate slot to the found_object
                SlotSet(key=buy_info.slot_name, value=found_object.name),
                SlotSet(key=buy_info.number_slot_name, value=number_value),
                # Followup with appropriate trigger
                FollowupAction(name=buy_info.trigger_name),
            ]
        elif len(found_objects) > 0:
            dispatcher.utter_message(text=f"You have a few options.")

            for object in found_objects:
                dispatcher.utter_message(text=f"{object.intro}")
        else:
            dispatcher.utter_message(
                text="Hm, I couldn't find anything like that you can buy."
            )

        return []
