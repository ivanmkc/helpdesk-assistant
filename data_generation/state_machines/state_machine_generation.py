from typing import Set
from rasa.shared.nlu.state_machine.state_machine_models import (
    Action,
    Intent,
    Slot,
    Utterance,
)

from rasa.shared.core.domain import Domain
from rasa.shared.core.slots import CategoricalSlot, TextSlot, AnySlot
from rasa.shared.core.slots import Slot as RasaSlot
from rasa.shared.utils.io import dump_obj_as_yaml_to_string, write_text_file
from rasa.shared.nlu.state_machine.state_machine_state import (
    StateMachineState,
)

from rasa.shared.nlu.training_data.formats import RasaYAMLReader

import rasa.shared.utils.validation
import rasa.shared.constants
import yaml


def get_domain_nlu(state: StateMachineState, states_filename: str):
    all_entity_names = state.all_entities()
    all_intents: Set[Intent] = state.all_intents()
    all_utterances: Set[Utterance] = [
        action
        for action in state.all_actions()
        if isinstance(action, Utterance)
    ]
    all_actions: Set[Action] = state.all_actions()
    all_slots: Set[Slot] = state.all_slots()

    # Write domain
    domain = Domain(
        intents=[intent.name for intent in all_intents],
        entities=all_entity_names,  # List of entity names
        slots=[TextSlot(name=slot.name) for slot in all_slots],
        responses={
            utterance.name: [{"text": utterance.text}]
            for utterance in all_utterances
        },
        action_names=[action.name for action in all_actions],
        forms={},
        state_machine={
            "initial_state_name": state.name,
            "states_file": states_filename,
        },
        action_texts=[],
    )

    # Write NLU
    nlu_data = {
        "version": "2.0",
        "nlu": [intent.as_yaml() for intent in all_intents],
    }

    return domain, nlu_data


# Write NLU
def persist(
    state: StateMachineState,
    states_filename: str,
    domain_filename: str,
    nlu_filename: str,
):
    # Persist states
    states_yaml = yaml.dump(
        {state.name: state for state in state.all_states()}
    )
    write_text_file(states_yaml, states_filename)

    domain, nlu_data = get_domain_nlu(state, states_filename)

    # Persist domain
    rasa.shared.utils.validation.validate_yaml_schema(
        domain.as_yaml(), rasa.shared.constants.DOMAIN_SCHEMA_FILE
    )
    domain.persist(domain_filename)

    nlu_data_yaml = dump_obj_as_yaml_to_string(
        nlu_data, should_preserve_key_order=True
    )
    RasaYAMLReader().validate(nlu_data_yaml)
    write_text_file(nlu_data_yaml, nlu_filename)