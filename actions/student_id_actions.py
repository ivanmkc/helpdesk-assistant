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

        if all([name, hometown, age]):
            if "alice" in name.lower() and "austin" in hometown.lower() and age == 20:
                dispatcher.utter_message(response=f"utter_provide_student_id_card")
                return [SlotSet("is_id_card_given", True)]

        dispatcher.utter_message(response=f"utter_no_id_found")
        
        return [AllSlotsReset()]