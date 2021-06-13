from typing import Optional, List

from rasa.shared.nlu.state_machine.state_machine_models import (
    IntentWithExamples,
)

import actions.find_objects_action as find_objects_action

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

        # Add plurals
        all_synonyms += [
            inflect_engine.plural_noun(synonym) for synonym in base_synonyms
        ]

        # Add singulars
        all_synonyms += [
            synonym
            for synonym in [
                inflect_engine.singular_noun(synonym)
                for synonym in base_synonyms
            ]
            if isinstance(synonym, str)
        ]

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
            for example in self.parameterized_examples
        ]

        return IntentWithExamples(
            examples=examples_replaced,
            name=self.name,
            entities=[self.entity_name],
        )


intent_what_is_context_creator = ParameterizedIntentCreator(
    name="intent_what_is_context_with_entities",
    parameterized_examples=[
        "What is {context}?",
        "What's {context}?",
        "Tell me about {context}.",
        "Can I hear more about {context}?",
        "Do you have more details about {context}",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAMES,
    object_attribute="details",
)

intent_is_there_a_context_creator = ParameterizedIntentCreator(
    name="intent_is_there_a_context_with_entities",
    parameterized_examples=[
        "Is there a {context}?",
        "Is there a {context} around here?",
        "Do you know of any {context}?",
        "Any {context}?",
        "Have you heard about {context}?",
        "You wouldn't know the {context}, would you?",
        "Tell me about the {context}?",
        "I've heard about {context}",
        "I've heard there was a {context}?",
        "I've heard there was a {context}. Know anything about that?",
        "Do you know about a {context}",
        "Tell me about any {context}",
        "Can you point me towards a {context}",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAMES,
)

intent_what_about_context_creator = ParameterizedIntentCreator(
    name="intent_what_about_context_with_entities",
    parameterized_examples=[
        "What about {context}?",
        "How about {context}",
        "And {context}?",
        "How about for {context}?",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAMES,
)


intent_is_there_a_place_with_context_creator = ParameterizedIntentCreator(
    name="intent_is_there_a_place_with_context_with_entities",
    parameterized_examples=[
        "Is there a place to {context}?",
        "Do you know of any places for {context}?",
        "I want to {context}?",
        "Where can I find {context}?",
        "Where would I go for {context}?",
        "I'm looking for {context}?",
        "Is there somewhere with {context}",
        "I want to see {context}",
        "Are there {context}?",
        "Are there {context} around here?",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_THING_PROVIDED,
)


intent_when_is_that_creator = ParameterizedIntentCreator(
    name="intent_what_hours_with_entities",
    parameterized_examples=[
        "What are the hours of {context}?",
        "What time does {context} happpen?",
        "When does {context} open?",
        "When does {context} close?",
        "What are {context} hours?",
        "When does {context} close?",
        "What time does {context} open until?",
        "What time does {context} close?",
        "Is {context} still open?",
        "When would the {context} be open?",
        "When would the {context} open?",
        "When would the {context} close?",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAMES,
    object_attribute="hours",
)

intent_what_price_creator = ParameterizedIntentCreator(
    name="intent_what_price_with_entities",
    parameterized_examples=[
        "How much is {context}?",
        "Is {context} expensive?",
        "Is {context} cheap?",
        "How much does {context} cost?",
        "What's the cost of {context}?",
        "What's the price of {context}?",
        "How much for {context}?",
        "What price for {context}?",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAMES,
    object_attribute="price",
)

intent_what_duration_creator = ParameterizedIntentCreator(
    name="intent_what_duration_with_entities",
    parameterized_examples=[
        "How long is {context}?",
        "What's the length of {context}?",
        "What's the duration of {context}?",
        "How much time does {context} take?",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAMES,
    object_attribute="duration",
)

intent_directions_creator = ParameterizedIntentCreator(
    name="intent_directions_with_entities",
    parameterized_examples=[
        "How do you get to {context}?",
        "What's the way to {context}?",
        "How do I go to {context}?",
        "What are the directions to {context}?",
        "Where is {context}?",
        "Do you know where the {context} is?",
        "Do you know how to get to {context}?",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAMES,
    object_attribute="directions",
)

intent_ill_have_context_creator = ParameterizedIntentCreator(
    name="intent_i_will_have_with_entities",
    parameterized_examples=[
        "Sure, I'll get {context}",
        "I'll have the {context} then",
        "{context} sounds great",
        "Yes, I'll get {context}",
        "I'll have {context}",
        "I'll take a {context}",
        "Ya, {context} sounds good",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAMES,
)

intent_creators = [
    intent_is_there_a_context_creator,
    intent_what_is_context_creator,
    intent_what_about_context_creator,
    intent_directions_creator,
    # intent_is_there_a_place_with_context_creator,
    intent_when_is_that_creator,
    intent_what_price_creator,
    intent_what_duration_creator,
    # intent_ill_have_context_creator,
]
