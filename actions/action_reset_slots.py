import logging
from typing import Dict, Text, Any, List
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher, Action
from rasa_sdk.events import SlotSet
import abc

logger = logging.getLogger(__name__)
vers = "vers: 0.1.0, date: May 18, 2021"
logger.debug(vers)


class ActionResetSlots(abc.ABC, Action):
    @abc.abstractproperty
    def action_name() -> str:
        pass

    @abc.abstractproperty
    def slot_names() -> str:
        pass

    def name(self) -> Text:
        return self.action_name

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        return [SlotSet(slot_name, None) for slot_name in self.slot_names]
