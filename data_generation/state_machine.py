from dataclasses import dataclass
from rasa.shared.nlu.state_machine.state_machine_state import StateMachineState
from data_generation import state_machine_generation
from typing import List


@dataclass
class StateMachine:
    initial_state: StateMachineState
    other_states: List[StateMachineState]

    def persist(self, domain_folder: str, nlu_folder: str):
        state_machine_generation.persist(
            state=self.initial_state,
            is_initial_state=True,
            domain_folder=domain_folder,
            nlu_folder=nlu_folder,
        )

        for state in self.other_states:
            state_machine_generation.persist(
                state=state,
                is_initial_state=False,
                domain_folder=domain_folder,
                nlu_folder=nlu_folder,
            )
