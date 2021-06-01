from typing import List

from rasa.shared.nlu.state_machine.state_machine_models import Intent


class ParameterizedIntentCreator:
    def __init__(self, name: str, parameterized_examples: List[str]):
        self.name = name
        self.parameterized_examples = parameterized_examples

    def create_parameterized_intent(
        self,
        context_name: str,
        context_value: str,
        context_value_synonyms: List[str] = [],
    ) -> Intent:
        examples_replaced = [
            example.replace(
                "{context}",
                f'[{synonym}]{{"entity":"{context_name}", "value": "{context_value}"}}',
            )
            for synonym in context_value_synonyms + [context_value]
            for example in self.parameterized_examples
        ]

        return Intent(
            examples=examples_replaced,
            name=self.name,
            entities=[context_name],
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
)

intent_directions_creator = ParameterizedIntentCreator(
    name="intent_directions_with_entities",
    parameterized_examples=[
        "How do you get to {context}?",
        "What's the way to {context}?",
        "How do I go to {context}?",
        "What are the directions to {context}?",
        "Where is {context}?",
    ],
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
)

intent_what_price_creator = ParameterizedIntentCreator(
    name="intent_what_price_with_entities",
    parameterized_examples=[
        "How much is {context}?",
        "Is {context} expensive?",
        "How much does {context} cost?",
        "What's the cost of {context}?",
        "What's the price of {context}?",
        "How much for {context}?",
        "What price for {context}?",
        "What's the cost {context}?",
    ],
)

intent_what_duration_creator = ParameterizedIntentCreator(
    name="intent_what_duration_with_entities",
    parameterized_examples=[
        "How long is {context}?",
        "What's the length of {context}?",
        "What's the duration of {context}?",
        "How much time does {context} take?",
    ],
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
)
