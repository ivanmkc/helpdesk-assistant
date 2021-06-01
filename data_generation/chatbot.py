from dataclasses import dataclass
from rasa.shared.nlu.state_machine.state_machine_state import StateMachineState
from data_generation.state_machine import StateMachine
from data_generation import story_generation
from data_generation.story_generation import Story
from actions import question_answer_action

from typing import List
import os
import shutil


@dataclass
class Chatbot:
    """Class representing everything in a chatbot"""

    state_machine: StateMachine
    stories: List[Story]
    question_answer_context_file_path: str

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
            use_rules=False,
        )

        # Copy context
        shutil.copy(
            self.question_answer_context_file_path,
            question_answer_action.CONTEXT_FILE_PATH,
        )
