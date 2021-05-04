from typing import List, Set
from rasa.shared.nlu.state_machine.state_machine_models import (
    Action,
    Intent,
    Slot,
    Utterance,
)

from rasa.shared.core.domain import Domain
from rasa.shared.utils.io import dump_obj_as_yaml_to_string, write_text_file
from rasa.shared.nlu.state_machine.state_machine_state import (
    StateMachineState,
)

from rasa.shared.nlu.training_data.formats import RasaYAMLReader

import rasa.shared.utils.validation
import rasa.shared.constants
import yaml

from data_generation.story_generation import Story, Or, Fork

# def get_stories(state: StateMachineState) -> List[Story]:
#     for response in state.responses


def get_domain_nlu(state: StateMachineState, states_filename: str):
    all_entity_names = {
        entity
        for state in state.all_states()
        for entity in state.all_entities()
    }

    all_intents: Set[Intent] = {
        intent
        for state in state.all_states()
        for intent in state.all_intents()
    }

    all_actions: Set[Action] = {
        action
        for state in state.all_states()
        for action in state.all_actions()
    }

    all_utterances: Set[Utterance] = {
        action for action in all_actions if isinstance(action, Utterance)
    }

    all_slots: Set[Slot] = {
        slot for state in state.all_states() for slot in state.all_slots()
    }
    # all_stories: List[Story] = get_stories(state)

    # Write domain
    domain = Domain(
        intents=[intent.name for intent in all_intents],
        entities=all_entity_names,  # List of entity names
        slots=[slot.as_rasa_slot() for slot in all_slots],
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
        "nlu": [intent.as_nlu_yaml() for intent in all_intents],
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
        domain.as_nlu_yaml(), rasa.shared.constants.DOMAIN_SCHEMA_FILE
    )
    domain.persist(domain_filename)

    nlu_data_yaml = dump_obj_as_yaml_to_string(
        nlu_data, should_preserve_key_order=True
    )
    RasaYAMLReader().validate(nlu_data_yaml)
    write_text_file(nlu_data_yaml, nlu_filename)
