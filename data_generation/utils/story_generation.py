import os
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import rasa.shared.constants
import rasa.shared.utils.validation
from rasa.shared.core.domain import Domain
from rasa.shared.core.slots import Slot
from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    IntentWithExamples,
)
from rasa.shared.nlu.training_data.formats import RasaYAMLReader
from rasa.shared.utils.io import dump_obj_as_yaml_to_string, write_text_file

from data_generation.models.story_models import Story, SlotWasSet


def persist(
    stories: List[Story],
    domain_filename: str,
    nlu_filename: str,
    additional_intents: List[Intent],
    slots: List[Slot],
    use_rules: bool = False,
):
    all_domain = Domain.empty()
    all_intents: Set[Intent] = set(additional_intents)
    all_stories: List[Story] = []
    all_slot_was_sets: Set[SlotWasSet] = set()

    for story in stories:
        domain, sub_stories, intents, slot_was_sets = story.get_domain_nlu(
            use_rules=use_rules
        )

        # print([intent.name for intent in intents])
        # print(domain.intents)

        all_domain = all_domain.merge(domain)
        all_intents.update(intents)
        all_stories.extend(sub_stories)
        all_slot_was_sets.update(slot_was_sets)

    # # Create consolidated slots
    # slots_dict: Dict[str, List[Any]] = {}
    # # Go through all entities and create consolidated slot
    # for slot_was_set in all_slot_was_sets:
    #     for slot in slot_was_set.slots_and_values:
    #         if isinstance(slot, dict):
    #             for entity_name, slot_value in slot:
    #                 new_slot_values = slots_dict.get(entity_name, []) + [
    #                     slot_value
    #                 ]
    #                 slots_dict[entity_name] = list(
    #                     set(new_slot_values)
    #                 )  # Get unique values

    # # Go through all entities and create consolidated slot
    # for intent in all_intents:
    #     for example in intent.examples:
    #         # TODO: Extract entities of form: [City Bus Tour]()

    #         # Extract entities of form: [City Bus Tour]{"entity":"object_name", "value": "City Bus Tour"}
    #         regex = r"\[.+?\](\{.+?\})"
    #         matches = re.finditer(regex, example, re.MULTILINE)
    #         for match in matches:
    #             for groupNum in range(0, len(match.groups())):
    #                 groupNum = groupNum + 1
    #                 group = match.group(groupNum)
    #                 extracted_entity = json.loads(group)
    #                 entity_name = extracted_entity["entity"]
    #                 slot_value = extracted_entity["value"]

    #                 new_slot_values = slots_dict.get(entity_name, []) + [
    #                     slot_value
    #                 ]
    #                 slots_dict[entity_name] = list(
    #                     set(new_slot_values)
    #                 )  # Get unique values

    # slots: List[Slot] = [
    #     CategoricalSlot(name=entity_name, values=slot_values)
    #     for entity_name, slot_values in slots_dict.items()
    # ]

    # Append consolidated slots
    domain_slots = Domain(
        intents=set([intent.name for intent in all_intents]),
        entities=[slot.name for slot in slots],
        slots=slots,
        responses={},
        action_names=[],
        forms=[],
    )
    all_domain = all_domain.merge(domain_slots)

    # Validate domain
    rasa.shared.utils.validation.validate_yaml_schema(
        all_domain.as_yaml(), rasa.shared.constants.DOMAIN_SCHEMA_FILE
    )

    # Write domain
    os.remove(domain_filename)
    all_domain.persist(domain_filename)

    # Write NLU
    nlu_data = {
        "version": "2.0",
        "nlu": [
            intent.as_nlu_yaml()
            for intent in all_intents
            if isinstance(intent, IntentWithExamples)
        ],
        "rules" if use_rules else "stories": all_stories,
    }

    nlu_data_yaml = dump_obj_as_yaml_to_string(
        nlu_data, should_preserve_key_order=True
    )

    RasaYAMLReader().validate(nlu_data_yaml)

    # TODO: Create folders if not existent

    os.remove(nlu_filename)
    write_text_file(nlu_data_yaml, nlu_filename)
