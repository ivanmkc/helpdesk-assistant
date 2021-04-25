from typing import List, Optional
from state_machine_models import Action, Slot, Utterance
from conditions import Condition


class Response:
    condition: Condition
    repeatable: bool
    actions: List[str]

    def __init__(
        self,
        condition: Condition,
        actions: List[Action],
        repeatable: bool = True,
    ):
        self.condition = condition
        self.repeatable = repeatable
        self.actions = [action.name for action in actions]


class Transition:
    name: str
    condition: Condition
    transition_utterances: List[str]
    destination_state: Optional[str]

    def __init__(
        self,
        name: str,
        condition: Condition,
        transition_utterances: List[Utterance],
        destination_state: Optional["StateMachineState"],
    ):
        self.name = name
        self.condition = condition
        self.transition_utterances = [
            utterance.name for utterance in transition_utterances
        ]
        self.destination_state = (
            destination_state.name if destination_state else None
        )


class StateMachineState:
    name: str
    slots: List[Slot]
    slot_fill_utterances: List[str]
    transitions: List[Transition]
    responses: List[Response]

    def __init__(
        self,
        name: str,
        slots: List[Slot],
        slot_fill_utterances: List[Utterance],
        transitions: List[Transition],
        responses: List[Response],
    ):
        self.name = name
        self.slots = slots  # [slot.name for slot in slots]
        self.slot_fill_utterances = [
            utterance.name for utterance in slot_fill_utterances
        ]
        self.transitions = transitions
        self.responses = responses