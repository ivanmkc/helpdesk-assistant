from typing import Optional, List

from rasa.shared.nlu.state_machine.state_machine_models import (
    IntentWithExamples,
)
from random import sample, randint
import copy
import re
import inflect

inflect_engine = inflect.engine()

NUMBERS: List[int] = range(0, 20)


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

    @staticmethod
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

                new_resolved_examples = ParameterizedIntentCreator.resolve_parameterized_example_matches(
                    resolved_example,
                    copy.deepcopy(matches),
                    offset + additional_offset,
                )
                resolved_examples.extend(new_resolved_examples)

            return resolved_examples

    @staticmethod
    def resolve_parameterized_example(example: str) -> List[str]:
        synonym_pattern = r"\[(.+?)\]"

        matches = list(re.finditer(synonym_pattern, example))

        return (
            ParameterizedIntentCreator.resolve_parameterized_example_matches(
                example, matches
            )
        )

    @property
    def parameterized_examples_resolved(self) -> List[str]:
        return [
            example
            for parameterized_example in self.parameterized_examples
            for example in ParameterizedIntentCreator.resolve_parameterized_example(
                parameterized_example
            )
        ]

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
        synonyms_with_the = [
            f"the {synonym_without_the}"
            for synonym_without_the in [
                synonym
                for synonym in base_synonyms
                if not synonym.startswith("the ")
                and not synonym.startswith("The ")
                and not synonym.startswith("a ")
                and not synonym.startswith("an ")
                and not synonym.startswith("your ")
            ]
        ]

        # Add plurals
        synonyms_plural = [
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
        all_synonyms = list(
            set(synonyms_plural + base_synonyms + synonyms_with_the)
        )

        examples_replaced = [
            example.replace(
                "{context}",
                f'[{synonym}]{{"entity":"{self.entity_name}", "value": "{entity_value}"}}',
            )
            for synonym in all_synonyms
            for example in sample(
                self.parameterized_examples,
                min(3, len(self.parameterized_examples_resolved)),
            )
        ]

        # examples_replaced_with_the = [
        #     example.replace(
        #         "{context}",
        #         f'[{synonym}]{{"entity":"{self.entity_name}", "value": "{entity_value}"}}',
        #     )
        #     for synonym in list(set(synonyms_with_the))
        #     for example in sample(
        #         self.parameterized_examples,
        #         min(3, len(self.parameterized_examples)),
        #     )
        #     if "{number}" not in example and "{number_only}" not in example
        # ]

        fixed_examples = []
        for example in [example for example in examples_replaced]:
            if "{number}" in example:
                for number in sample(NUMBERS, 2):
                    number_value = (
                        inflect_engine.number_to_words(number)
                        if randint(0, 1) == 0
                        else number
                    )
                    fixed_examples.append(
                        example.replace("{number}", str(number_value))
                    )

                # Add case with no number
                fixed_examples.append(
                    example.replace(
                        " {number}",
                        "",
                    )
                )
            elif "{number_only}" in example:
                for number in sample(NUMBERS, 2):
                    number_value = (
                        inflect_engine.number_to_words(number)
                        if randint(0, 1) == 0
                        else number
                    )
                    fixed_examples.append(
                        example.replace("{number_only}", str(number_value))
                    )
            else:
                fixed_examples.append(example)

        return IntentWithExamples(
            examples=fixed_examples,
            name=self.name,
            entities=[self.entity_name],
        )
