import os
from pathlib import Path
from typing import Set

import rasa.shared.constants
import rasa.shared.utils.validation
import yaml
from rasa.shared.core.domain import Domain
from rasa.shared.nlu.state_machine.state_machine_models import (
    Action,
    IntentWithExamples,
    Slot,
    Utterance,
)
from rasa.shared.nlu.state_machine.state_machine_state import StateMachineState
from rasa.shared.nlu.training_data.formats import RasaYAMLReader
from rasa.shared.utils.io import dump_obj_as_yaml_to_string, write_text_file

# def get_stories(state: StateMachineState) -> List[Story]:
#     for response in state.responses


def get_domain_nlu(state: StateMachineState, is_initial_state: bool):
    all_entity_names = {entity for entity in state.all_entities()}

    all_intents: Set[IntentWithExamples] = {
        intent for intent in state.all_intents()
    }

    all_actions: Set[Action] = {action for action in state.all_actions()}

    all_utterances: Set[Utterance] = {
        action for action in all_actions if isinstance(action, Utterance)
    }

    all_slots: Set[Slot] = {slot for slot in state.all_slots()}
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
        action_texts=[],
        state_machine_states={
            state.name: {
                "is_initial_state": is_initial_state,
                "state_yaml": yaml.dump(state),
            }
        },
    )

    # Write NLU
    nlu_data = {
        "version": "2.0",
        "nlu": [
            intent.as_nlu_yaml()
            for intent in all_intents
            if isinstance(intent, IntentWithExamples)
        ],
    }

    return domain, nlu_data


# Write NLU
def persist(
    state: StateMachineState,
    is_initial_state: bool,
    domain_folder: str,
    nlu_folder: str,
):
    domain, nlu_data = get_domain_nlu(
        state=state, is_initial_state=is_initial_state
    )

    # Generate filename
    filename = "".join(
        e.lower()
        for e in state.name
        if e.isalnum() or e.isspace() or e in ["-", "_"]
    )
    filename = "_".join(filename.split(" ")) + ".yaml"

    # Persist domain
    domain_filename = os.path.join(domain_folder, filename)
    Path(domain_filename).parent.mkdir(parents=True, exist_ok=True)
    rasa.shared.utils.validation.validate_yaml_schema(
        domain.as_yaml(), rasa.shared.constants.DOMAIN_SCHEMA_FILE
    )
    domain.persist(domain_filename)

    # Persist NLU
    nlu_filename = os.path.join(nlu_folder, filename)
    nlu_data_yaml = dump_obj_as_yaml_to_string(
        nlu_data, should_preserve_key_order=True
    )
    RasaYAMLReader().validate(nlu_data_yaml)
    Path(nlu_filename).parent.mkdir(parents=True, exist_ok=True)
    write_text_file(nlu_data_yaml, nlu_filename)
