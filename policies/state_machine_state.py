# Bring your packages onto the path
import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "policies")))

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
    transitionUtterances: List[str]
    destinationState: Optional[str]

    def __init__(
        self,
        name: str,
        condition: Condition,
        transitionUtterances: List[Utterance],
        destinationState: Optional["StateMachineState"],
    ):
        self.name = name
        self.condition = condition
        self.transitionUtterances = [
            utterance.name for utterance in transitionUtterances
        ]
        self.destinationState = (
            destinationState.name if destinationState else None
        )


class StateMachineState:
    name: str
    slots: List[str]
    slotFillUtterances: List[str]
    transitions: List[Transition]
    responses: List[Response]

    def __init__(
        self,
        name: str,
        slots: List[Slot],
        slotFillUtterances: List[Utterance],
        transitions: List[Transition],
        responses: List[Response],
    ):
        self.name = name
        self.slots = [slot.name for slot in slots]
        self.slotFillUtterances = [
            utterance.name for utterance in slotFillUtterances
        ]
        self.transitions = transitions
        self.responses = responses