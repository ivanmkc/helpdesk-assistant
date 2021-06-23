from typing import Optional, List

from rasa.shared.nlu.state_machine.state_machine_models import (
    IntentWithExamples,
)
from random import sample

import inflect

inflect_engine = inflect.engine()


class ParameterizedIntentCreator:
    def __init__(
        self,
        name: str,
        parameterized_examples: List[str],
        entity_name: str,
        object_attribute: Optional[str] = None,
    ):
        self.name = name
        self.parameterized_examples = parameterized_examples
        self.entity_name = entity_name
        self.object_attribute = object_attribute

    def create_parameterized_intent(
        self,
        entity_value: str,
        entity_synonyms: List[str] = [],
        # TODO: Add applicable verbs
    ) -> IntentWithExamples:
        all_synonyms = entity_synonyms + [entity_value]

        # Strip
        all_synonyms = [synonym.strip() for synonym in all_synonyms]
        base_synonyms = all_synonyms[:]

        # Add "the" to synonyms without it
        all_synonyms += [
            f"the {synonym_without_the}"
            for synonym_without_the in [
                synonym
                for synonym in base_synonyms
                if not synonym.startswith("the ")
                and not synonym.startswith("The ")
                and not synonym.startswith("a ")
                and not synonym.startswith("an ")
            ]
        ]

        # Add pluralsI
        all_synonyms += [
            inflect_engine.plural_noun(synonym) for synonym in base_synonyms
        ]

        # # Add singulars
        # all_synonyms += [
        #     synonym
        #     for synonym in [
        #         inflect_engine.singular_noun(synonym)
        #         for synonym in base_synonyms
        #     ]
        #     if isinstance(synonym, str)
        # ]

        # # Add a or an
        # all_synonyms += [
        #     inflect_engine.a(synonym)
        #     for synonym in all_synonyms
        #     if not synonym.startswith("the ")
        #     and not synonym.startswith("The ")
        #     and not synonym.startswith("a ")
        #     and not synonym.startswith("an ")
        # ]

        # Get unique values
        all_synonyms = list(set(all_synonyms))

        examples_replaced = [
            example.replace(
                "{context}",
                f'[{synonym}]{{"entity":"{self.entity_name}", "value": "{entity_value}"}}',
            )
            for synonym in all_synonyms
            for example in sample(
                self.parameterized_examples,
                min(3, len(self.parameterized_examples)),
            )
        ]

        # Sample examples
        # examples_replaced = sample(examples_replaced, 5)

        return IntentWithExamples(
            examples=examples_replaced,
            name=self.name,
            entities=[self.entity_name],
        )
