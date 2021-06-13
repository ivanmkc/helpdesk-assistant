from dataclasses import dataclass
from rasa.shared.nlu.state_machine.state_machine_state import StateMachineState
from data_generation.state_machine import StateMachine
from data_generation import story_generation
from data_generation.models import Object
from data_generation.story_generation import Story
from actions import question_answer_action, get_object_info
from typing import List
import os
import shutil
import yaml

from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
)

from rasa.shared.core.slots import Slot, TextSlot, ListSlot


@dataclass
class Chatbot:
    """Class representing everything in a chatbot"""

    state_machine: StateMachine
    stories: List[Story]
    objects: List[Object]
    additional_intents: List[Intent]
    question_answer_context_file_path: str

    @property
    def base_slots(self) -> List[Slot]:
        return [
            ListSlot(name="object_names"),
            TextSlot(name="object_type"),
            TextSlot(name="object_attribute"),
            TextSlot(name="object_thing_provided"),
        ]

    def persist(self, domain_folder: str, nlu_folder: str):
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
            slots=self.base_slots,
            use_rules=False,
        )

        # Object
        with open(get_object_info.OBJECTS_FILE_PATH, "w") as file:
            yaml.dump(self.objects, file)

        shutil.copy(
            self.question_answer_context_file_path,
            question_answer_action.CONTEXT_FILE_PATH,
        )
