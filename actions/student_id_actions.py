import logging
from typing import Dict, Text, Any, List
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher, Action
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import AllSlotsReset, SlotSet
import random

logger = logging.getLogger(__name__)
vers = "vers: 0.1.0, date: Apr 2, 2020"
logger.debug(vers)

class ActionAskName(Action):
    def name(self) -> Text:
        return "action_ask_name"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(response=f"utter_ask_name")
        return []


class ActionAskHometown(Action):
    def name(self) -> Text:
        return "action_ask_hometown"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(response=f"utter_ask_hometown")
        return []


class ActionAskBirthday(Action):
    def name(self) -> Text:
        return "action_ask_birthday"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(response=f"utter_ask_birthday")
        return []


class ActionConfirmName(Action):
    def name(self) -> Text:
        return "action_confirm_name_slot_filled"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(response=f"utter_confirm_name_slot_filled")
        return []

EXPECTED_NAME: str = "Alice"
EXPECTED_HOMETOWN: str = "austin"
class ValidateIDInformation(Action):
    def name(self) -> Text:
        return "action_validate_id_information"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        name = tracker.get_slot("name") 
        hometown = tracker.get_slot("hometown")
        age = tracker.get_slot("age")

        if isinstance(name, list):
            name = name[0]

        if isinstance(hometown, list):
            hometown = hometown[0]

        if isinstance(hometown, list):
            age = age[0]

        is_validated = False
        if all([name, hometown, age]):
            if EXPECTED_NAME.lower() in name.lower() and EXPECTED_HOMETOWN.lower() in hometown.lower() and age == 20:
                is_validated = True
        
        return [SlotSet("name", None), SlotSet("hometown", None), SlotSet("age", None), SlotSet("is_id_card_given", is_validated)]