import logging
from typing import Dict, Text, Any, List
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher, Action
from rasa_sdk.events import SlotSet
import abc

import actions.find_objects_action as find_objects_action
import actions.get_object_info as get_object_info

logger = logging.getLogger(__name__)
vers = "vers: 0.1.0, date: May 18, 2021"
logger.debug(vers)

ACTION_NAME = "action_reset_slots_except_found_object_names"


class ActionResetSlotsExceptObjectNamesSlots(abc.ABC, Action):
    def name(self) -> Text:
        return ACTION_NAME

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        all_slot_names = tracker.slots.keys()
        return [
            SlotSet(slot_name, None)
            for slot_name in all_slot_names
            if slot_name != find_objects_action.SLOT_FOUND_OBJECT_NAMES
            and slot_name != get_object_info.SLOT_OBJECT_ATTRIBUTE
        ]
