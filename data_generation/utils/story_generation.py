import os
from typing import List, Set

import rasa.shared.constants
import rasa.shared.utils.validation
from rasa.shared.core.domain import Domain
from rasa.shared.core.slots import Slot
from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    IntentWithExamples,
    Utterance,
)
from rasa.shared.nlu.training_data.formats import RasaYAMLReader
from rasa.shared.utils.io import dump_obj_as_yaml_to_string, write_text_file

from data_generation.models.story_models import Story, SlotWasSet
from pathlib import Path
import copy
import re


def persist(
    stories: List[Story],
    domain_filename: str,
    nlu_filename: str,
    additional_intents: List[Intent],
    additional_utterances: List[Utterance],
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

        all_domain = all_domain.merge(domain)
        all_intents.update(intents)
        all_stories.extend(sub_stories)
        all_slot_was_sets.update(slot_was_sets)

    # Append consolidated slots
    domain_slots = Domain(
        intents=set([intent.name for intent in all_intents]),
        entities=[slot.name for slot in slots],
        slots=slots,
        responses={
            utterance.name: [{"text": utterance.text}]
            for utterance in additional_utterances
        },
        action_names=[],
        forms={},
    )
    all_domain = all_domain.merge(domain_slots)

    # Validate domain
    rasa.shared.utils.validation.validate_yaml_schema(
        all_domain.as_yaml(), rasa.shared.constants.DOMAIN_SCHEMA_FILE
    )

    # Write domain
    if os.path.exists(domain_filename):
        os.remove(domain_filename)

    Path(domain_filename).parent.mkdir(parents=True, exist_ok=True)
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

    if os.path.exists(nlu_filename):
        os.remove(nlu_filename)

    Path(nlu_filename).parent.mkdir(parents=True, exist_ok=True)

    write_text_file(nlu_data_yaml, nlu_filename)


def expand_inline_synonyms(example: str) -> List[str]:
    """
    Creates multiple examples from examples with inline synonyms, e.g.:

    'I'm from [NYC|New York City|New York]'
    """

    def resolve_parameterized_example_matches(
        example: str, matches: List[re.Match], offset: int = 0
    ) -> List[str]:
        if len(matches) == 0:
            return [example]
        else:
            # Assuming the matches go from left to right
            resolved_examples = []
            # while len(matches) > 0:
            match = matches.pop(0)

            # Replace match
            start_index = match.span(1)[0] + offset
            end_index = match.span(1)[1] + offset
            match_length = end_index - start_index
            synonyms = example[start_index:end_index].split("|")
            for synonym in synonyms:
                resolved_example = (
                    example[: start_index - 1]
                    + synonym
                    + example[end_index + 1 :]
                )
                additional_offset = (
                    len(synonym) - match_length - 2
                )  # Minus 2 for brackets

                new_resolved_examples = resolve_parameterized_example_matches(
                    resolved_example,
                    copy.deepcopy(matches),
                    offset + additional_offset,
                )
                resolved_examples.extend(new_resolved_examples)

            return resolved_examples

    synonym_pattern = r"\[(.+?)\]"

    matches = list(re.finditer(synonym_pattern, example))

    return [
        " ".join(example_resolved.split()).strip()
        for example_resolved in resolve_parameterized_example_matches(
            example, matches
        )
    ]
