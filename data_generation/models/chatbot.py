from actions import find_objects_action, get_object_info
from dataclasses import dataclass
from data_generation.models.state_machine import StateMachine
from data_generation.models.object_models import Object
from data_generation.models.story_models import Story
from data_generation.utils import story_generation
from actions import get_object_info
from typing import List
import os
import shutil
import yaml
from typing import Optional

from rasa.shared.nlu.state_machine.state_machine_models import Intent

from rasa.shared.core.slots import FloatSlot, Slot, TextSlot, ListSlot


@dataclass
class Chatbot:
    """Class representing everything in a chatbot"""

    state_machine: Optional[StateMachine]
    stories: List[Story]
    objects: List[Object]
    additional_intents: List[Intent]
    additional_slots: List[Slot]

    @property
    def base_slots(self) -> List[Slot]:
        return [
            ListSlot(
                name=find_objects_action.SLOT_FOUND_OBJECT_NAMES,
            ),
            TextSlot(name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE),
            TextSlot(name=get_object_info.SLOT_OBJECT_ATTRIBUTE),
            FloatSlot(
                name="number", max_value=100, influence_conversation=False
            ),
        ]

    def persist(self, domain_folder: str, nlu_folder: str):
        if self.state_machine:
            self.state_machine.persist(
                domain_folder=domain_folder, nlu_folder=nlu_folder
            )

        domain_filename = os.path.join(domain_folder, "stories.yaml")
        nlu_filename = os.path.join(nlu_folder, "stories.yaml")

        # Stories
        story_generation.persist(
            self.stories,
            domain_filename=domain_filename,
            nlu_filename=nlu_filename,
            additional_intents=self.additional_intents,
            additional_utterances=[
                utterance
                for object in self.objects
                for utterance in object.utterances
            ],
            slots=self.base_slots + self.additional_slots,
            use_rules=False,
        )

        # Create folders
        os.makedirs(
            os.path.dirname(get_object_info.OBJECTS_FILE_PATH), exist_ok=True
        )

        # Object
        with open(get_object_info.OBJECTS_FILE_PATH, "w") as file:
            yaml.dump(self.objects, file)
